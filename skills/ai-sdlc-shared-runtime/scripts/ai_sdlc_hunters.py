#!/usr/bin/env python3
"""Source-bound hunter candidates, deterministic gates and native handoffs.

Pure analysis by default. Only reproduce executes an explicitly selected test,
in a disposable source copy with a 30 second deadline; it is not an OS sandbox.
No lifecycle mutation. Explicit output uses the existing atomic path contract.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import copy

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ai_sdlc_toon import decode_toon, encode_toon
from ai_sdlc_safe_io import bounded_path, atomic_write_text

_contract_path = HERE.parent / 'references/hunters.schema.toon'
if not _contract_path.is_file():
    _peer = HERE.parents[3] / "products" / "ai-sdlc-loop" / "skills" / "ai-sdlc-loop-shared-runtime" / "references" / "hunters.schema.toon"
    if _peer.is_file():
        _contract_path = _peer
CONTRACT = decode_toon(_contract_path.read_text(encoding='utf-8'))

CANDIDATE = 'ai-sdlc-hunter-candidates/v1'
REPORT = 'ai-sdlc-hunter-report/v1'
REPRO = 'ai-sdlc-hunter-reproduction/v1'
KINDS = ('edge-case-hunter','blind-case-hunter','bug-hunter')
SEVERITIES = ('critical','high','medium','low','info')
ROLES = ('requirements','design','implementation','tests','operations')
LENSES = dict(zip(KINDS,('edge-case-hunt','assumption-challenge','adversarial-review')))
RULES = {
 'INPUT': (r'\b(input|argument|parameter|request|array|list)\b',('requirements','tests')),
 'TIME': (r'\b(datetime|timestamp|timezone|date range|DST)\b',('requirements','design','tests')),
 'NETWORK': (r'\b(requests|httpx|external API|provider|HTTP)\b',('requirements','design','tests')),
 'RETRY': (r'\b(retry|retries|external API|provider)\b',('requirements','design','tests')),
 'PERSISTENCE': (r'\b(database|sqlite|sqlalchemy|persist|transaction)\b',('design','implementation','tests')),
 'CONCURRENCY': (r'\b(async|thread|concurrent|transaction)\b',('design','implementation','tests')),
 'IDEMPOTENCY': (r'\b(retry|persist|database|transaction)\b',('requirements','design','tests')),
 'PERMISSIONS': (r'\b(permission|role|admin|authentication|tenant)\b',('requirements','design','tests')),
 'DATA_VOLUME': (r'\b(pagination|page size|batch|large dataset)\b',('requirements','design','tests')),
 'NUMERIC': (r'\b(decimal|precision|integer|amount|price|float)\b',('requirements','tests')),
 'ENCODING': (r'\b(encoding|UTF|unicode|serialize|text)\b',('requirements','tests')),
 'LIFECYCLE': (r'\b(state|workflow|activate|delete|deletion)\b',('requirements','design','tests')),
}
BLIND = {
 'ACTORS': ('INPUT',('actor','user','system actor')),
 'FAILURE_RECOVERY': ('NETWORK',('recovery','provider failure','dependency failure')),
 'ROLLBACK': ('PERSISTENCE',('rollback','restore previous')),
 'MIGRATION': ('PERSISTENCE',('migration','migrate')),
 'PERMISSIONS': ('PERMISSIONS',('authorization','permission denied')),
 'OPERATIONS': ('LIFECYCLE',('runbook','operational procedure','support workflow')),
 'TEMPORAL_MODEL': ('TIME',('timezone','temporal model','DST')),
 'TENANCY': ('PERMISSIONS',('tenant isolation','single tenant')),
}

class Invalid(ValueError):
    pass


def require(condition, code):
    if not condition: raise Invalid(code)


def digest(value):
    return hashlib.sha256(encode_toon(value).encode('utf-8')).hexdigest()


def strings(value, label, *, nonempty=False):
    require(isinstance(value,list) and (bool(value) or not nonempty) and all(isinstance(x,str) and x.strip() and len(x)<=180 for x in value), 'SCHEMA_ERROR: '+label)
    return sorted(set(value))


def text(value,label):
    require(isinstance(value,str) and bool(value.strip()) and len(value)<=180,'SCHEMA_ERROR: '+label)
    return ' '.join(value.split())


def read(root,path):
    target=bounded_path(root,Path(path))
    require(target.is_file() and target.stat().st_size<=256_000,'ARTIFACT_NOT_FOUND: bounded regular file required')
    return target.read_text(encoding='utf-8')


def load(root,path):
    target=bounded_path(root,Path(path))
    require(target.is_file() and target.stat().st_size<=4_000_000,'ARTIFACT_NOT_FOUND: bounded artifact required')
    return decode_toon(target.read_text(encoding='utf-8'))


def sources(root,inventory):
    require(isinstance(inventory,list) and 1<=len(inventory)<=32,'SCHEMA_ERROR: source inventory requires 1..32 files')
    result=[];seen=set();total=0
    for row in inventory:
        require(isinstance(row,dict) and set(row)=={'path','role'} and row['role'] in ROLES,'SCHEMA_ERROR: source fields')
        path=row['path'];require(isinstance(path,str) and not Path(path).is_absolute() and '..' not in Path(path).parts,'INVALID_INPUT: source path')
        require(path not in seen,'SCHEMA_ERROR: duplicate source');seen.add(path)
        content=read(root,path);total+=len(content.encode('utf-8'))
        require(total<=1_000_000,'ANALYSIS_INCOMPLETE: source budget exceeded')
        result.append(dict(path=path,role=row['role'],sha256=hashlib.sha256(content.encode('utf-8')).hexdigest()))
    return sorted(result,key=lambda x:x['path'])


def snapshot(root,value):
    actual=sources(root,[dict(path=s['path'],role=s['role']) for s in value['sources']])
    require(actual==value['sources'],'EVIDENCE_UNRESOLVED: stale source snapshot')
    return {s['path']:read(root,s['path']) for s in actual}


def dimensions(contents):
    combined='\n'.join(contents.values())
    return sorted(k for k,(pattern,roles) in RULES.items() if re.search(pattern,combined,re.I))


def signals(contents,rows):
    result=[]
    kinds={ast.If:'CONDITIONAL',ast.Assign:'STATE_MUTATION',ast.Try:'ERROR_HANDLING',ast.Call:'CALL_BOUNDARY',ast.AsyncFunctionDef:'CONCURRENCY'}
    for row in rows:
        if row['role']!='implementation' or not row['path'].endswith('.py'):continue
        path=row['path']
        try:
            tree=ast.parse(contents[path])
            for node in ast.walk(tree):
                if type(node) in kinds:result.append(dict(path=path,line=node.lineno,kind=kinds[type(node)]))
        except SyntaxError as exc:result.append(dict(path=path,line=exc.lineno or 1,kind='SYNTAX_ERROR'))
    result=sorted(result,key=lambda r:(r['path'],r['line'],r['kind']))
    require(len(result)<=200,'ANALYSIS_INCOMPLETE: narrow implementation scope below 200 risk signals')
    return result


def prepare(root,hunter,scope,inventory):
    require(hunter in KINDS,'INVALID_INPUT: hunter')
    rows=sources(root,inventory)
    contents={s['path']:read(root,s['path']) for s in rows}
    selected=dimensions(contents)
    if hunter=='blind-case-hunter':selected=sorted(k for k,(signal,terms) in BLIND.items() if signal in selected)
    if hunter=='bug-hunter':selected=['IMPLEMENTATION'] if any(s['role']=='implementation' for s in rows) else []
    return dict(schema=CANDIDATE,hunter=hunter,scope=text(scope,'scope'),sources=rows,dimensions=selected,iteration=1,signals=signals(contents,rows),candidates=[],coverage=[],related_reports=[])


def anchor(contents,value):
    require(isinstance(value,dict) and set(value)=={'path','line','quote'},'SCHEMA_ERROR: evidence anchor')
    require(value['path'] in contents and type(value['line']) is int and value['line']>0,'EVIDENCE_UNRESOLVED: location')
    quote=text(value['quote'],'quote');lines=contents[value['path']].splitlines()
    require(value['line']<=len(lines) and quote in lines[value['line']-1],'EVIDENCE_UNRESOLVED: quoted evidence')
    return dict(path=value['path'],line=value['line'],quote=quote)


def absence(contents,source_rows,dimension):
    signal,terms=BLIND[dimension]
    needed=set(RULES[signal][1])
    if dimension in {'ROLLBACK','OPERATIONS','MIGRATION'}:needed.add('operations')
    roles={s['role'] for s in source_rows}
    matches=[]
    for path,content in sorted(contents.items()):
        for number,line in enumerate(content.splitlines(),1):
            if any(re.search(r'\b'+re.escape(term)+r'\b',line,re.I) for term in terms):
                matches.append(dict(path=path,line=number))
    return dict(dimension=dimension,required_roles=sorted(needed),searched_paths=sorted(contents),missing_roles=sorted(needed-roles),matches=matches,status='UNKNOWN' if needed-roles else 'REQUIRES_REVIEW' if matches else 'ABSENT_IN_DECLARED_SCOPE')


def validate_reproduction(root,receipt,value):
    require(isinstance(receipt,dict) and set(receipt)=={'schema','source_snapshot','test_path','log_path','log_sha256','exit_code','failures','errors','status','fingerprint'} and receipt.get('schema')==REPRO,'SCHEMA_ERROR: reproduction receipt')
    require(receipt.get('fingerprint')==digest({k:v for k,v in receipt.items() if k!='fingerprint'}),'EVIDENCE_UNRESOLVED: reproduction fingerprint')
    require(receipt['source_snapshot']==digest(value['sources']),'EVIDENCE_UNRESOLVED: reproduction source drift')
    require(receipt['test_path'] in {s['path'] for s in value['sources'] if s['role']=='tests'},'EVIDENCE_UNRESOLVED: test outside source scope')
    require(receipt['status'] in {'REPRODUCED','UNVERIFIED'} and all(type(receipt[k]) is int for k in ('exit_code','failures','errors')),'SCHEMA_ERROR: reproduction outcome')
    log=read(root,receipt['log_path'])
    require(hashlib.sha256(log.encode('utf-8')).hexdigest()==receipt['log_sha256'],'EVIDENCE_UNRESOLVED: reproduction log drift')
    observed_failures,observed_errors=test_outcome(log)
    require((receipt.get('failures'),receipt.get('errors'))==(observed_failures,observed_errors),'EVIDENCE_UNRESOLVED: reproduction summary contradicts log')
    return receipt.get('status')=='REPRODUCED' and receipt.get('exit_code')==1 and receipt.get('failures',0)>0 and receipt.get('errors')==0


def evaluate(root,value,ancestors=(),verified=None):
    verified={} if verified is None else verified
    require(isinstance(value,dict) and set(value)==set(CONTRACT['candidate_fields']),'SCHEMA_ERROR: candidate fields')
    require(value['schema']==CANDIDATE and value['hunter'] in KINDS,'SCHEMA_ERROR: candidate identity')
    require(type(value['iteration']) is int and 1<=value['iteration']<=3,'ANALYSIS_INCOMPLETE: repair limit')
    value=copy.deepcopy(value)
    contents=snapshot(root,value);hunter=value['hunter'];scope=text(value['scope'],'scope')
    expected=prepare(root,hunter,scope,[dict(path=s['path'],role=s['role']) for s in value['sources']])['dimensions']
    require(value['signals']==signals(contents,value['sources']),'SCHEMA_ERROR: risk signals changed')
    require(value['dimensions']==expected,'SCHEMA_ERROR: applicable dimensions changed')
    require(isinstance(value['coverage'],list) and len(value['coverage'])<=32,'SCHEMA_ERROR: coverage array')
    require(isinstance(value['candidates'],list) and len(value['candidates'])<=100,'SCHEMA_ERROR: at most 100 candidates')
    value['candidates'].sort(key=digest)
    value['coverage'].sort(key=digest)
    value['related_reports']=strings(value['related_reports'],'related_reports')
    require(len(value['related_reports'])<=8,'ANALYSIS_INCOMPLETE: related report budget')
    coverage={}
    for row in value['coverage']:
        require(set(row)=={'dimension','status','evidence'} and row['dimension'] in expected and row['status'] in {'OUT_OF_SCOPE','NOT_APPLICABLE','COVERED_ELSEWHERE'},'SCHEMA_ERROR: coverage decision')
        require(row['dimension'] not in coverage,'SCHEMA_ERROR: conflicting coverage decision')
        coverage[row['dimension']]=dict(row,evidence=anchor(contents,row['evidence']))
    related={}
    for path in strings(value['related_reports'],'related_reports'):
        report=load(root,path)
        require(report.get('schema')==REPORT and report.get('fingerprint')==digest({k:v for k,v in report.items() if k!='fingerprint'}),'EVIDENCE_UNRESOLVED: related report')
        resolved=str(bounded_path(root,Path(path)))
        require(resolved not in ancestors and len(ancestors)<8,'EVIDENCE_UNRESOLVED: cyclic or excessive related reports')
        if resolved not in verified:
            require(len(verified)<32,'ANALYSIS_INCOMPLETE: related report graph budget')
            verified[resolved]=None
            require(report==evaluate(root,report['input'],ancestors+(resolved,),verified),'EVIDENCE_UNRESOLVED: related report evaluation drift')
            verified[resolved]=report
        else:require(verified[resolved]==report,'EVIDENCE_UNRESOLVED: related report changed during evaluation')
        for finding in report['findings']:related[finding['id']]=finding
    findings=[];duplicates=[];seen={};queries=[]
    fields=set(CONTRACT['finding_fields'])
    for candidate in value['candidates']:
        require(isinstance(candidate,dict) and set(candidate)==fields,'SCHEMA_ERROR: finding fields')
        dimension=candidate['dimension'];require(dimension in expected,'SCHEMA_ERROR: inapplicable dimension')
        require(candidate['severity'] in SEVERITIES and candidate['evidence_type'] in {'OBSERVED','INFERRED','HYPOTHETICAL'},'SCHEMA_ERROR: evidence or severity enum')
        evidence=anchor(contents,candidate['evidence'])
        trace_targets=strings(candidate['trace_targets'],'trace_targets',nonempty=True)
        for trace in trace_targets:require(any(re.search(r'(?<![\w-])'+re.escape(trace)+r'(?![\w-])',c) for c in contents.values()),'EVIDENCE_UNRESOLVED: trace target '+trace)
        tests=strings(candidate['test_refs'],'test_refs')
        require(set(tests)<={s['path'] for s in value['sources'] if s['role']=='tests'},'EVIDENCE_UNRESOLVED: test mapping')
        links=strings(candidate['related_findings'],'related_findings');require(set(links)<=set(related),'EVIDENCE_UNRESOLVED: related finding')
        review=candidate['review'];require(isinstance(review,dict) and set(review)=={'decision','reason'} and review['decision'] in {'PENDING','ACCEPT','REJECT'},'SCHEMA_ERROR: semantic review')
        reason=text(review['reason'],'review reason')
        signature=text(candidate['signature'],'signature').casefold()
        identity='HUNT-'+digest([hunter,scope,dimension,evidence['path'],signature])[:20]
        status='UNVERIFIED';validation='INSUFFICIENT_EVIDENCE'
        if review['decision']=='REJECT':status='REJECTED';validation='REVIEW_REJECTED'
        elif dimension in coverage:status='REJECTED';validation=coverage[dimension]['status']
        elif hunter=='edge-case-hunter':status='MAPPED' if tests else 'PROPOSED';validation='SCENARIO_NOT_EXECUTED'
        elif hunter=='blind-case-hunter':
            query=absence(contents,value['sources'],dimension);queries.append(query)
            if query['status']=='ABSENT_IN_DECLARED_SCOPE' and review['decision']=='ACCEPT':status='MISSING';validation='SCOPED_ABSENCE_REVIEWED'
            elif query['matches']:status='UNVERIFIED';validation='COVERAGE_REQUIRES_REVIEW'
            else:status='UNKNOWN';validation='SEARCH_INCOMPLETE'
        else:
            require(next(s['role'] for s in value['sources'] if s['path']==evidence['path'])=='implementation','EVIDENCE_UNRESOLVED: bug needs implementation location')
            if candidate['evidence_type']=='OBSERVED' and review['decision']=='ACCEPT':status='SUPPORTED';validation='CODE_REVIEWED_NOT_REPRODUCED'
            if candidate['reproduction']:
                receipt=load(root,candidate['reproduction'])
                require(receipt.get('test_path') in tests,'EVIDENCE_UNRESOLVED: reproduction is not mapped to this candidate')
                proven=validate_reproduction(root,receipt,value)
                if proven:
                    status='CONFIRMED' if review['decision']=='ACCEPT' and candidate['evidence_type']=='OBSERVED' else 'REPRODUCED'
                    validation='TEST_FAILURE_AND_REVIEW' if status=='CONFIRMED' else 'TEST_FAILURE_REQUIRES_REVIEW'
                else:status='UNVERIFIED';validation='REPRODUCTION_INCONCLUSIVE'
        record=dict(id=identity,hunter=hunter,lens=LENSES[hunter],dimension=dimension,title=text(candidate['title'],'title'),condition=text(candidate['condition'],'condition'),expected=text(candidate['expected'],'expected'),severity=candidate['severity'],impact=text(candidate['impact'],'impact'),evidence_type=candidate['evidence_type'],evidence=dict(evidence,detail=evidence['quote']),trace_targets=trace_targets,owner=text(candidate['owner'],'owner'),next_action=text(candidate['next_action'],'next_action'),resolution_status='rejected' if status=='REJECTED' else 'open',validation_status=status,validation_reason=validation,review_reason=reason,test_refs=tests,related_findings=links,reproduction=candidate['reproduction'])
        if identity in seen:
            require(seen[identity]==record,'SCHEMA_ERROR: duplicate signature has conflicting facts')
            duplicates.append(identity)
        else:seen[identity]=record;findings.append(record)
    findings.sort(key=lambda f:(SEVERITIES.index(f['severity']),{'CONFIRMED':0,'REPRODUCED':1,'SUPPORTED':2}.get(f['validation_status'],3),f['evidence']['path'],f['evidence']['line'],f['id']))
    report=dict(schema=REPORT,hunter=hunter,scope=scope,input=value,findings=findings,duplicate_ids=sorted(set(duplicates)),absence_searches=sorted(queries,key=lambda q:q['dimension']),coverage=sorted(coverage.values(),key=lambda c:c['dimension']),dimensions_applicable=expected,dimensions_with_cases=sorted({f['dimension'] for f in findings if f['validation_status']!='REJECTED'}),execution='PASS' if expected and (findings or coverage) else 'BLOCKED',authorizes_execution=False,limitations=['Semantic review is supplied evidence, not independent proof','Negative search is scoped lexical evidence, not whole-repository absence','Test mapping does not imply executed coverage'])
    report['fingerprint']=digest(report)
    return report


def test_outcome(log):
    # Parent-appended trailer comes from unittest.TestResult, never test stdout.
    match=re.search(r"\nHUNTER_RESULT failures=(\d+) errors=(\d+)\n\Z",log)
    require(match is not None,'EVIDENCE_UNRESOLVED: missing structured test result')
    return int(match[1]),int(match[2])


REPRO_RUNNER = """import pathlib, sys, unittest
root, test, result_path = sys.argv[1:]
suite = unittest.defaultTestLoader.discover(str(pathlib.Path(root)/pathlib.Path(test).parent), pattern=pathlib.Path(test).name, top_level_dir=root)
result = unittest.TextTestRunner(verbosity=2).run(suite)
pathlib.Path(result_path).write_text(str(len(result.failures))+' '+str(len(result.errors))+' '+str(result.testsRun), encoding='utf-8')
sys.exit(0 if result.wasSuccessful() else 1)
"""


def reproduce(root,value,test_path,log_path):
    contents=snapshot(root,value)
    require(log_path not in contents,'INVALID_INPUT: log would overwrite source')
    require(test_path in {s['path'] for s in value['sources'] if s['role']=='tests'} and Path(test_path).name.startswith('test_') and test_path.endswith('.py'),'INVALID_INPUT: explicit Python unittest source required')
    with tempfile.TemporaryDirectory(prefix='hunter-repro-') as directory:
        temporary=Path(directory)
        for path,content in contents.items():
            destination=temporary/path;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(content,encoding='utf-8')
        try:
            result_path=temporary/'__hunter_result__'
            require(not result_path.exists(),'INVALID_INPUT: reserved reproduction result path')
            command=[sys.executable,'-I','-B','-c',REPRO_RUNNER,str(temporary),test_path,str(result_path)]
            process=subprocess.run(command,cwd=temporary,capture_output=True,text=True,timeout=30,encoding='utf-8',errors='replace')
            log=(process.stdout+process.stderr).replace(str(temporary),'<fixture>')
            log=re.sub(r'(Ran \d+ tests? in )\d+(?:\.\d+)?s',r'\1<elapsed>s',log)
            code=process.returncode
            counts=result_path.read_text(encoding='utf-8').split() if result_path.is_file() else []
            if len(counts)==3 and all(n.isdigit() for n in counts) and int(counts[2])>0:
                failures,errors=map(int,counts[:2])
            else:failures,errors=0,1
        except subprocess.TimeoutExpired:
            log='REPRODUCTION_FAILED: deadline exceeded\n';code=124;failures,errors=0,1
    log+='\nHUNTER_RESULT failures='+str(failures)+' errors='+str(errors)+'\n'
    require(len(log.encode('utf-8'))<=256_000,'TOOL_FAILURE: reproduction output exceeds limit')
    failures,errors=test_outcome(log)
    receipt=dict(schema=REPRO,source_snapshot=digest(value['sources']),test_path=test_path,log_path=log_path,log_sha256=hashlib.sha256(log.encode('utf-8')).hexdigest(),exit_code=code,failures=failures,errors=errors,status='REPRODUCED' if code==1 and failures>0 and errors==0 else 'UNVERIFIED')
    receipt['fingerprint']=digest(receipt)
    atomic_write_text(root,Path(log_path),log)
    return receipt


def render(skill_root,report):
    import chat_output as chat
    contract=chat.contract(skill_root)
    hunter=report['hunter'];rows=[];unverified=[]
    for f in report['findings']:
        if f['validation_status']=='REJECTED':continue
        if hunter=='bug-hunter' and f['validation_status'] not in {'SUPPORTED','CONFIRMED'}:
            unverified.append(dict(zip(contract['secondary'],[f['id'],f['evidence']['path']+':'+str(f['evidence']['line']),f['validation_status'],f['next_action']])))
            continue
        if hunter=='edge-case-hunter':values=[f['id'],f['condition'],f['dimension'],f['impact'],f['expected'],f['validation_status']]
        elif hunter=='blind-case-hunter':values=[f['id'],f['title'],f['dimension'],f['validation_reason'],f['impact'],f['next_action']]
        else:values=[f['id'],f['severity'].upper() if f['severity']!='info' else 'N/A',f['evidence']['path']+':'+str(f['evidence']['line']),f['title'],f['validation_reason'],f['validation_status']]
        rows.append(dict(zip(contract['primary'],values)))
    state='BLOCKED' if report['execution']=='BLOCKED' else 'WARNING' if any(f['validation_status'] in {'MISSING','CONFIRMED','SUPPORTED','REPRODUCED','UNKNOWN','UNVERIFIED'} for f in report['findings']) else 'PASS'
    result=dict(schema='ai-sdlc-chat-result/v1',summary=dict(Status=state,Decision='Diagnostic proposals; no delivery approval',Evidence=report['fingerprint']),primary=rows,secondary=unverified,actions=[],full_artifact='native hunter report.toon')
    if state=='BLOCKED':
        result['failures']=[dict(zip(contract['failure'],[report['scope'],'BLOCKED','No applicable supported analysis','source snapshot','Supply scoped behavior and candidates']))]
        result['actions']=[{'Owner':'Analyst','Next action':'Supply scoped behavior and candidates','Expected evidence':'Current source-bound input'}]
    elif report['findings']:result['actions']=[{'Owner':f['owner'],'Next action':f['id']+': '+f['next_action'][:130],'Expected evidence':'Validated downstream artifact'} for f in report['findings'][:8]]
    output=chat.render(contract,result);require(chat.evaluate(contract,output)['status']=='PASS','BAD_RENDERING: native chat evaluation failed')
    return output


def self_check():
    """Safe synthetic gates for Doctor; never invoke reproduction or recurse."""
    with tempfile.TemporaryDirectory(prefix='hunter-self-check-') as directory:
        root=Path(directory)
        (root/'requirements.md').write_text('REQ-01: input uses external API timestamp.\n',encoding='utf-8')
        (root/'app.py').write_text('def run():\n    return 1\n',encoding='utf-8')
        inventory=[dict(path='requirements.md',role='requirements'),dict(path='app.py',role='implementation')]
        identities=[]
        for hunter in KINDS:
            value=prepare(root,hunter,'doctor-fixture',inventory)
            path='app.py' if hunter=='bug-hunter' else 'requirements.md'
            candidate=dict(signature='boundary',dimension=value['dimensions'][0],title='Boundary proposal',condition='Input reaches a boundary',expected='REQ-01 remains satisfied',severity='medium',impact='Contract may not hold',evidence_type='HYPOTHETICAL',evidence=dict(path=path,line=1,quote=read(root,path).splitlines()[0]),trace_targets=['REQ-01'],owner='QA',next_action='Verify the scenario',review=dict(decision='PENDING',reason='Semantic review is required'),test_refs=[],related_findings=[],reproduction='')
            value['candidates']=[candidate]
            first=evaluate(root,value);second=evaluate(root,value)
            require(encode_toon(first)==encode_toon(second),'BAD_DETERMINISM: repeated hunter report')
            require(first['findings'][0]['validation_status']!='CONFIRMED','BAD_EVIDENCE_VALIDATION: hypothesis promoted')
            if hunter=='blind-case-hunter':require(first['findings'][0]['validation_status']=='UNKNOWN','BAD_SCOPE: incomplete absence search')
            identities.append(first['findings'][0]['id'])
        require(len(set(identities))==3,'BAD_DEDUPLICATION: cross-hunter identity collapse')
    return 'three hunter gates, scoped absence, stable IDs and repeated reports passed'


def evidence_paths(root,value,visited=None,traversed=None):
    """Bounded closure of sources, reports, receipts and logs before writes."""
    visited=set() if visited is None else visited
    traversed=set() if traversed is None else traversed
    require(len(visited)<=128,'ANALYSIS_INCOMPLETE: evidence reference budget')
    candidate=value.get('input',value) if isinstance(value,dict) else {}
    for source in candidate.get('sources',[]):visited.add(bounded_path(root,Path(source['path'])))
    for path in candidate.get('related_reports',[]):
        resolved=bounded_path(root,Path(path))
        if resolved not in traversed:
            traversed.add(resolved)
            visited.add(resolved);evidence_paths(root,load(root,path),visited,traversed)
    for finding in candidate.get('candidates',[]):
        path=finding.get('reproduction')
        if path:
            visited.add(bounded_path(root,Path(path)))
            receipt=load(root,path)
            visited.add(bounded_path(root,Path(receipt['log_path'])))
    require(len(visited)<=128,'ANALYSIS_INCOMPLETE: evidence reference budget')
    return visited


def main(hunter=None,skill_root=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('prepare','evaluate','verify','render','reproduce','handoff','verify-handoff'))
    p.add_argument('--root',type=Path,required=True);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--hunter',choices=KINDS,default=hunter);p.add_argument('--scope');p.add_argument('--output',type=Path);p.add_argument('--report',type=Path)
    p.add_argument('--test');p.add_argument('--log');p.add_argument('--quick-flow',action='store_true');p.add_argument('--full-flow',action='store_true')
    p.add_argument('--state-check',action='store_true');p.add_argument('--begin-state',action='store_true');p.add_argument('--complete-state',action='store_true')
    args=p.parse_args()
    try:
        require(not args.begin_state and not args.complete_state and not args.state_check,'OKF_ERROR: hunters do not own lifecycle state')
        require(not (args.quick_flow and args.full_flow),'INVALID_INPUT: conflicting flow flags')
        require(hunter is None or args.hunter==hunter,'INVALID_INPUT: owning hunter cannot be overridden')
        root=args.root.resolve(strict=True);value=load(root,args.input)
        packet=value if args.command=='verify-handoff' else None
        inputs={bounded_path(root,args.input)}
        if packet is not None:
            require(args.report is not None,'INVALID_INPUT: --report required')
            inputs.add(bounded_path(root,args.report))
            value=load(root,args.report)
        if args.command=='prepare' and isinstance(value,list):
            for source in value:inputs.add(bounded_path(root,Path(source['path'])))
        if isinstance(value,dict):
            for source in value.get('sources',value.get('input',{}).get('sources',[])):
                inputs.add(bounded_path(root,Path(source['path'])))
        inputs.update(evidence_paths(root,value))
        if args.output:require(bounded_path(root,args.output) not in inputs,'INVALID_INPUT: output would overwrite evidence')
        if args.log:require(bounded_path(root,Path(args.log)) not in inputs and (not args.output or bounded_path(root,Path(args.log))!=bounded_path(root,args.output)),'INVALID_INPUT: log/output collision')
        if args.command=='prepare':output=prepare(root,args.hunter,args.scope,value)
        elif args.command=='reproduce':
            require(args.test and args.log and args.output,'INVALID_INPUT: reproduce needs --test --log --output')
            output=reproduce(root,value,args.test,args.log)
        else:
            candidate=value['input'] if value.get('schema')==REPORT else value
            require(candidate['hunter']==args.hunter,'SCHEMA_ERROR: owning hunter mismatch')
            output=evaluate(root,candidate)
            if args.command in {'verify','render','handoff','verify-handoff'}:require(value==output,'EVIDENCE_UNRESOLVED: report differs from current evaluation')
            if args.command in {'handoff','verify-handoff'}:
                prefix=HERE.parent.name[:-len('shared-runtime')]
                consumer=('requirements-review' if prefix=='ai-sdlc-loop-' else 'requirements-readiness-review') if args.hunter=='blind-case-hunter' else 'test-cases' if args.hunter=='edge-case-hunter' else 'code-review'
                output=dict(schema='ai-sdlc-hunter-handoff/v1',report_fingerprint=output['fingerprint'],source_snapshot=digest(candidate['sources']),findings=output['findings'],authorizes_execution=False,consumer=prefix+consumer)
                if packet is not None:require(packet==output,'EVIDENCE_UNRESOLVED: handoff differs from current producer report')
        body=render(skill_root,output) if args.command=='render' else encode_toon(output)
        if args.output:
            require(bounded_path(root,args.output)!=bounded_path(root,args.input),'INVALID_INPUT: output would overwrite input')
            atomic_write_text(root,args.output,body)
        else:print(body,end='')
        return 2 if output.get('execution')=='BLOCKED' else 0
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        print(encode_toon(dict(schema='ai-sdlc-hunter-error/v1',code=str(exc).split(':')[0],message=str(exc)[:500],status='BLOCKED')),end='')
        return 1

if __name__=='__main__':raise SystemExit(main())
