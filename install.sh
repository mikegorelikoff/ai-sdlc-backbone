#!/bin/sh

set -eu

usage() {
  printf '%s\n' \
    "Usage: install.sh AGENT" \
    "" \
    "Install every AI SDLC Harness skill into the current project for one agent." \
    "" \
    "Examples:" \
    "  ./install.sh codex" \
    "  curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/main/install.sh | sh -s -- claude-code" \
    "" \
    "Optional environment overrides:" \
    "  AI_SDLC_SOURCE              Harness source (default: mikegorelikoff/ai-sdlc-harness)" \
    "  AI_SDLC_SKILLS_CLI_VERSION Skills CLI version (default: 1.5.19)"
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

if ! command -v npx >/dev/null 2>&1; then
  printf '%s\n' "AI SDLC Harness installer requires Node.js and npx." >&2
  exit 127
fi

agent=$1
source_locator=${AI_SDLC_SOURCE:-mikegorelikoff/ai-sdlc-harness}
skills_cli_version=${AI_SDLC_SKILLS_CLI_VERSION:-1.5.19}

printf 'Installing AI SDLC Harness for agent "%s" from "%s"...\n' \
  "$agent" "$source_locator"

DISABLE_TELEMETRY=1
export DISABLE_TELEMETRY

exec npx -y "skills@$skills_cli_version" add \
  "$source_locator" --skill '*' --agent "$agent" -y
