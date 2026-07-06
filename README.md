# CRO — GTM·세일즈 전략 AI 스킬 스위트

리드 제너레이션부터 딜 블로커 제거, 파이프라인 설계, 유저 획득 캠페인까지 — Go-To-Market의 각 기능을
**독립된 `/CRO-*` 스킬**로 분해한 모음입니다. HubSpot·Gong·Salesforce를 MCP로 연결하면 실시간 데이터로,
연결이 없으면 내장 프레임워크로 자문(advisory)합니다.

## 설계 원칙 (전역·이식성)

- **자체 완결형.** 세일즈 지식은 스킬 안 `CRO/references/`에 내장됩니다. 특정 폴더(예: 개인 스터디 코퍼스)에 의존하지 않아 **누구나 어떤 디렉토리에서도** 씁니다.
- **지식은 내장, 데이터는 주입.** "우리 회사 데이터"는 런타임에 주입: `MCP → CRO_CORPUS_DIR/경로 → 첨부 → 자문 모드` 우선순위. (규약: `CRO/references/data-sources.md`)
- **근거 우선.** 활동이 아니라 성과·게이트·고객 측 증거로 말하고, 없는 수치·인용을 지어내지 않습니다.

## 스킬 구성

매출 여정의 **국면**으로 묶은 6개 기능 스킬 + 오케스트레이터. 각 스킬은 내부에 여러 블록(하위 국면)을 갖는다.

| 스킬 | 하는 일 (내부 블록) | 예시 트리거 |
|:--|:--|:--|
| `CRO` | 오케스트레이터/라우터 — 질문을 분해해 알맞은 스킬로 보냄 | "GTM", "세일즈 도와줘" |
| `CRO-market` | 시장 진입·수요 창출 — ICP/니치 · 씨앗/그물/창 리드젠 · 캠페인/ABM · GTM 모션/세그멘테이션/프라이싱 | "누구한테 팔지", "리드가 부족", "캠페인", "GTM 모션" |
| `CRO-deal` | 단건 기회 실행 — 디스커버리/3Whys · MEDDPICC 언블록 · 밸류/협상/딜 크래프팅 · 검증 콜(AI 구매) | "딜이 멈췄", "디스커버리 질문", "협상" |
| `CRO-account` | 랜드 이후 성장 — 멀티스레딩/어카운트 플랜 · 랜드앤익스팬드 · 리텐션/NRR/LIR · CSM/확장 | "확장", "리텐션", "멀티스레딩" |
| `CRO-forecast` | 예측·레브옵스 — 포캐스트 분류 · 커버리지/캐파시티 수학 · 컨슘션 포캐스팅 | "이번 분기 얼마", "커버리지", "컨슘션" |
| `CRO-org` | 팀·조직 설계 — 채용/인재상 · 보상/쿼터 · 역할 구조 · AI 네이티브 전환 · 인에이블먼트/램프 · 리더십(CEO/보드 정렬·신임 CRO 90일·승계) | "세일즈 채용", "보상 설계", "AI 세일즈 조직" |
| `CRO-coaching` | 성과 운영 — 지표 코칭 · 1:1/QBR 케이던스 · 실시간 콜 코칭 · 신뢰 전이/프레즌스 | "코칭", "1:1", "약점 진단" |

## 내장 프레임워크 (지식 원천)

`skills/CRO/references/`:
- `frameworks-meddpicc.md` — MEDDPICC, 3 Whys, 챔피언 vs 코치, EB 미팅, POV 4조건, 포캐스팅·코칭·채용 (John McMahon, 《The Qualified Sales Leader》)
- `frameworks-saf.md` — 채용·교육·관리·수요창출 4공식 (Mark Roberge, 《The Sales Acceleration Formula》)
- `frameworks-fi2i.md` — 니치, 리드 3유형(Seeds/Nets/Spears), 확장·딜규모·고객성공 (Aaron Ross & Jason Lemkin, 《From Impossible to Inevitable》)
- `insights-corpus.md` — 인터뷰 코퍼스(팟캐스트·강연) 증류 인사이트, **(화자 × 매체)** 출처 표기, **CRO 기능 7대 도메인**으로 조직(§1 딜~§7 정렬·전략). 약 20명 화자(Matt Dixon/JOLT, Becca Lindquist/Clay, Elena Verna/Lovable, Healey Cypher/BoomPop, Chad Peets, Carles Reina/ElevenLabs, Mark Roberge, Jane Thompson, John Donnelly, Jen Abel, Bob Ranaldi, Jon Addison/Okta, Jeanne DeWitt/Vercel, Elenore Dorfman/Anthropic, Sam Senior, Devavrat Shah 등) + 상충·맥락 요약표. 책이 항구적 원칙이면 인터뷰는 최신·상황적 지식.
- `conflict-resolution.md` — **상충 해소·맥락 적합·지식 누적 규약.** 세일즈 지식은 쌓이고 상충하며 맥락 의존적이다. 조언 전 맥락 프로파일을 확정하고, 소스가 갈리면 조건별로 갈라 답한다.
- `data-sources.md` — 데이터 소스 해석 규약
- `mcp-data-access.md` — HubSpot/Gong/Salesforce MCP 접근 규약

> 위 요약은 원저작 방법론을 자체 정리한 것으로, 스킬 동작에 원문 파일은 필요하지 않습니다.

## 설치

```bash
bash install.sh                          # ~/.claude/skills 로 설치 (Claude Code 개인 스킬)
bash install.sh <repo>/.claude/skills    # 프로젝트 스코프 설치(팀 공유, 커밋)
python3 validate_skills.py               # 구조 검증 (설치본: python3 validate_skills.py ~/.claude/skills)
python3 tests/check_outputs.py           # 드라이런 산출물 스모크 테스트
```

## 호환성 (제품별)

| 호스트 | 상태 | 비고 |
|:--|:--|:--|
| **Claude Code (CLI)** | 네이티브(주 타깃) | `~/.claude/skills/` 또는 프로젝트 `.claude/skills/` 자동 로드, FS·셸로 `.cro/context.md` 지속 |
| **Claude 앱(웹/데스크톱)** | 패키징 필요 | `skills/`를 zip으로 Skills 업로드(references 동봉). 샌드박스라 맥락은 대화 한정 |
| **Codex 등 타 에이전트** | 비네이티브 | `AGENTS.md` 체계 — 참조 자료로 쓰거나 규약을 AGENTS.md로 이식 |

**맥락은 어디에 적용되나:** 스킬은 조언 전에 회사 맥락을 확정하고 `./.cro/context.md`(또는 `$CRO_CONTEXT_FILE`)에 저장해 재사용합니다. **상위 맥락을 이미 읽었으면(예: `~/.claude/CLAUDE.md`·프로젝트 `CLAUDE.md`·`AGENTS.md`·대화 히스토리) 그걸 먼저 흡수하고 다시 묻지 않습니다.** FS가 없는 앱 환경에선 카드를 대화 안에 유지합니다. (자세히: `portability.md`, `context-profile.md`)

`tests/`에 워크플로 드라이런 예시가 있습니다: `fixtures/`(가상 입력) + `scenarios/`(스킬을 실행한 산출물). `CRO-deal`(멈춘 딜 → MEDDPICC 진단·언블록)과 `CRO-market`(파이프라인 2배 → 씨앗·그물·창 설계, 블록 B)·`CRO-context-branching`(맥락 분기) 시나리오가 각 스킬의 출력 계약을 충족하는지 검증합니다.

## MCP 연결 (선택)

`.mcp.json.template` 를 `~/.claude/mcp.json`(전역) 또는 프로젝트 `.mcp.json` 에 병합하고, 자격 증명을 환경변수로 주입합니다.
서버 패키지명·툴 구성은 벤더/커뮤니티 배포에 따라 다를 수 있어, 연결 후 세션 도구 목록에서 실제 툴 이름을 확인해 사용합니다. (자세히: `mcp-data-access.md`)

## 사내 자료 연결 (선택)

```bash
export CRO_CORPUS_DIR="/path/to/our-sales-notes"   # 플레이북·인터뷰·요약 등, 읽기 전용 참고
```

없으면 조용히 건너뛰고 내장 프레임워크로 동작합니다. 연결 시엔 그 폴더의 `*_핵심정리.md`(인터뷰 요약 등)를 **최신·상황적 지식**으로 읽어 내장 `insights-corpus.md` 스냅샷을 보강합니다.

**지식 우선순위:** 책(항구적 원칙) > 인터뷰(최신·상황적). 상충하면 `conflict-resolution.md`가 맥락으로 심판합니다 — 같은 조언도 상황(GTM 모션·ACV·사이클·단계 등)에 따라 맞고 틀리므로, 스킬은 조건을 갈라 답합니다.

## 사용 예

- "이 $200K 딜이 3주째 안 움직여요" → `CRO-deal` (MEDDPICC 점수화 → 블로커 → 언블록 계획)
- "새 시장 진출하려는데 어디부터?" → `CRO-market` (니치 확정 → 모션·캠페인 → 리드 실행)
- "분기 말인데 포캐스트가 못 미더워요" → `CRO-forecast` → `CRO-deal`
- "AI로 세일즈 조직을 어떻게 바꾸지?" → `CRO-org` (스킬화·에이전트·생산성 KPI) + `CRO-deal` (검증 콜)
- "고객이 자꾸 이탈해요" → `CRO-account` (리텐션/LIR → 확장 모션)

## 확장

새 GTM 기능을 추가하려면 `skills/CRO-<name>/SKILL.md` 를 기존 스킬(예: `CRO-deal`) 구조로 만들고,
`CRO/SKILL.md` 라우팅 표에 한 줄 추가한 뒤 `validate_skills.py` 로 검증하세요.
