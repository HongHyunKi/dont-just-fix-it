#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
case "${1:-}" in
  --check)
    [[ $# == 1 ]] || { echo "Usage: $0 --check" >&2; exit 1; }
    git -C "$repo_dir" fetch origin main
    echo "새 커밋: $(git -C "$repo_dir" rev-list --count HEAD..origin/main)"
    exit 0 ;;
  ''|--claude-only|--codex-only) ;;
  *) echo "Usage: $0 [--check|--claude-only|--codex-only]" >&2; exit 1 ;;
esac
[[ $# -le 1 ]] || { echo "옵션은 하나만 지정하세요." >&2; exit 1; }
if [[ -n "$(git -C "$repo_dir" status --porcelain)" ]]; then
  echo "로컬 변경이 있습니다. 먼저 보존·정리한 뒤 업데이트하세요." >&2
  exit 1
fi
if [[ "$(git -C "$repo_dir" branch --show-current)" != main ]]; then
  echo "main 브랜치의 clone에서 실행하세요. 이전 태그 설치는 INSTALL.md의 전환 안내를 확인하세요." >&2
  exit 1
fi
git -C "$repo_dir" pull --ff-only origin main
exec "$repo_dir/install.sh" "$@"
