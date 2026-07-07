# CRO Skills KO — GTM·세일즈 전략 AI 스킬 스위트

리드 제너레이션, 딜 블로커 제거, 파이프라인 설계, 유저 획득 캠페인까지 — Go-To-Market의 각 기능을
독립된 `/CRO-*` 스킬로 나눈 Claude Code 스킬 모음이다. HubSpot·Gong·Salesforce 같은 Revenue MCP와
Notion·Google Drive·Confluence·Slack 같은 Company Knowledge MCP를 연결하면 실제 데이터와 사내 정보를 함께 읽고,
연결이 없으면 내장 프레임워크로 자문한다.

이 저장소는 한국어판이다. 영문판은 별도 저장소로 분리하는 전제를 둔다.

## 스킬 구성

매출 여정의 국면별로 묶은 기능 스킬 6개와 오케스트레이터 1개. 각 스킬은 안에 여러 블록(하위 국면)을 둔다.

| 스킬 | 하는 일 (내부 블록) | 예시 트리거 |
|:--|:--|:--|
| `CRO` | 오케스트레이터/라우터 — 질문을 쪼개 알맞은 스킬로 보낸다 | "GTM", "세일즈 도와줘" |
| `CRO-market` | 시장 진입·수요 창출 — ICP/니치 · 씨앗/그물/창 리드젠 · 캠페인/ABM · GTM 모션/세그멘테이션/프라이싱 | "누구한테 팔지", "리드가 부족", "캠페인", "GTM 모션" |
| `CRO-deal` | 단건 기회 실행 — 디스커버리/3Whys · MEDDPICC 언블록 · 밸류/협상/딜 크래프팅 · 검증 콜(AI 구매) | "딜이 멈췄", "디스커버리 질문", "협상" |
| `CRO-account` | 랜드 이후 성장 — 멀티스레딩/어카운트 플랜 · 랜드앤익스팬드 · 리텐션/NRR/LIR · CSM/확장 | "확장", "리텐션", "멀티스레딩" |
| `CRO-forecast` | 예측·레브옵스 — 포캐스트 분류 · 커버리지/캐파시티 수학 · 컨슘션 포캐스팅 | "이번 분기 얼마", "커버리지", "컨슘션" |
| `CRO-org` | 팀·조직 설계 — 채용/인재상 · 보상/쿼터 · 역할 구조 · AI 네이티브 전환 · 인에이블먼트/램프 · 리더십(CEO/보드 정렬·신임 CRO 90일·승계) | "세일즈 채용", "보상 설계", "AI 세일즈 조직" |
| `CRO-coaching` | 성과 운영 — 지표 코칭 · 1:1/QBR 케이던스 · 실시간 콜 코칭 · 신뢰 전이/프레즌스 | "코칭", "1:1", "약점 진단" |

## Quick Start

Claude Code 사용자는 `npx skills`로 바로 설치할 수 있다.

```bash
npx skills add DustinYoon/cro-skills-ko \
  --skill CRO CRO-market CRO-deal CRO-account CRO-forecast CRO-org CRO-coaching \
  -a claude-code -g
```

설치 후 Claude Code 세션을 재시작해야 새 스킬이 로드된다. 이후 `/CRO`로 시작하면 질문을 적절한 하위 스킬로 라우팅한다.

설치 전 목록만 확인하려면:

```bash
npx skills add DustinYoon/cro-skills-ko --list
```

프로젝트 단위로 팀에 공유하려면 `-g`를 빼고 프로젝트 루트에서 실행한다.

## 작동 방식

세일즈 지식은 스킬에 내장돼 있고, 회사 데이터는 실행 시점에 붙인다. `gstack`식으로 라우팅, 컨텍스트,
사내 정보 검색, trust policy, 상태 보고를 공통 운영체계(`revenue-operating-system.md`)로 묶는다.

- **연결 모드** — Revenue MCP(HubSpot·Gong·Salesforce·제품/청구 데이터)와 Company Knowledge MCP(Notion·Drive·Confluence·Slack 등)를 연결하거나 데이터를 대화에 붙여넣으면, 실제 파이프라인·콜·딜 수치와 내부 정책/전략 문서로 진단한다.
- **맥락 재사용 모드** — `.cro/context.md`와 `.cro/memory/*.md`에 회사 맥락, 과거 결정, GTM 실험을 저장해 다음 세션에서 재사용한다.
- **자문 모드** — 연결이 없으면 내장 프레임워크로 "무엇을 확인하고 어떤 순서로 움직일지"를 짚어 준다. 없는 수치는 지어내지 않고 질문으로 채운다.

답변 첫 줄에는 무엇을 근거로 말하는지 데이터 소스를 밝힌다(`[MCP:Salesforce+Gong] / [회사문서:Notion] / [컨텍스트:.cro/context.md] / [자문 모드]` 등). 활동이 아니라
성과·게이트·고객 측 증거로 말하고, 조언이 갈리면 상황(GTM 모션·ACV·사이클·단계)별로 나눠 답한다.

## 설치

### 플러그인 설치 (Claude Code CLI, 권장)

Claude Code 플러그인으로 설치하면 **스킬·`/cro-*` 슬래시 커맨드·SessionStart 자동발화 훅이 한 번에** 등록된다(`npx skills`는 `skills/`만 복사). 설치 후 세션을 재시작하면 `cro-skills-ko:CRO` 등으로 스킬 목록에 뜬다.

```bash
claude plugin marketplace add DustinYoon/cro-skills-ko   # GitHub 에서 마켓플레이스 등록
claude plugin install cro-skills-ko@cro-skills-ko        # 플러그인 설치 (전역, --scope user 기본)
# 로컬 클론에서 설치하려면 리포 경로를 그대로 넘긴다:
#   claude plugin marketplace add /path/to/cro-skills-ko
```

### npx skills / install.sh

```bash
npx skills add DustinYoon/cro-skills-ko --skill CRO CRO-market CRO-deal CRO-account CRO-forecast CRO-org CRO-coaching -a claude-code -g
bash install.sh                          # ~/.claude/skills 에 설치 + SessionStart 훅 + 슬래시 커맨드 병합
bash install.sh <repo>/.claude/skills    # 프로젝트에 설치(팀 공유, 커밋)
CRO_INSTALL_HOOK=0 bash install.sh       # 훅 없이 스킬만 설치
CRO_INSTALL_COMMANDS=0 bash install.sh   # 슬래시 커맨드 없이 설치
python3 validate_skills.py               # 구조 검증 (설치본: python3 validate_skills.py ~/.claude/skills)
python3 tests/check_outputs.py           # 드라이런 산출물 스모크 테스트
python3 tests/check_hook.py              # SessionStart 부트스트랩 훅 스모크 테스트
python3 tests/check_commands.py          # 슬래시 커맨드 구조 스모크 테스트
```

Claude Code CLI 사용자는 **플러그인 설치**가 1차 권장이다(스킬·커맨드·훅 일괄). `npx skills`는 스킬만 필요하거나 타 호스트에 붙일 때, `install.sh`는 로컬 클론에서 직접 복사해야 할 때 쓴다(훅·슬래시 커맨드는 `install.sh`·플러그인 경로에서만 설치된다).

### 자동 발화 (SessionStart 훅)

스킬은 트리거 키워드가 걸릴 때만 발화한다. 사용자가 `/CRO`를 기억하지 않아도 세일즈·GTM 신호에
**자동으로** 발화하도록, `hooks/`의 SessionStart 부트스트랩을 `~/.claude/settings.json`에 등록할 수 있다.
매 세션 시작·`/clear`·컨텍스트 압축 때 라우팅 규칙(1% 규칙)과 불변 규율(데이터 소스 표기·수치 날조 금지·
진단 우선)이 주입된다. `obra/superpowers`의 `using-superpowers` 부트스트랩과 같은 방식이다.

> **전제:** 자동 발화 훅은 **로컬 클론에서 `bash install.sh`를 돌릴 때만** 설치된다(훅을 `~/.claude/cro-hooks/`로
> 복사 후 settings.json 병합). 위의 권장 설치인 `npx skills add …`는 `skills/`만 복사하고 `hooks/`는 가져오지
> 않으므로, npx로 설치했다면 `hooks/README.md`의 수동 설치(방법 2)로 훅을 따로 등록해야 한다.

자세히·수동 설치·이식성: `hooks/README.md`.

### 저마찰 진입점 (슬래시 커맨드)

아티팩트를 바로 던져 분석을 시작할 수 있다. 인테이크 질문 없이 곧장 fetch→파싱→분석으로 간다.

```text
/cro-deal <Gong URL | 통화 전사 붙여넣기 | 파일경로>   # 3 Whys·MEDDPICC 바로 채점
/cro-forecast pipeline.csv                              # 포캐스트 분류·커버리지 (딜 많으면 병렬)
/cro-market https://competitor.com                      # 포지셔닝·니치 분석 (세그먼트 많으면 병렬)
/cro-account renewals.csv     /cro-coaching reps.csv     /cro-org scorecard.md
/cro <질문 또는 아티팩트>                                # 오케스트레이터: 분해→라우팅
```

각 커맨드는 해당 스킬의 **아티팩트 우선 경로**로 진입시키는 얇은 래퍼다(`commands/*.md`). 아티팩트가 비면 일반 라우팅으로 넘어가고, 아티팩트에 없는 수치는 여전히 지어내지 않는다(철칙 유지).

> **전제:** 슬래시 커맨드도 훅과 마찬가지로 **`bash install.sh`를 돌릴 때만** `~/.claude/commands/`에 설치된다. `npx skills add …`는 `skills/`만 복사한다. npx로만 설치했다면 `commands/*.md`가 로컬에 없으므로, **리포를 clone 해 `bash install.sh`를 돌리거나**(권장), clone한 리포의 `commands/*.md`를 `~/.claude/commands/`(전역) 또는 `<repo>/.claude/commands/`(프로젝트)로 직접 복사한다.

### 병렬 처리 (fan-out)

분석 유닛이 많으면 서브에이전트로 병렬 처리해 처리량·컨텍스트를 확보한다. `CRO-forecast`(딜 >8개 → 딜당 병렬 MEDDPICC 채점), `CRO-market`(세그먼트·경쟁사 >3개 → 유닛당 병렬 리서치), `CRO` 오케스트레이터(독립 진단 축 2개+ → 축별 병렬)에서 자동 판단한다. 유닛이 적으면 인라인(오버헤드 낭비 금지). 병렬이라고 데이터 소스 규율·수치 날조 금지를 느슨하게 하지 않는다 — 각 서브에이전트가 규율을 상속하고, 집계가 빈칸을 지어내지 않는다.

## 사용 예

- "이 $200K 딜이 3주째 안 움직여요" → `CRO-deal` (MEDDPICC 점수화 → 블로커 → 언블록 계획)
- "새 시장 진출하려는데 어디부터?" → `CRO-market` (니치 확정 → 모션·캠페인 → 리드 실행)
- "분기 말인데 포캐스트가 못 미더워요" → `CRO-forecast` → `CRO-deal`
- "AI로 세일즈 조직을 어떻게 바꾸지?" → `CRO-org` (스킬화·에이전트·생산성 KPI) + `CRO-deal` (검증 콜)
- "고객이 자꾸 이탈해요" → `CRO-account` (리텐션/LIR → 확장 모션)
- `/cro-deal <Gong URL>` — 통화를 바로 받아 3 Whys·MEDDPICC 채점 (인테이크 생략)
- `/cro-forecast pipeline.csv` (딜 40개) — 딜당 서브에이전트 병렬 채점 → 분류표 집계

## 내장 프레임워크

세일즈 지식은 `skills/CRO/references/`에 들어 있어 외부 자료 없이도 자문한다.

- `frameworks-meddpicc.md` — MEDDPICC, 3 Whys, 챔피언 vs 코치, EB 미팅, POV 4조건 (John McMahon, 《The Qualified Sales Leader》)
- `frameworks-saf.md` — 채용·교육·관리·수요창출 4공식 (Mark Roberge, 《The Sales Acceleration Formula》)
- `frameworks-fi2i.md` — 니치, 리드 3유형(Seeds/Nets/Spears), 확장·딜규모·고객성공 (Aaron Ross & Jason Lemkin, 《From Impossible to Inevitable》)
- `revenue-operating-system.md` — 라우팅, 데이터 맵, 사내정보 검색, trust policy, persistent memory, 상태 프로토콜
- `insights-corpus.md` — 팟캐스트·강연 인터뷰에서 뽑은 인사이트를 CRO 기능 7대 도메인으로 정리. 책이 항구적 원칙이라면 인터뷰는 최신·상황적 지식.
- `conflict-resolution.md` — 상충 해소·맥락 적합·지식 누적 규약. 소스가 갈리면 조건별로 나눠 답한다.
- `data-sources.md` · `mcp-data-access.md` — 데이터 소스·MCP 접근 규약

> 요약은 원저작 방법론을 자체 정리한 것으로, 스킬 동작에 원문 파일은 필요 없다.

## MCP 연결 (선택)

`.mcp.json.template`을 `~/.claude/mcp.json`(전역) 또는 프로젝트 `.mcp.json`에 병합하고, 자격 증명은
환경변수로 넣는다. 서버 패키지명·툴 구성은 벤더/커뮤니티 배포마다 다를 수 있으니, 연결 뒤 세션 도구
목록에서 실제 툴 이름을 확인해 쓴다. (자세히: `mcp-data-access.md`)

권장 연결 순서:

1. Revenue MCP: Salesforce/HubSpot + Gong부터 연결한다.
2. Company Knowledge MCP: Notion/Google Drive/Confluence/SharePoint/Slack 중 실제 전략·가격·QBR 문서가 있는 곳을 읽기 전용으로 연결한다.
3. Product/Billing MCP: 리텐션·컨슘션·NDR을 다루려면 사용량과 청구 데이터를 추가한다.

쓰기 권한은 기본적으로 쓰지 않는다. CRM 업데이트, 문서 수정, Slack 발송은 사용자가 명시 요청하고 대상/내용을 확인한 뒤에만 수행한다.

## 사내 자료 연결 (선택)

플레이북·인터뷰·요약 같은 사내 세일즈 노트가 있으면 폴더를 하나 물려 내장 지식을 보강할 수 있다.

```bash
export CRO_CORPUS_DIR="/path/to/our-sales-notes"   # 읽기 전용 참고
```

없으면 조용히 건너뛴다. 있으면 그 폴더의 최신 자료를 내장 `insights-corpus.md`보다 우선해 읽는다. (자세히: `data-sources.md`)

## 지속 맥락 (선택)

프로젝트별 CRO 메모리를 두면 매번 같은 회사 맥락을 다시 묻지 않는다.

```text
.cro/context.md              # GTM 모션, ACV, 세일즈 사이클, 구매주체, 단계
.cro/memory/decisions.md     # ICP, 가격, 할인, 보상, 프로세스 결정
.cro/memory/experiments.md   # GTM 실험과 결과
.cro/memory/accounts.md      # 전략 계정 학습(민감정보 최소화)
```

스킬은 확인된 사실만 저장하고, 모르는 것은 `미정`으로 남긴다.

## 호환성

| 호스트 | 상태 | 비고 |
|:--|:--|:--|
| **Claude Code (CLI)** | 네이티브(주 타깃) | `~/.claude/skills/` 또는 프로젝트 `.claude/skills/` 자동 로드, 파일·셸로 `.cro/context.md` 저장 |
| **Claude 앱(웹/데스크톱)** | 패키징 필요 | `skills/`를 zip으로 올린다(references 동봉). 샌드박스라 맥락은 대화 안에서만 유지 |
| **Codex 등 타 에이전트** | 비네이티브 | `AGENTS.md` 체계 — 참조 자료로 쓰거나 규약을 AGENTS.md로 옮긴다 |

스킬은 조언 전에 회사 맥락을 확정해 `./.cro/context.md`(또는 `$CRO_CONTEXT_FILE`)에 저장하고 재사용한다.
상위 맥락(`~/.claude/CLAUDE.md`·프로젝트 `CLAUDE.md`·`AGENTS.md`·대화 히스토리)을 이미 읽었으면 그걸 먼저
흡수하고 다시 묻지 않는다. 파일 저장이 안 되는 앱에서는 맥락 카드를 대화 안에 남긴다. (자세히: `portability.md`, `context-profile.md`)

`tests/`에 워크플로 드라이런 예시가 있다: `fixtures/`(가상 입력) + `scenarios/`(스킬 실행 산출물).
`CRO-deal`(멈춘 딜 → MEDDPICC 진단·언블록), `CRO-market`(파이프라인 2배 → 씨앗·그물·창 설계),
`CRO-context-branching`(맥락 분기) 시나리오가 각 스킬의 출력 계약을 지키는지 검증한다.

## 확장

새 GTM 기능을 추가하려면 `skills/CRO-<name>/SKILL.md`를 기존 스킬(예: `CRO-deal`) 구조로 만들고,
`CRO/SKILL.md` 라우팅 표에 한 줄 더한 뒤 `validate_skills.py`로 검증한다. 기능 스킬은 필수 섹션
(`철칙`·`아티팩트 우선`·`참조`·`데이터 소스`·`워크플로`·`출력 형식`·`안티패턴`·`합리화 차단`·`핸드오프`)을 갖춰야 한다.

- **`description`은 트리거 전용**으로 쓴다("이럴 때 쓴다" + `Triggers:`). 워크플로 요약을 넣으면 에이전트가
  본문을 안 읽고 설명만 따르는 함정이 있다(superpowers 실측). 무엇을 하는지는 본문 첫 문단이 담당한다.
- **`철칙`(Iron Law)**은 압박 하에서도 지키는 불변 규율 한 줄, **`합리화 차단`**은 에이전트가 실제로 쓸
  변명→현실 2열 표다. 규율이 시간·권위·매몰비용 압박에 무너지지 않게 한다.
- **`아티팩트 우선`(저마찰 진입)**은 URL·전사·CSV·파일을 바로 받아 인테이크를 건너뛰는 fast path다. 대응
  `commands/cro-<name>.md` 래퍼도 함께 두고 `tests/check_commands.py`로 검증한다. 아티팩트 fetch가 필요하면
  `allowed-tools`에 `WebFetch`(웹)·`Read`(파일)를 더한다.
- **fan-out**이 필요한 스킬은 `allowed-tools`에 `Task`를 더하고 본문에 **병렬 처리** 규약(언제·어떻게·집계·
  가드레일)을 명시한다. `validate_skills.py`가 Task 선언 시 규약 존재를 강제한다. 유닛이 많을 때만 병렬,
  각 서브에이전트는 데이터 소스 규율·수치 날조 금지를 상속한다.
- 새 규율을 넣기 전에 `tests/eval-scenarios/`의 압박 시나리오로 **스킬 없이 실패(RED)를 먼저 재현**하고
  스킬로 준수(GREEN)를 확인한다(방법론: `tests/eval-scenarios/README.md`).

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
