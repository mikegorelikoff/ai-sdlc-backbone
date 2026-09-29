#!/usr/bin/env python3
"""Render and check skill-specific chat tables; native artifacts keep their format.

No command execution, source discovery, readiness changes or authority grants.
Input facts must already be verified by the owning skill.
"""
from __future__ import annotations
import argparse
import html
import re
import sys
from ai_sdlc_toon import encode_toon
from pathlib import Path

STATUSES = ('PASS', 'FAIL', 'WARNING', 'BLOCKED', 'PENDING', 'N/A')
MAX_BYTES = 256_000
SUMMARY = ['Status', 'Decision', 'Evidence']
ACTIONS = ['Owner', 'Next action', 'Expected evidence']
SCENARIOS = ('happy', 'partial', 'warning', 'blocked', 'missing-input', 'large', 'small', 'edge')


def read(path: Path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError('INVALID_INPUT: regular bounded file required')
    raw = path.read_text(encoding='utf-8')
    from ai_sdlc_toon import decode_toon
    return decode_toon(raw)


def contract(root: Path):
    if root.is_symlink() or not root.is_dir():
        raise ValueError('INVALID_INPUT: regular skill directory required')
    root = root.resolve()
    candidates = [root / ('references/chat-output'+suffix) for suffix in ('.toon',)]
    present = [p for p in candidates if p.exists()]
    if len(present) != 1:
        raise ValueError('WRONG_SCHEMA: exactly one native chat contract required')
    path = present[0]
    if path.parent.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError('INVALID_INPUT: unsafe contract path')
    c = read(path)
    if not isinstance(c, dict) or c.get('schema') != 'ai-sdlc-chat-contract/v1' or c.get('skill') != root.name:
        raise ValueError('WRONG_SCHEMA: contract identity mismatch')
    for key in ('primary', 'failure', 'clarification', 'secondary'):
        if key == 'secondary' and c.get(key) == []:continue
        columns = c.get(key)
        if not isinstance(columns, list) or not 2 <= len(columns) <= 6 or len(set(columns)) != len(columns):
            raise ValueError('WRONG_SCHEMA: invalid '+key+' columns')
    for columns in [c['primary'], c['failure'], c['clarification'], c.get('secondary', [])]:
        if len(columns) > 6 or any(not isinstance(x, str) or not x.strip() or any(t in x for t in ('|', '\n')) for x in columns):
            raise ValueError('WRONG_SCHEMA: invalid column name')
    return c


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('MISSING_INFORMATION: nonempty text required')
    if len(value) > 180:
        raise ValueError('LONG_CELLS: shorten the fact; link native evidence')
    return value


def cell(value):
    value = text(value)
    # Escape markup inside cells; evidence paths stay readable and cannot create rows.
    return html.escape(value, quote=False).replace('|', '&#124;').replace('\r\n', '<br>').replace('\n', '<br>').replace('\r', '<br>')


def table(columns, rows):
    return '\n'.join(['| '+' | '.join(columns)+' |', '| '+' | '.join('---' for _ in columns)+' |'] +
                     ['| '+' | '.join(cell(row[col]) for col in columns)+' |' for row in rows])


def validate_input(c, value):
    if not isinstance(value, dict) or value.get('schema') != 'ai-sdlc-chat-result/v1':
        raise ValueError('WRONG_SCHEMA: expected ai-sdlc-chat-result/v1')
    allowed = {'schema', 'summary', 'primary', 'secondary', 'failures', 'clarifications', 'actions', 'native', 'full_artifact'}
    if set(value)-allowed:
        raise ValueError('WRONG_SCHEMA: unknown result fields')
    if not isinstance(value.get('summary'), dict) or set(value['summary']) != set(SUMMARY):
        raise ValueError('MISSING_INFORMATION: summary decision and evidence required')
    if value['summary']['Status'] not in STATUSES:
        raise ValueError('UNCLEAR_STATUS: unsupported summary status')
    for v in value['summary'].values(): text(v)
    for key, cols in [('primary', c['primary']), ('secondary', c.get('secondary', [])), ('failures', c['failure']), ('clarifications', c['clarification']), ('actions', ACTIONS)]:
        rows = value.get(key, [])
        if not isinstance(rows, list) or len(rows) > 500:
            raise ValueError('INVALID_INPUT: rows must be a bounded list')
        if rows and not cols:
            raise ValueError('WRONG_SCHEMA: undeclared secondary table')
        seen = set()
        for row in rows:
            if not isinstance(row, dict) or set(row) != set(cols):
                raise ValueError('MISSING_INFORMATION: '+key+' columns must match contract')
            for k,v in row.items():
                text(v)
                if k == 'Severity' and v not in ('CRITICAL','HIGH','MEDIUM','LOW','N/A'):
                    raise ValueError('UNCLEAR_STATUS: invalid severity')
                if 'status' in k.lower() and k not in ('Decision status',) and v not in STATUSES:
                    raise ValueError('UNCLEAR_STATUS: '+k)
            identity = tuple(row[k] for k in cols)
            if identity in seen:
                raise ValueError('DUPLICATED_INFORMATION: duplicate row')
            seen.add(identity)
        if len(rows) > 8 and not value.get('full_artifact'):
            raise ValueError('MISSING_INFORMATION: large results require full_artifact')
    if value.get('full_artifact'): text(value['full_artifact'])
    if value['summary']['Status'] in ('FAIL','BLOCKED') and not value.get('failures'):
        raise ValueError('BAD_FAILURE_FORMAT: blocked or failed result needs a blocker row')
    if (value.get('failures') or value.get('clarifications')) and not value.get('actions'):
        raise ValueError('UNCLEAR_ACTION: failure or question needs owned next action')
    if value.get('failures') and value['summary']['Status'] == 'PASS':
        raise ValueError('UNCLEAR_STATUS: failures cannot accompany PASS')
    for block in value.get('native', []):
        if not isinstance(block, dict) or set(block) != {'language','content'} or not re.fullmatch(r'[a-zA-Z0-9_-]{0,20}',block['language']):
            raise ValueError('INVALID_INPUT: native block schema')
        if not isinstance(block['content'],str) or len(block['content'].encode()) > 32_000:
            raise ValueError('INVALID_INPUT: native block exceeds budget')


def render(c, value):
    validate_input(c, value)
    chunks = [table(SUMMARY, [value['summary']])]
    for key,cols in [('failures',c['failure']), ('clarifications',c['clarification']), ('primary',c['primary']), ('secondary',c.get('secondary',[])), ('actions',ACTIONS)]:
        rows = value.get(key, [])
        if not rows: continue
        # Preserve producer order: severity and dependency order are semantic facts.
        chunks.append(table(cols, rows[:8]))
        if len(rows) > 8:
            chunks.append(table(['Shown', 'Total', 'Full evidence'], [{'Shown':'8', 'Total':str(len(rows)), 'Full evidence':value['full_artifact']}]))
    for block in value.get('native',[]):
        fence = '`' * max(3, 1+max([len(m[0]) for m in re.finditer(r'`+',block['content'])]+[0]))
        chunks.append(fence+block['language']+'\n'+block['content']+'\n'+fence)
    return '\n\n'.join(chunks)+'\n'


def parse_tables(response):
    tables, prose, native = [], [], []
    lines=response.splitlines(); i=0; fence=None
    while i<len(lines):
        line=lines[i].strip()
        if line.startswith('```'):
            fence=re.match(r'`+',line)[0]; block=[];i+=1
            while i<len(lines) and lines[i].strip()!=fence:
                block.append(lines[i]);i+=1
            if i==len(lines): raise ValueError('WRONG_SCHEMA: unclosed native block')
            native.append('\n'.join(block));i+=1;continue
        if not line: i+=1;continue
        if line.startswith('|') and line.endswith('|'):
            columns=[html.unescape(x.strip()) for x in line[1:-1].split('|')]
            if i+1>=len(lines): raise ValueError('WRONG_SCHEMA: missing table delimiter')
            delim=lines[i+1].strip()
            parts=delim[1:-1].split('|') if delim.startswith('|') and delim.endswith('|') else []
            if len(parts)!=len(columns) or not all(re.fullmatch(r'\s*:?-{3,}:?\s*',x) for x in parts):
                raise ValueError('WRONG_SCHEMA: malformed table delimiter')
            rows=[];i+=2
            while i<len(lines) and lines[i].strip().startswith('|'):
                raw=lines[i].strip()
                if not raw.endswith('|'): raise ValueError('WRONG_SCHEMA: unclosed row')
                cells=[html.unescape(x.strip().replace('<br>','\n')) for x in raw[1:-1].split('|')]
                if len(cells)!=len(columns):raise ValueError('WRONG_SCHEMA: uneven row')
                rows.append(cells);i+=1
            tables.append((columns,rows));continue
        prose.append(line);i+=1
    return tables,prose,native


def evaluate(c, response, *, required_facts=(), expected_status=None):
    failures=[]
    def fail(code, detail):
        if not any(x['code']==code and x['evidence']==detail for x in failures):
            failures.append({'code':code,'evidence':detail,'recommended_action':'Repair this criterion using the local chat contract'})
    if not isinstance(response,str) or len(response.encode('utf-8'))>MAX_BYTES:
        return {'status':'FAIL','failures':[{'code':'TOO_VERBOSE','evidence':'Response byte budget exceeded','recommended_action':'Use bounded table previews'}]}
    if not response.lstrip().startswith('|'):fail('NON_TABULAR','First visible block is not a table')
    try: tables,prose,native=parse_tables(response)
    except ValueError as e:
        fail(str(e).split(':')[0],str(e));tables=[];prose=[];native=[]
    known=[SUMMARY,c['primary'],c['failure'],c['clarification'],ACTIONS,['Shown','Total','Full evidence']]
    if c.get('secondary'):known.append(c['secondary'])
    if not tables:fail('NON_TABULAR','No real Markdown table outside native blocks')
    if tables and tables[0][0]!=SUMMARY:fail('WRONG_SCHEMA','Summary must expose status, decision and evidence')
    schemas=[]
    for cols,rows in tables:
        if cols not in known:fail('WRONG_SCHEMA','Unexpected columns: '+', '.join(cols))
        if len(cols)>6:fail('TOO_WIDE','More than six columns')
        if len(rows)>8:fail('TOO_VERBOSE','More than eight preview rows')
        if cols in schemas and cols != ['Shown','Total','Full evidence']:fail('DUPLICATED_INFORMATION','Repeated table schema')
        schemas.append(cols)
        if not rows:fail('MISSING_INFORMATION','Empty table should be omitted with an explicit summary')
        if len({tuple(r) for r in rows})!=len(rows):fail('DUPLICATED_INFORMATION','Duplicate table rows')
        for row in rows:
            for col,v in zip(cols,row):
                if not v:fail('MISSING_INFORMATION','Empty '+col)
                if len(v)>180:fail('LONG_CELLS',col+' exceeds 180 characters')
                if col == 'Severity' and v not in ('CRITICAL','HIGH','MEDIUM','LOW','N/A'):fail('UNCLEAR_STATUS','Unknown severity: '+v)
                if 'status' in col.lower() and col!='Decision status' and v not in STATUSES:fail('UNCLEAR_STATUS','Unknown '+col+': '+v)
    if c['clarification'] in schemas and not any(cols == c['clarification'] and rows for cols, rows in tables):
        fail('BAD_CLARIFICATION_FORMAT','Empty clarification')
    if prose:fail('TOO_VERBOSE','Prose outside tables/native blocks: '+' '.join(prose)[:100])
    visible='\n'.join(' '.join(row) for cols,rows in tables for row in rows)
    for fact in required_facts:
        if fact not in visible and not any(fact in block for block in native):fail('MISSING_INFORMATION','Required fact absent: '+fact[:100])
    if tables and tables[0][0]==SUMMARY and tables[0][1]:
        status=tables[0][1][0][0]
        if len(tables[0][1]) != 1:fail('UNCLEAR_STATUS','Exactly one summary decision required')
        if status == 'PASS' and c['failure'] in schemas:fail('UNCLEAR_STATUS','Failure table contradicts PASS')
        if expected_status and status!=expected_status:fail('UNCLEAR_STATUS','Summary disagrees with source result')
        if status in ('FAIL','BLOCKED') and c['failure'] not in schemas:fail('BAD_FAILURE_FORMAT','Missing domain failure table')
    if (c['failure'] in schemas or c['clarification'] in schemas) and ACTIONS not in schemas:fail('UNCLEAR_ACTION','Missing owned next action')
    return {'status':'FAIL' if failures else 'PASS','failures':failures}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['render','check'])
    p.add_argument('--skill-root',type=Path,required=True)
    p.add_argument('--input',type=Path)
    p.add_argument('--response',type=Path)
    a=p.parse_args()
    try:
        c=contract(a.skill_root)
        if a.command=='render':
            if not a.input:raise ValueError('MISSING_INPUT: --input required')
            sys.stdout.write(render(c,read(a.input)));return 0
        if not a.response or not a.response.is_file() or a.response.stat().st_size>MAX_BYTES:
            raise ValueError('MISSING_INPUT: bounded --response required')
        result=evaluate(c,a.response.read_text(encoding='utf-8'))
        sys.stdout.write(encode_toon(result));return int(result['status']!='PASS')
    except (ValueError,KeyError,TypeError,OSError) as e:
        print(encode_toon({'status':'FAIL','failures':[{'code':str(e).split(':')[0],'evidence':str(e),'recommended_action':'Correct input; no readiness was changed'}]}),file=sys.stderr)
        return 1

if __name__=='__main__':raise SystemExit(main())
