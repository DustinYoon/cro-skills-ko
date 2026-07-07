# CRO Skills KO - GTM·세일즈 전략 AI 스킬 스위트

리드젠, 딜 언블록, 파이프라인 설계, 유저 획득까지 GTM의 각 국면을 `/CRO-*` 스킬로 쪼갠 Claude Code 스킬 모음입니다. HubSpot·Gong·Salesforce 같은 Revenue MCP나 Notion·Drive·Confluence·Slack 같은 Company Knowledge MCP를 붙이면 실제 데이터로 진단하고, 연결이 없으면 내장 프레임워크로 자문합니다. 한국어판입니다(영문판은 별도 저장소로 분리할 예정).

> Shoutout: 이 스킬의 최신 CRO 인터뷰 코퍼스는 **윤덕진(Dukjin Yoon)** 님의 LinkedIn 뉴스레터 **[CRO 스터디](https://www.linkedin.com/newsletters/cro-%EC%8A%A4%ED%84%B0%EB%94%94-7395346980689895424/)** 를 바탕으로 정리했습니다. 원문 인터뷰·요약은 해당 뉴스레터에서 확인하실 수 있습니다.

## 스킬 구성

매출 여정의 국면별 기능 스킬 6개와 오케스트레이터 1개입니다. 각 스킬은 안에 하위 국면(블록)을 여럿 둡니다.

| 스킬 | 하는 일 (내부 블록) | 예시 트리거 |
|:--|:--|:--|
| `CRO` | 오케스트레이터/라우터 — 질문을 쪼개 알맞은 스킬로 보냅니다 | "GTM", "세일즈 도와줘" |
| `CRO-market` | 시장 진입·수요 창출 — ICP/니치 · 씨앗/그물/창 리드젠 · 캠페인/ABM · GTM 모션/세그멘테이션/프라이싱 | "누구한테 팔지", "리드가 부족", "캠페인", "GTM 모션" |
| `CRO-deal` | 단건 기회 실행 — 디스커버리/3Whys · MEDDPICC 언블록 · 밸류/협상/딜 크래프팅 · 검증 콜(AI 구매) | "딜이 멈췄", "디스커버리 질문", "협상" |
| `CRO-account` | 랜드 이후 성장 — 멀티스레딩/어카운트 플랜 · 랜드앤익스팬드 · 리텐션/NRR/LIR · CSM/확장 | "확장", "리텐션", "멀티스레딩" |
| `CRO-forecast` | 예측·레브옵스 — 포캐스트 분류 · 커버리지/캐파시티 수학 · 컨슘션 포캐스팅 | "이번 분기 얼마", "커버리지", "컨슘션" |
| `CRO-org` | 팀·조직 설계 — 채용/인재상 · 보상/쿼터 · 역할 구조 · AI 네이티브 전환 · 인에이블먼트/램프 · 리더십(CEO/보드 정렬·신임 CRO 90일·승계) | "세일즈 채용", "보상 설계", "AI 세일즈 조직" |
| `CRO-coaching` | 성과 운영 — 지표 코칭 · 1:1/QBR 케이던스 · 실시간 콜 코칭 · 신뢰 전이/프레즌스 | "코칭", "1:1", "약점 진단" |

## 설치

Claude Code CLI라면 **플러그인 설치**가 가장 깔끔합니다. 스킬, `/cro-*` 슬래시 커맨드, SessionStart 자동발화 훅이 한 번에 붙습니다.

```bash
claude plugin marketplace add DustinYoon/cro-skills-ko
claude plugin install cro-skills-ko@cro-skills-ko
# 로컬 클론에서 설치하려면 리포 경로를 그대로 넘깁니다:
#   claude plugin marketplace add /path/to/cro-skills-ko
```

설치 후 세션을 재시작하면 `cro-skills-ko:CRO` 등으로 스킬 목록에 뜨고, `/CRO`로 라우팅이 시작됩니다.

스킬만 필요하거나 다른 호스트에 붙일 때는 `npx skills`, 로컬 클론에서 직접 복사할 때는 `install.sh`를 씁니다. `npx`는 `skills/`만 복사하므로, 훅과 슬래시 커맨드는 플러그인이나 `install.sh` 경로로 설치해야 붙습니다.

```bash
npx skills add DustinYoon/cro-skills-ko --skill CRO CRO-market CRO-deal CRO-account CRO-forecast CRO-org CRO-coaching -a claude-code -g
npx skills add DustinYoon/cro-skills-ko --list   # 설치 전 목록만 확인
bash install.sh                          # ~/.claude/skills + SessionStart 훅 + 슬래시 커맨드
bash install.sh <repo>/.claude/skills    # 프로젝트에 설치(팀 공유, 커밋)
CRO_INSTALL_HOOK=0 bash install.sh       # 훅 없이
CRO_INSTALL_COMMANDS=0 bash install.sh   # 커맨드 없이
python3 validate_skills.py               # 구조 검증
python3 tests/check_outputs.py           # 산출물 스모크 테스트
python3 tests/check_hook.py              # 훅 스모크 테스트
python3 tests/check_commands.py          # 커맨드 스모크 테스트
```

## 작동 방식

세일즈 지식은 스킬에 내장돼 있고, 회사 데이터는 실행 시점에 붙습니다. 라우팅·컨텍스트·사내정보 검색·trust policy·상태 보고는 공통 운영체계(`revenue-operating-system.md`)로 묶여 있습니다.

- **연결 모드** — Revenue MCP와 Company Knowledge MCP를 붙이거나 데이터를 대화에 붙여넣으면, 실제 파이프라인·콜·딜 수치와 내부 문서로 진단합니다.
- **맥락 재사용 모드** — `.cro/context.md`와 `.cro/memory/*.md`에 회사 맥락·과거 결정·GTM 실험을 저장해 다음 세션에서 재사용합니다.
- **자문 모드** — 연결이 없으면 내장 프레임워크로 무엇을 어떤 순서로 확인할지 짚어 줍니다. 없는 수치는 지어내지 않고 질문으로 채웁니다.

답변 첫 줄에는 근거가 된 데이터 소스를 밝힙니다(`[MCP:Salesforce+Gong]`, `[회사문서:Notion]`, `[컨텍스트:.cro/context.md]`, `[자문 모드]` 등). 활동이 아니라 성과·게이트·고객 측 증거로 말하고, 조언이 갈리면 상황(GTM 모션·ACV·사이클·단계)별로 나눠 답합니다.

## 슬래시 커맨드로 바로 시작

아티팩트를 바로 던지면 인테이크 질문 없이 fetch→파싱→분석으로 직행합니다.

```text
/cro-deal <Gong URL | 통화 전사 | 파일경로>   # 3 Whys·MEDDPICC 바로 채점
/cro-forecast pipeline.csv                     # 포캐스트 분류·커버리지 (딜 많으면 병렬)
/cro-market https://competitor.com             # 포지셔닝·니치 분석 (세그먼트 많으면 병렬)
/cro-account renewals.csv    /cro-coaching reps.csv    /cro-org scorecard.md
/cro <질문 또는 아티팩트>                       # 오케스트레이터: 분해→라우팅
```

각 커맨드는 해당 스킬의 아티팩트 우선 경로로 넣는 얇은 래퍼입니다(`commands/*.md`). 아티팩트가 비면 일반 라우팅으로 넘어가고, 없는 수치는 여전히 지어내지 않습니다.

## 자동 발화

스킬은 트리거 키워드가 걸릴 때 발화합니다. `/CRO`를 기억하지 않아도 세일즈·GTM 신호에 자동으로 뜨도록, SessionStart 훅이 매 세션 시작·`/clear`·컨텍스트 압축 때 라우팅 규칙과 불변 규율(데이터 소스 표기, 수치 날조 금지, 진단 우선)을 주입합니다. `obra/superpowers`의 `using-superpowers` 부트스트랩과 같은 방식입니다.

플러그인으로 설치하면 훅은 자동으로 붙습니다. `install.sh`는 훅을 `~/.claude/cro-hooks/`로 복사하고 settings.json에 병합합니다. `npx`로만 설치했다면 `hooks/README.md`의 수동 등록을 따릅니다.

## 병렬 처리

분석 유닛이 많으면 서브에이전트로 병렬 처리합니다. `CRO-forecast`(딜 8개 초과 → 딜당 MEDDPICC 채점), `CRO-market`(세그먼트·경쟁사 3개 초과 → 유닛당 리서치), `CRO`(독립 진단 축 2개 이상 → 축별)가 알아서 판단하고, 유닛이 적으면 인라인으로 처리합니다. 병렬이어도 데이터 소스 규율과 수치 날조 금지는 각 서브에이전트가 그대로 상속하고, 집계 단계가 빈칸을 지어내지 않습니다.

## 사용 예

- "이 $200K 딜이 3주째 안 움직여요" → `CRO-deal` (MEDDPICC 점수화 → 블로커 → 언블록 계획)
- "새 시장 진출하려는데 어디부터?" → `CRO-market` (니치 확정 → 모션·캠페인 → 리드 실행)
- "분기 말인데 포캐스트가 못 미더워요" → `CRO-forecast` → `CRO-deal`
- "AI로 세일즈 조직을 어떻게 바꾸지?" → `CRO-org` (스킬화·에이전트·생산성 KPI) + `CRO-deal` (검증 콜)
- "고객이 자꾸 이탈해요" → `CRO-account` (리텐션/LIR → 확장 모션)
- `/cro-deal <Gong URL>` — 통화를 바로 받아 3 Whys·MEDDPICC 채점
- `/cro-forecast pipeline.csv` (딜 40개) — 딜당 병렬 채점 후 분류표 집계

## 내장 프레임워크

세일즈 지식은 `skills/CRO/references/`에 들어 있어 외부 자료 없이도 자문합니다.

- `frameworks-meddpicc.md` — MEDDPICC, 3 Whys, 챔피언 vs 코치, EB 미팅, POV 4조건 (John McMahon, 《The Qualified Sales Leader》)
- `frameworks-saf.md` — 채용·교육·관리·수요창출 4공식 (Mark Roberge, 《The Sales Acceleration Formula》)
- `frameworks-fi2i.md` — 니치, 리드 3유형(Seeds/Nets/Spears), 확장·딜규모·고객성공 (Aaron Ross & Jason Lemkin, 《From Impossible to Inevitable》)
- `revenue-operating-system.md` — 라우팅, 데이터 맵, 사내정보 검색, trust policy, persistent memory, 상태 프로토콜
- `insights-corpus.md` — 팟캐스트·강연 인터뷰 인사이트를 CRO 7대 도메인으로 정리. 책이 항구적 원칙이면 인터뷰는 최신·상황적 지식입니다.
- `conflict-resolution.md` — 상충 해소·맥락 적합·지식 누적 규약. 소스가 갈리면 조건별로 나눠 답합니다.
- `data-sources.md` · `mcp-data-access.md` — 데이터 소스·MCP 접근 규약

> 요약은 원저작 방법론을 자체 정리한 것으로, 스킬을 돌리는 데 원문 파일은 필요 없습니다.

## MCP 연결 (선택)

`.mcp.json.template`을 `~/.claude/mcp.json`(전역)이나 프로젝트 `.mcp.json`에 병합하고, 자격 증명은 환경변수로 넣습니다. 서버 패키지명·툴 구성은 배포마다 다를 수 있으니, 연결 뒤 세션 도구 목록에서 실제 툴 이름을 확인해 씁니다. (자세히: `mcp-data-access.md`)

권장 연결 순서:

1. Revenue MCP: Salesforce/HubSpot + Gong부터.
2. Company Knowledge MCP: Notion/Google Drive/Confluence/SharePoint/Slack 중 실제 전략·가격·QBR 문서가 있는 곳을 읽기 전용으로.
3. Product/Billing MCP: 리텐션·컨슘션·NDR을 다루려면 사용량·청구 데이터를 추가.

쓰기 권한은 기본적으로 쓰지 않습니다. CRM 업데이트, 문서 수정, Slack 발송은 사용자가 명시 요청하고 대상·내용을 확인한 뒤에만 합니다.

## 사내 자료 연결 (선택)

플레이북·인터뷰·요약 같은 사내 세일즈 노트가 있으면 폴더를 하나 물려 내장 지식을 보강할 수 있습니다.

```bash
export CRO_CORPUS_DIR="/path/to/our-sales-notes"   # 읽기 전용 참고
```

없으면 조용히 건너뛰고, 있으면 그 폴더 자료를 내장 `insights-corpus.md`보다 먼저 읽습니다. (자세히: `data-sources.md`)

## 지속 맥락 (선택)

프로젝트별 CRO 메모리를 두면 매번 같은 회사 맥락을 다시 묻지 않습니다.

```text
.cro/context.md              # GTM 모션, ACV, 세일즈 사이클, 구매주체, 단계
.cro/memory/decisions.md     # ICP, 가격, 할인, 보상, 프로세스 결정
.cro/memory/experiments.md   # GTM 실험과 결과
.cro/memory/accounts.md      # 전략 계정 학습(민감정보 최소화)
```

스킬은 확인된 사실만 저장하고, 모르는 것은 `미정`으로 남깁니다.

## 호환성

| 호스트 | 상태 | 비고 |
|:--|:--|:--|
| **Claude Code (CLI)** | 네이티브(주 타깃) | `~/.claude/skills/`나 프로젝트 `.claude/skills/` 자동 로드, 파일·셸로 `.cro/context.md` 저장 |
| **Claude 앱(웹/데스크톱)** | 패키징 필요 | `skills/`를 zip으로 올립니다(references 동봉). 샌드박스라 맥락은 대화 안에서만 유지 |
| **Codex 등 타 에이전트** | 비네이티브 | 참조 자료로 쓰거나 규약을 `AGENTS.md`로 옮깁니다 |

스킬은 조언 전에 회사 맥락을 확정해 `./.cro/context.md`(또는 `$CRO_CONTEXT_FILE`)에 저장하고 재사용합니다. 상위 맥락(`~/.claude/CLAUDE.md`, 프로젝트 `CLAUDE.md`, `AGENTS.md`, 대화 히스토리)을 이미 읽었으면 그걸 먼저 흡수하고 다시 묻지 않습니다. 파일 저장이 안 되는 앱에서는 맥락 카드를 대화 안에 남깁니다. (자세히: `portability.md`, `context-profile.md`)

`tests/`에는 워크플로 드라이런 예시가 있습니다. `fixtures/`(가상 입력)와 `scenarios/`(실행 산출물)로, `CRO-deal`(멈춘 딜 진단·언블록), `CRO-market`(파이프라인 2배 설계), `CRO-context-branching`(맥락 분기)이 각 스킬의 출력 계약을 지키는지 검증합니다.

## 확장

새 GTM 기능은 `skills/CRO-<name>/SKILL.md`를 기존 스킬(예: `CRO-deal`) 구조로 만들고, `CRO/SKILL.md` 라우팅 표에 한 줄 더한 뒤 `validate_skills.py`로 검증합니다. 기능 스킬은 필수 섹션(`철칙`·`아티팩트 우선`·`참조`·`데이터 소스`·`워크플로`·`출력 형식`·`안티패턴`·`합리화 차단`·`핸드오프`)을 갖춰야 합니다.

- **`description`은 트리거 전용**으로 씁니다("이럴 때 쓴다" + `Triggers:`). 워크플로 요약을 넣으면 에이전트가 본문을 안 읽고 설명만 따르는 함정이 있습니다(superpowers 실측). 무엇을 하는지는 본문 첫 문단이 담당합니다.
- **`철칙`(Iron Law)**은 압박 하에서도 지키는 불변 규율 한 줄, **`합리화 차단`**은 실제로 쓸 변명→현실 2열 표입니다. 규율이 시간·권위·매몰비용 압박에 무너지지 않게 합니다.
- **`아티팩트 우선`**은 URL·전사·CSV·파일을 바로 받아 인테이크를 건너뛰는 fast path입니다. 짝이 되는 `commands/cro-<name>.md` 래퍼도 함께 두고 `tests/check_commands.py`로 검증합니다. 아티팩트 fetch가 필요하면 `allowed-tools`에 `WebFetch`(웹)·`Read`(파일)를 더합니다.
- **fan-out**이 필요하면 `allowed-tools`에 `Task`를 더하고 본문에 병렬 처리 규약(언제·어떻게·집계·가드레일)을 적습니다. `validate_skills.py`가 Task 선언 시 규약 존재를 강제합니다. 각 서브에이전트는 데이터 소스 규율과 수치 날조 금지를 상속합니다.
- 새 규율을 넣기 전에 `tests/eval-scenarios/`의 압박 시나리오로 **스킬 없이 실패(RED)를 먼저 재현**하고 스킬로 준수(GREEN)를 확인합니다(방법론: `tests/eval-scenarios/README.md`).

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
