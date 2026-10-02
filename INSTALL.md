# 설치·업데이트·제거

Claude Code와 OpenAI Codex CLI를 지원합니다. Claude Code에서는 마켓플레이스 설치가 기본 안내이며, Codex 또는 두 도구를 함께 쓸 때는 clone + 전역 설치 스크립트를 사용할 수 있습니다. 같은 Claude 스킬을 두 방식으로 중복 설치할 필요는 없습니다.

## Claude Code 마켓플레이스

Claude Code 안에서 실행하세요.

```text
/plugin marketplace add HongHyunKi/dont-just-fix-it
/plugin install dont-just-fix-it@dont-just-fix-it
```

새 세션에서 다음 명령을 사용합니다.

```text
/dont-just-fix-it:dont-just-fix-it 이번 개선을 사례로 남겨줘.
```

터미널로 설치하려면 앞의 `/plugin` 대신 `claude plugin`을 사용합니다. 설치 여부는 터미널에서 `claude plugin list`와 `claude plugin details dont-just-fix-it`으로 확인할 수 있습니다.

업데이트:

```text
/plugin marketplace update dont-just-fix-it
/plugin update dont-just-fix-it@dont-just-fix-it
```

제거:

```text
/plugin uninstall dont-just-fix-it@dont-just-fix-it
/plugin marketplace remove dont-just-fix-it
```

플러그인의 설치·버전 관리는 Claude Code에 맡깁니다. 이 방식에서는 저장소의 `install.sh`나 `update.sh`를 실행하지 않습니다. 명령 이름에는 플러그인 접두사가 붙으며, 사용자가 호출할 때만 실행합니다. [Claude 공식 마켓플레이스 안내](https://code.claude.com/docs/en/plugin-marketplaces).

## clone + 전역 설치

Git, Bash, 사용할 도구의 CLI가 필요합니다. 스크립트는 macOS·Linux용이며 Windows 네이티브 설치는 검증하지 않았습니다.

```sh
git clone https://github.com/HongHyunKi/dont-just-fix-it.git
cd dont-just-fix-it
./install.sh
```

스크립트는 `PATH`에서 `claude`와 `codex`를 찾아 설치 대상을 결정합니다. 하나만 설치하거나 CLI를 나중에 설치할 예정이라면 대상을 지정하세요.

```sh
./install.sh --claude-only
./install.sh --codex-only
```

| 도구 | 사용자 전역 설치 위치 | 호출 |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/dont-just-fix-it` | `/dont-just-fix-it 이번 개선을 사례로 남겨줘.` |
| Codex CLI | `~/.agents/skills/dont-just-fix-it` | `$dont-just-fix-it 이번 개선을 사례로 남겨줘.` |

두 경로는 clone한 저장소의 `skills/dont-just-fix-it/`를 가리키는 심볼릭 링크입니다. 본문은 복제하지 않습니다. 설치 뒤 새 세션을 열고, Codex에서 목록에 보이지 않으면 재시작하세요. [Codex 공식 스킬 안내](https://learn.chatgpt.com/docs/build-skills).

이미 이 저장소를 가리키는 링크는 그대로 둡니다. 다른 파일·폴더·심볼릭 링크가 같은 경로에 있으면 덮어쓰지 않고 설치를 중단합니다. 먼저 기존 내용을 확인하고 별도로 옮기거나 제거하세요.

### 업데이트

clone한 저장소에서 실행합니다.

```sh
./update.sh --check     # fetch 후 받을 새 커밋 수 표시; 작업 파일은 변경하지 않음
./update.sh             # main을 fast-forward로 갱신하고 설치 링크 확인
./update.sh --codex-only
```

`main` 브랜치의 최신 코드를 받습니다. 미커밋·미추적 파일이 있거나 브랜치가 `main`이 아니면 중단합니다. 히스토리가 갈라졌을 때도 강제로 덮어쓰거나 병합하지 않습니다. 로컬 변경은 먼저 보존하고 사용자가 정리하세요.

코드를 받기 전에 설치 대상과 기존 경로 충돌을 검사합니다. `./install.sh --check`로 설치 사전 검사만 실행할 수도 있습니다. 코드 갱신과 설치 링크 확인 결과는 따로 표시합니다. 사전 검사 이후 파일 시스템 상태가 바뀌어 링크 확인에 실패하면 코드는 이미 갱신된 상태임을 알립니다.

### 제거와 저장소 이동

```sh
./uninstall.sh
./uninstall.sh --claude-only
./uninstall.sh --codex-only
```

현재 저장소를 가리키는 링크만 제거합니다. 다른 설치나 사용자 파일, clone한 저장소, 생성된 사례 문서는 지우지 않습니다. 저장소를 이동하거나 삭제하기 **전에** 제거하세요. 이동 후에는 새 위치에서 다시 설치합니다.

### 이전 프로젝트별 설치에서 전환

v0.1.x 안내로 프로젝트의 `.claude/skills/dont-just-fix-it` 또는 `.agents/skills/dont-just-fix-it`에 clone했다면, 그 폴더의 수정 내용을 먼저 확인하세요. 필요한 변경을 보관한 뒤 해당 프로젝트 설치를 제거하고 위 전역 설치를 사용하면 됩니다. 프로젝트별 설치와 전역 설치를 함께 두면 같은 이름이 중복으로 나타날 수 있습니다. 새 스크립트가 기존 프로젝트 설치를 자동 삭제하지는 않습니다.

## 동작과 검증 범위

스킬 본문은 두 도구가 공유합니다. Claude Code는 `disable-model-invocation: true`, Codex는 `agents/openai.yaml`의 `allow_implicit_invocation: false`로 요청 기반 호출을 유지합니다. claude.ai 업로드용 패키지나 Copilot·Gemini 지원을 주장하지 않습니다.

개발 중 설치 스크립트를 검증하려면 `python3 tests/install.py`를 실행하세요. 테스트는 임시 디렉터리와 로컬 Git 원격만 사용합니다. `DJFI_HOME`은 이 테스트에서 전역 설치 기준 경로를 바꾸기 위한 환경 변수이며, 보통 사용자는 설정할 필요가 없습니다. 실제 실행 결과와 한계는 [검증 기록](validation/README.md)에 있습니다.
