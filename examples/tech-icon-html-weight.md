# 기술 칩 아이콘을 HTML에서 분리해 모바일 LCP 개선 (`개인 portfolio 프로젝트`)

- **Skills & Libraries**: Next.js 16.3.4, React Server Components, CSS Masking, Lighthouse 13.5.0, Playwright
- **작업 일자**: 2026.10.01
- **대상**: 홈 `/`의 Tech Stack 섹션과 모든 기술 칩(`TechChip`)

**홈 HTML 전송량 59% 감소**

- **문제**— 앞선 LCP 원인 분석에서 모바일 LCP 3.84초가 첫 페인트 전 전송량에 묶여 있다는 것을 확인했습니다. 그런데 그중 가장 먼저, 가장 높은 우선순위로 받는 홈 HTML이 gzip 기준 45.1KiB로 페이지 규모에 비해 컸습니다.
- **원인**— HTML을 분해해 보니 기술 칩의 브랜드 아이콘이 원인이었습니다. `TechChip`은 아이콘 path 문자열을 `<svg><path d="…"/></svg>`로 직접 그렸습니다. 서버 컴포넌트로 렌더링한 path는 HTML 마크업에 한 번, 하이드레이션용 RSC 페이로드에 한 번 더 실립니다. 좌표 숫자로 된 문자열이라 gzip으로도 거의 줄지 않아, 아이콘 path만 빼면 HTML gzip이 44.6KiB → 17.9KiB로 줄어드는 것을 빌드 결과물에서 확인했습니다. 화면 아래쪽 장식 아이콘이 첫 페인트 전 전송량의 HTML 몫을 절반 넘게 차지하고 있었습니다.
- **해결**— path 34개를 `public/tech-icons/<이름>.svg` 파일로 옮기고, `techIcons`는 기술명 → 파일명 매핑만 갖도록 바꿨습니다. 칩은 아이콘 자리에 빈 `span`을 두고 CSS `mask`로 SVG를 씌운 뒤 `bg-current`로 칠합니다. 그래서 다크·라이트 테마에서 글자색을 따라가는 기존 동작과 크기(`1em`)·투명도(`opacity-80`)를 그대로 유지했습니다. 아이콘을 추가할 때도 simple-icons의 SVG 파일을 폴더에 넣고 매핑 한 줄만 적으면 되도록 단순해졌습니다.
- **결과**— 같은 조건 3회 중앙값 기준으로 홈 HTML 전송량은 45.1KiB → 18.4KiB(-59%), LCP는 3.84초 → 3.64초(-0.19초), FCP는 1.66초 → 1.50초로 줄었습니다. 모바일 성능 점수 중앙값은 88점 → 90점이 됐습니다. 대신 아이콘 SVG 16개(20.4KiB)가 낮은 우선순위의 이미지 요청으로 추가됐고, 이 파일들은 다른 페이지에서 재사용되도록 캐시됩니다. LCP 2.5초 목표에는 여전히 도달하지 못했습니다.

<details>
<summary>칩 아이콘 렌더링 비교</summary>

```tsx
// 변경 전 — path 문자열이 HTML과 RSC 페이로드에 각각 실린다
<svg viewBox="0 0 24 24" className="size-[1em] shrink-0 fill-current opacity-80" aria-hidden>
  <path d={techIcons[name]} />
</svg>

// 변경 후 — 파일을 마스크로 씌우고 글자색으로 칠한다
<span
  aria-hidden
  className="size-[1em] shrink-0 bg-current opacity-80"
  style={{ mask: `url(/tech-icons/${icon}.svg) center / contain no-repeat` }}
/>
```

</details>

로컬 프로덕션 빌드(`next build --webpack`, `next start --port 3100`)에 Lighthouse 13.5.0 모바일 프리셋을 `simulate` 감속(CPU 4배, RTT 150ms, 1,638.4Kbps)으로 변경 전·후 각각 3회 순차 실행했습니다. 표의 지표는 3회 중앙값이고, 성능 점수는 3회 값을 모두 적었습니다. 변경 전 값은 앞선 LCP 원인 분석의 '현재' 단계와 같은 측정입니다.

| 지표            | 변경 전  | 변경 후      | 차이                   |
| --------------- | -------- | ------------ | ---------------------- |
| 성능 점수 (3회) | 90·88·88 | **91·90·90** | 중앙값 +2점            |
| LCP             | 3.84초   | **3.64초**   | -0.19초                |
| FCP             | 1.66초   | **1.50초**   | -0.15초                |
| Speed Index     | 2.28초   | 2.16초       | -0.12초                |
| TBT             | 33ms     | 35ms         | 차이 없음으로 판단     |
| HTML 전송량     | 45.1KiB  | **18.4KiB**  | -26.6KiB (-59%)        |
| 이미지 전송량   | 34.5KiB  | 54.9KiB      | +20.4KiB (아이콘 16개) |
| CLS             | 0        | 0            | 유지                   |

두 단계 모두 첫 회 측정의 FCP·LCP가 후속 회차보다 낮게 나왔고, 중앙값만 비교에 썼습니다. 렌더링 결과는 Playwright로 홈 Tech Stack 섹션을 다크·라이트 테마에서 각각 캡처해 아이콘 위치·색이 유지되는지 확인했습니다.

![Lighthouse 모바일 보고서 두 장을 좌우로 나란히 둔 화면. 왼쪽 "변경 전 — 기술 칩 아이콘 path가 HTML에 포함"은 성능 88점, First Contentful Paint 1.7 s, Largest Contentful Paint 3.8 s, Total Blocking Time 30 ms, Speed Index 2.3 s를 보여 줍니다. 오른쪽 "변경 후 — 아이콘을 SVG 파일로 분리"는 성능 90점, First Contentful Paint 1.5 s, Largest Contentful Paint 3.6 s, Total Blocking Time 50 ms, Speed Index 2.3 s를 보여 줍니다](../evidence/tech-icons-before-after.png)

변경 전·후 각각 2회차 보고서입니다. 표의 중앙값과는 회차별로 소수점 단위 차이가 있습니다.

단계별 6회 측정의 점수·지표·전송량·측정 설정은 [measurements.json](../evidence/tech-icon-html-weight.json)에 남겼습니다.

이 문서는 개인 portfolio에서 작성한 기존 사례를 공개 예제로 옮긴 것입니다. 이번 스킬 배포 과정에서 새로 측정한 결과가 아닙니다.
