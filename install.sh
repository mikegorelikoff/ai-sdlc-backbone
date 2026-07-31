#!/bin/sh

set -eu

usage() {
  printf '%s\n' \
    "Usage: install.sh AGENT" \
    "" \
    "Install every AI SDLC Harness skill into the current project with TOON-only provenance." \
    "" \
    "Examples:" \
    "  ./install.sh codex" \
    "  curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.0.1/install.sh | sh -s -- codex" \
    "" \
    "Optional environment overrides:" \
    "  AI_SDLC_SOURCE               Clean local checkout or reviewed Git remote" \
    "  AI_SDLC_REVISION             Exact commit or tag (remote default: v4.0.1)" \
    "  AI_SDLC_PYTHON               Python 3.10+ executable (default: python3)" \
    "  AI_SDLC_INSTALL_REPLACE      Set to 1 only after reviewing managed differences"
}

case "${1-}" in
  -h|--help)
    if [ "$#" -eq 1 ]; then
      usage
      exit 0
    fi
    ;;
esac

if [ "$#" -ne 1 ] || [ -z "$1" ]; then
  usage >&2
  exit 64
fi

ai_sdlc_agent=$1
if [ "$ai_sdlc_agent" != "codex" ]; then
  printf '%s\n' "AI SDLC Harness v4 validates native project installation only for agent codex." >&2
  exit 65
fi

if ! command -v git >/dev/null 2>&1; then
  printf '%s\n' "AI SDLC Harness installer requires Git." >&2
  exit 127
fi

ai_sdlc_python=${AI_SDLC_PYTHON:-python3}
if ! command -v "$ai_sdlc_python" >/dev/null 2>&1; then
  printf '%s\n' "AI SDLC Harness installer requires Python 3.10 or newer." >&2
  exit 127
fi
if ! "$ai_sdlc_python" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  printf '%s\n' "AI SDLC Harness installer requires Python 3.10 or newer." >&2
  exit 65
fi

ai_sdlc_target=$(pwd -P)
ai_sdlc_temp=

cleanup() {
  if [ -n "$ai_sdlc_temp" ] && [ -d "$ai_sdlc_temp" ]; then
    rm -rf "$ai_sdlc_temp"
  fi
}
trap cleanup 0 HUP INT TERM

ai_sdlc_local=
case "$0" in
  install.sh|*/install.sh)
    ai_sdlc_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
    if [ -f "$ai_sdlc_script_dir/config/ai-sdlc-managed-skills.txt" ]; then
      ai_sdlc_local=$ai_sdlc_script_dir
    fi
    ;;
esac

if [ -n "${AI_SDLC_SOURCE:-}" ]; then
  if [ -d "$AI_SDLC_SOURCE" ]; then
    ai_sdlc_local=$(CDPATH= cd -- "$AI_SDLC_SOURCE" && pwd -P)
  else
    ai_sdlc_local=
  fi
fi

if [ -n "$ai_sdlc_local" ]; then
  ai_sdlc_source=$ai_sdlc_local
  ai_sdlc_head=$(git -C "$ai_sdlc_source" rev-parse --verify HEAD)
  if [ -n "${AI_SDLC_REVISION:-}" ]; then
    ai_sdlc_revision=$(git -C "$ai_sdlc_source" rev-parse --verify "$AI_SDLC_REVISION^{commit}")
    if [ "$ai_sdlc_revision" != "$ai_sdlc_head" ]; then
      printf '%s\n' "AI_SDLC_REVISION does not resolve to the local source HEAD." >&2
      exit 65
    fi
  else
    ai_sdlc_revision=$ai_sdlc_head
  fi
else
  ai_sdlc_locator=${AI_SDLC_SOURCE:-https://github.com/mikegorelikoff/ai-sdlc-harness.git}
  case "$ai_sdlc_locator" in
    /*|./*|../*|~/*)
      printf '%s\n' "AI_SDLC_SOURCE names a local path that does not exist." >&2
      exit 65
      ;;
    http://*|https://*|git://*|ssh://*|git@*)
      ai_sdlc_remote=$ai_sdlc_locator
      ;;
    */*)
      ai_sdlc_remote="https://github.com/$ai_sdlc_locator.git"
      ;;
    *)
      printf '%s\n' "AI_SDLC_SOURCE must be a local checkout or reviewed Git remote." >&2
      exit 65
      ;;
  esac
  ai_sdlc_requested_revision=${AI_SDLC_REVISION:-v4.0.1}
  case "$ai_sdlc_requested_revision" in
    *[!A-Za-z0-9._-]*|"")
      printf '%s\n' "AI_SDLC_REVISION contains unsupported characters." >&2
      exit 65
      ;;
  esac
  ai_sdlc_temp=$(mktemp -d /tmp/ai-sdlc-harness.XXXXXX)
  ai_sdlc_source=$ai_sdlc_temp/source
  git init "$ai_sdlc_source"
  git -C "$ai_sdlc_source" remote add origin "$ai_sdlc_remote"
  if [ "${#ai_sdlc_requested_revision}" -eq 40 ]; then
    case "$ai_sdlc_requested_revision" in
      *[!0-9a-f]*)
        printf '%s\n' "A 40-character AI_SDLC_REVISION must be a lowercase Git SHA." >&2
        exit 65
        ;;
    esac
    git -C "$ai_sdlc_source" fetch --depth 1 origin "$ai_sdlc_requested_revision"
    git -C "$ai_sdlc_source" checkout --detach FETCH_HEAD
  else
    git -C "$ai_sdlc_source" fetch --depth 1 origin \
      "refs/tags/$ai_sdlc_requested_revision:refs/tags/$ai_sdlc_requested_revision"
    ai_sdlc_tag_type=$(git -C "$ai_sdlc_source" cat-file -t "$ai_sdlc_requested_revision")
    if [ "$ai_sdlc_tag_type" != "tag" ]; then
      printf '%s\n' "AI_SDLC_REVISION must name an annotated release tag." >&2
      exit 65
    fi
    git -C "$ai_sdlc_source" checkout --detach "$ai_sdlc_requested_revision^{commit}"
  fi
  ai_sdlc_revision=$(git -C "$ai_sdlc_source" rev-parse --verify HEAD)
  if [ "${#ai_sdlc_requested_revision}" -ne 40 ]; then
    ai_sdlc_tag_revision=$(git -C "$ai_sdlc_source" rev-list -n 1 "$ai_sdlc_requested_revision")
    if [ "$ai_sdlc_tag_revision" != "$ai_sdlc_revision" ]; then
      printf '%s\n' "Release tag does not resolve to the checked-out source revision." >&2
      exit 65
    fi
  fi
fi

printf 'Installing AI SDLC Harness for agent "%s" from revision "%s"...\n' \
  "$ai_sdlc_agent" "$ai_sdlc_revision"

set -- \
  "$ai_sdlc_source/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install.py" \
  --source "$ai_sdlc_source" \
  --root "$ai_sdlc_target" \
  --revision "$ai_sdlc_revision" \
  --agent "$ai_sdlc_agent"
if [ "${AI_SDLC_INSTALL_REPLACE:-0}" = "1" ]; then
  set -- "$@" --replace-reviewed
fi
"$ai_sdlc_python" -B "$@"
