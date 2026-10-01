# dont-just-fix-it

**고치는 데서 끝내지 말고, 사례로 남기세요.**

좋은 개선을 했는데, 나중에 설명하려니 기억이 안 나나요? 이 스킬은 요청 한 번으로 작업 맥락·코드·측정 자료를 모아 **문제 → 원인 → 해결 → 결과**가 담긴 기술 사례를 작성합니다.

| 도구 | 요청 |
| --- | --- |
| Codex | `$dont-just-fix-it 이번 개선을 사례로 남겨줘.` |
| Claude Code (스크립트 설치) | `/dont-just-fix-it 이번 개선을 사례로 남겨줘.` |
| Claude Code (마켓플레이스) | `/dont-just-fix-it:dont-just-fix-it 이번 개선을 사례로 남겨줘.` |

## 이렇게 남습니다

아래는 실제 기록을 줄인 예시입니다. [코드 비교·측정 조건·스크린샷이 포함된 전체 사례](examples/tech-icon-html-weight.md)도 볼 수 있습니다.

> **문제**— 홈 HTML 전송량이 45.1KiB로 페이지 규모에 비해 컸습니다.
>
> **원인**— 기술 아이콘의 SVG path가 HTML과 RSC 페이로드에 중복으로 실렸습니다.
>
> **해결**— 아이콘을 별도 SVG 파일로 옮기고 CSS mask로 표시했습니다.
>
> **결과**— HTML 전송량이 18.4KiB로 약 59% 줄었습니다. 모바일 성능 중앙값은 88 → 90점으로 바뀌었습니다. 대신 아이콘 요청 16개와 이미지 전송량 약 20.4KiB가 추가됐습니다.

기본 결과물은 다음과 같습니다. 프로젝트에 기존 문서 규칙이 있으면 그 규칙을 따릅니다.

```text
docs/issue/
├── 01-<개선-사례>.md
└── assets/<개선-사례>/
    └── 측정 자료·전후 화면 등 실제 확보한 근거
```

개발을 끝낸 뒤 대화를 다시 훑고 글을 처음부터 쓰는 부담을 줄입니다. 남긴 자료는 팀 기록, 기술 블로그, 포트폴리오에 활용할 수 있습니다.

## 설치 (Install)

**Claude Code · OpenAI Codex CLI**를 지원합니다. 전체 가이드: [INSTALL.md](INSTALL.md).

### Claude Code — 플러그인 마켓플레이스 (권장)

Claude Code 안에서 실행합니다. 직접 clone할 필요가 없습니다.

```text
/plugin marketplace add HongHyunKi/dont-just-fix-it
/plugin install dont-just-fix-it@dont-just-fix-it
```

새 세션에서 호출합니다. 플러그인 설치는 이름 충돌을 피하기 위해 접두사가 붙습니다.

```text
/dont-just-fix-it:dont-just-fix-it 이번 개선을 사례로 남겨줘.
```

### Claude Code · Codex CLI — clone + 전역 설치

터미널에서 한 번 설치하면 여러 프로젝트에서 사용할 수 있습니다.

```sh
git clone https://github.com/HongHyunKi/dont-just-fix-it.git
cd dont-just-fix-it
./install.sh
```

- 설치된 CLI를 감지해 Claude는 `~/.claude/skills/`, Codex는 `~/.agents/skills/`에 연결합니다.
- 호출: Claude `/dont-just-fix-it` · Codex `$dont-just-fix-it`
- 한쪽만 설치: `./install.sh --claude-only` / `./install.sh --codex-only`
- 업데이트: `./update.sh` · 확인만: `./update.sh --check` · 제거: `./uninstall.sh`

스크립트 설치는 macOS·Linux의 Bash 환경을 대상으로 합니다. 심볼릭 링크를 사용하므로 clone한 폴더를 유지하세요. 마켓플레이스와 스크립트 중 Claude 설치 방식은 하나를 선택하세요.

## 요청 예시

아래 예시는 Codex 문법입니다. Claude Code에서는 스크립트 설치 시 `/dont-just-fix-it`, 마켓플레이스 설치 시 `/dont-just-fix-it:dont-just-fix-it`으로 바꿔 호출하세요.

작업하던 대화에서 호출하면 그 맥락을 사용합니다. 새 대화에서는 변경 커밋·파일·기존 기록을 알려주세요.

| 상황 | 요청 |
| --- | --- |
| 방금 끝낸 개선 | `$dont-just-fix-it 이번 개선을 사례로 남겨줘.` |
| 성능 전후 비교 | `$dont-just-fix-it 변경 전은 <커밋>, 변경 후는 현재 코드야. 배치 실행 시간을 비교해서 기록해줘.` |
| 수치 없는 UX 개선 | `$dont-just-fix-it 이 버튼 문구 변경을 전후 화면과 함께 기록해줘.` |
| 기존 자료 정리 | `$dont-just-fix-it 이 측정 JSON과 작업 기록으로 사례를 작성해줘. 새 측정은 하지 마.` |

기존 증거가 충분하면 재측정하지 않습니다. 새 측정이 필요한 경우 프로젝트의 도구와 사용자가 허용한 범위에서 수행합니다. 근거가 없으면 숫자를 만들지 않고 확인하지 못한 부분을 적습니다. 문서화 요청만으로 커밋·푸시하지 않습니다.

## 실제 기록에서 확인할 수 있는 것

이 스킬의 원형을 사용한 `dev-portfolio` 사례입니다. 아래 수치는 코드 변경의 결과이며 **스킬 자체의 성능 개선 효과를 뜻하지 않습니다.**

| 기록 | 결과와 함께 남긴 판단 | 자료 |
| --- | --- | --- |
| 한글 폰트·첫 화면 개선 | 성능 65 → 87점, LCP 7.97 → 3.84초. 중간 최고 94점 대신 회귀 수정 후 최종값을 사용했고, TBT 82.5 → 87.5ms 증가도 기록 | [30회 기록](evidence/mobile-lighthouse.json) |
| CSS 인라인 실험 | FCP 1.66 → 1.35초였지만 LCP 개선은 약 0.07초. HTML이 45.1 → 96.0KiB로 늘어 적용 보류 | [9회 기록](evidence/mobile-lcp-analysis.json) |
| 기술 아이콘 분리 | HTML 약 59% 감소와 추가 이미지 요청 비용을 함께 기록 | [전체 사례](examples/tech-icon-html-weight.md) · [6회 기록](evidence/tech-icon-html-weight.json) |

각 단계 3회 측정의 지표별 중앙값입니다. 로컬 프로덕션 빌드, Lighthouse 13.5.0 모바일 시뮬레이션(CPU 4배, RTT 150ms, 1,638.4Kbps)이며 실사용자 통계가 아닙니다. 누적 실험의 단계별 차이는 독립 효과로 더할 수 없습니다.

JSON은 기존 보고서에서 추출한 기록입니다. 내부의 `reports/...` 경로는 원래 프로젝트의 위치이며 전체 Lighthouse 보고서는 이 저장소에 포함하지 않습니다. 출처는 `HongHyunKi/dev-portfolio`의 `docs/issue/03`·`04`·`05` 문서입니다.

## 지원 범위와 검증

프론트엔드, API, 배치, CI 등 코드 개선을 기록하는 공통 구조입니다. 필요한 근거는 분야에 따라 달라집니다. 브라우저 측정에는 별도의 브라우저 자동화 도구나 Lighthouse 등이 필요합니다.

Codex와 Claude Code의 명시적 호출, 전역 설치 스크립트와 Claude Code 마켓플레이스 설치를 검증했습니다. Claude Code에서는 기존 측정 자료로 사례를 작성하는 실행도 확인했습니다. 다른 에이전트는 아직 검증하지 않았습니다. 공개 사례는 Next.js 프로젝트에서 나왔으며, 릴리스 검증에서는 별도의 배치 조회·UX 문구·기존 자료 프로젝트를 사용했습니다. [검증 결과와 한계](validation/README.md)를 확인하세요.

## 기여와 라이선스

실제 사용 중 잘못된 비교나 누락된 근거를 발견하면 요청·환경·기대한 기록과 실제 결과를 이슈로 알려주세요. 민감한 코드와 자료는 제거해 주세요.

[MIT](LICENSE)
