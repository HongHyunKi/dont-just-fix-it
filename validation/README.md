# 검증 기록

2026-10-01에 별도 임시 프로젝트 세 개에서 스킬을 읽은 독립 에이전트가 요청을 수행했습니다. 아래 문서는 사람이 작성한 예상 답안이 아니라 실제 실행 결과입니다. 배치·UX 프로젝트는 검증용 합성 입력이며 제품 개선 성과로 홍보하지 않습니다.

## 실행 결과

| 상황 | 전달한 요청 | 확인한 결과 |
| --- | --- | --- |
| 새 성능 측정 | before.py와 after.py를 benchmark.py로 비교해 사례 작성 | 5회 측정, 중앙값·추가 메모리·합성 입력의 한계 기록 |
| 수치 없는 UX 개선 | before.html과 after.html을 비교하고 전후 화면 기록 | 두 뷰포트에서 캡처 4장, 키보드·가로 넘침 검사. 전환율이나 이해도 수치를 만들지 않음 |
| 기존 자료만 정리 | notes.md와 measurements.json으로 작성, 새 측정·앱 실행 금지 | baseline/verified를 비교하고 악화된 TBT 포함. 소스 부재와 미실행 검사를 명시 |

- [배치 조회 사례](performance/docs/issue/01-batch-id-lookup.md) · [측정 JSON](performance/docs/issue/assets/batch-id-lookup/benchmark.json)
- [UX 문구 사례](ux/docs/issue/01-profile-save-copy.md) · [캡처·검사 기록](ux/docs/issue/assets/profile-save-copy/evidence.json)
- [기존 자료 사례](existing/docs/issue/01-home-loading.md)

각 입력과 출력은 이 디렉터리에 보존했습니다. 기존 자료 입력은 루트 evidence의 모바일 Lighthouse 기록과 동일합니다. 기본 사례 구조, 근거 링크, 실제 수치와 계산, 수행하지 않은 검사의 표시를 검토했습니다. 원본 소스와 스킬은 평가 실행 중 수정하지 않았습니다.

UX 실행에서 생성한 캡처 스크립트는 처음에 개인 Playwright 설치 경로를 포함했습니다. 일반 모듈 import로 바꾸고 가로 넘침 assertion을 추가한 뒤 재실행했습니다. 스킬에도 재현 스크립트에서 개인 경로를 하드코딩하지 않도록 보완했습니다. UX 최종 문서·스크립트·이미지는 이 수정 이후 결과입니다.

## 재실행

성능 입력은 Python 표준 라이브러리만 사용합니다. 저장된 결과를 덮어쓰지 않도록 새 출력을 별도 파일로 받으세요. 새 숫자가 달라도 실패가 아니며, 동일 결과 assertion이 실패하면 구현을 확인해야 합니다.

```sh
cd validation/performance
PYTHONDONTWRITEBYTECODE=1 python3 benchmark.py
```

UX 캡처는 Node.js와 Playwright 1.62.1, 해당 Chromium이 필요합니다. 이 도구는 스킬 설치 의존성이 아니라 이 검증 입력의 재현 도구입니다. 기존 모듈을 사용한다면 `NODE_PATH`에 그 `node_modules` 디렉터리를 지정하세요. 스크립트 실행은 저장된 캡처·증거 파일을 갱신하므로 복사본에서 수행하세요.

```sh
cd validation/ux
node docs/issue/assets/profile-save-copy/capture.cjs
```

기존 자료 요청은 `validation/existing`에서 스킬을 호출해 재현할 수 있습니다. 앱 실행과 새 측정은 금지하고 문서만 별도 경로에 작성하도록 요청하세요.

## 설치·호출 확인

Codex CLI 0.156.1에서 `.agents/skills/dont-just-fix-it/`를 스캔했습니다. `skills/list`가 스킬을 `repo` 범위, `enabled: true`로 반환했고 해당 스킬 파싱 오류는 없었습니다. `agents/openai.yaml`의 명시적 호출 정책도 포함해 설치합니다.

같은 CLI에서 `$dont-just-fix-it`을 사용한 읽기 전용 설치 확인 요청도 정상 종료했습니다. 응답은 사례 문서화 역할과 요청 기반 실행을 설명했고 새 문서나 측정을 수행하지 않았습니다.

명시적 호출의 정책 의미는 [공식 문서](https://learn.chatgpt.com/docs/build-skills)에 근거합니다. 독립 에이전트 실행은 스킬 경로를 제공한 동작 검증이며, 모든 에이전트 제품의 자동 발견을 검증한 것은 아닙니다.

## 한계

- 한 환경에서 각 상황을 한 번씩 수행한 정성 검증입니다. 모델별 성공률이나 반복 실행의 일관성을 입증하지 않습니다.
- 배치 조회는 동일 프로세스에서 5회 비교했지만 머신 전체 부하는 격리하지 않았습니다. 다른 검증 작업이 같은 머신에서 진행됐으므로 정밀 성능 벤치마크로 해석하지 않습니다.
- UX 화면에는 저장 기능이 없습니다. 버튼 문구와 배치·키보드 동작을 확인했으며 실제 저장 성공이나 사용자 이해도는 검증하지 않았습니다.
- 기존 자료 테스트에는 소스와 전체 Lighthouse 보고서가 없습니다. 측정 JSON 계산과 기록의 정직성을 확인했습니다.
- v0.1.0에서는 Codex 이외 에이전트의 설치·호출, 실제 API 서버와 CI 환경은 검증하지 않았습니다. Claude Code 후속 검증은 아래에 기록했습니다.

## v0.1.1 — Claude Code 지원

2026-10-01, Claude Code 2.1.283에서 임시 프로젝트의 `.claude/skills/dont-just-fix-it/SKILL.md`를 설치했습니다. 실행 시작 이벤트의 명령 목록에 `dont-just-fix-it`이 포함됐고, 아래 요청을 `claude -p`로 명시적으로 호출했습니다.

```text
/dont-just-fix-it notes.md와 measurements.json의 기존 자료로 docs/issue/01-home-loading.md에 개선 사례를 작성해줘. 새 측정·앱 실행·코드 변경·커밋은 하지 마. 제공된 자료만 사용해줘.
```

읽기·쓰기·검색 도구만 제공하고 외부 MCP를 연결하지 않았습니다. 기존 자료는 [v0.1.0 입력](existing/)과 동일합니다. 실행이 정상 종료됐고 권한 거절은 없었습니다. 도구 기록에서는 입력 읽기와 결과 문서 쓰기를 확인했으며, 새 측정·앱 실행 없이 원본 입력을 보존했습니다.

첫 실행에서는 `optimized` 단계에 특정 회귀가 남아 있었다고 단정했습니다. 입력 기록은 회귀 발생과 최종 `verified` 상태만 설명했으므로 그 단계까지 단정할 근거는 부족했습니다. 단계명·수치만으로 구현이나 버그를 추정하지 않도록 지침 한 줄을 추가하고 새 프로젝트에서 같은 요청을 다시 실행했습니다. [재실행 결과 문서](claude-code-case.md)는 단계별 구현의 미확인 상태를 밝히며, `verified`를 최종 비교 기준으로 사용하고 TBT 증가도 기록했습니다. 공개 사본은 입력 링크만 이 저장소에 맞췄습니다.

Claude Code의 `disable-model-invocation: true`와 Codex의 `allow_implicit_invocation: false`를 함께 유지합니다. Claude Code 설정을 포함한 동일 `SKILL.md`가 Codex CLI 0.156.1의 `skills/list`에서도 오류 없이 인식되는지 확인했습니다.

표준 필드만 허용하는 `quick_validate.py`는 Claude Code 확장 필드인 `disable-model-invocation`을 거절합니다. 배포 파일에서 이 필드를 제거하지 않았습니다. YAML boolean 값을 별도로 검사하고, 임시 사본에서 확장 필드만 제외해 공통 필드·본문 검사를 통과시켰으며 두 호스트의 실제 인식으로 호환성을 확인했습니다. claude.ai 업로드용 패키지 호환성은 주장하지 않습니다.

이 검증은 기존 자료를 문서화하는 한 상황을 수정 전후로 실행한 것입니다. Claude Code의 새 성능 측정·브라우저 캡처 수행이나 반복 성공률은 검증하지 않았습니다.
