#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
skill_dir="$repo_dir/skills/dont-just-fix-it"
install_home="${DJFI_HOME:-$HOME}"
mode=install
check_only=false
target=auto
for arg in "$@"; do
  case "$arg" in
    --claude-only|--codex-only)
      [[ "$target" == auto ]] || { echo "설치 대상 옵션은 하나만 지정하세요." >&2; exit 1; }
      target="${arg#--}"; target="${target%-only}" ;;
    --uninstall) mode=uninstall ;;
    --check) check_only=true ;;
    *) echo "Usage: $0 [--claude-only|--codex-only] [--uninstall|--check]" >&2; exit 1 ;;
  esac
done
if [[ "$check_only" == true && "$mode" == uninstall ]]; then
  echo "--check와 --uninstall은 함께 사용할 수 없습니다." >&2
  exit 1
fi

destinations=()
if [[ "$target" == claude ]] || { [[ "$target" == auto ]] && { [[ "$mode" == uninstall ]] || command -v claude >/dev/null; }; }; then
  destinations+=("$install_home/.claude/skills/dont-just-fix-it")
fi
if [[ "$target" == codex ]] || { [[ "$target" == auto ]] && { [[ "$mode" == uninstall ]] || command -v codex >/dev/null; }; }; then
  destinations+=("$install_home/.agents/skills/dont-just-fix-it")
fi
if [[ ${#destinations[@]} == 0 ]]; then
  echo "Claude Code 또는 Codex CLI를 찾지 못했습니다. --claude-only 또는 --codex-only로 대상을 지정하세요." >&2
  exit 1
fi

# 모든 충돌을 먼저 확인해 두 도구 중 하나만 설치되는 상황을 막는다.
if [[ "$mode" == install ]]; then
  [[ -f "$skill_dir/SKILL.md" ]] || { echo "스킬 파일이 없습니다: $skill_dir" >&2; exit 1; }
  for destination in "${destinations[@]}"; do
    if [[ -e "$destination" || -L "$destination" ]]; then
      if [[ ! -L "$destination" || "$(readlink "$destination")" != "$skill_dir" ]]; then
        echo "기존 경로를 보존합니다. 설치 중단: $destination" >&2
        exit 1
      fi
    fi
  done
fi

if [[ "$check_only" == true ]]; then
  echo "설치 사전 검사 통과"
  exit 0
fi

for destination in "${destinations[@]}"; do
  if [[ "$mode" == uninstall ]]; then
    if [[ -L "$destination" && "$(readlink "$destination")" == "$skill_dir" ]]; then
      unlink "$destination"
      echo "제거: $destination"
    elif [[ -e "$destination" || -L "$destination" ]]; then
      echo "이 저장소가 설치한 링크가 아니므로 유지: $destination"
    fi
  elif [[ ! -L "$destination" ]]; then
    mkdir -p "$(dirname "$destination")"
    ln -s "$skill_dir" "$destination"
    echo "설치: $destination"
  else
    echo "이미 설치됨: $destination"
  fi
done
