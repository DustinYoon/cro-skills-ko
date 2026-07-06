# MCP 데이터 접근 가이드 (Revenue · Company Knowledge)

> 모든 `CRO-*` 스킬이 **실시간 CRM/콜 데이터와 사내 지식**을 읽을 때 따르는 규약.
> 스킬은 특정 툴 이름을 하드코딩하지 않는다 — MCP 서버마다 툴 이름이 다르므로 **런타임에 탐지**한다.

## 1. MCP가 세션에 있는지 탐지

MCP 서버가 연결되면 세션 도구 목록에 해당 서버의 툴이 노출된다(클라이언트에 따라 `hubspot`, `salesforce`, `gong` 등의 네임스페이스/프리픽스로 보임).

**스킬 진입 시 절차:**
1. 사용 가능한 도구 목록에서 Revenue MCP(`hubspot`, `salesforce`, `gong`, `crm`, `sfdc`, `revops`, `stripe`, `product`)를 찾는다.
2. Company Knowledge MCP(`notion`, `drive`, `google`, `confluence`, `sharepoint`, `slack`, `jira`, `linear`, `docs`, `knowledge`)를 찾는다.
3. 도구가 있으면 **능력 기준**으로 선택한다. 툴 이름을 추측하지 말고, 검색/조회/상세읽기/쿼리/쓰기 가능 여부를 확인한다.
4. 없으면 `data-sources.md`의 하위 순위(저장 맥락/코퍼스/첨부/자문)로 폴백한다.
5. 어떤 소스를 쓰는지 답변 첫 줄에 표기한다.

> 툴 이름을 모르면 **추측하지 말고** 목록에서 확인한다. 목록에 없으면 "연결 안 됨"으로 간주.

## 2. 각 스킬이 필요로 하는 데이터(능력 기준)

플랫폼별 구현·툴명은 달라도, 스킬이 요구하는 **능력**은 다음과 같다. 연결된 MCP에서 이에 해당하는 툴을 골라 쓴다.

### HubSpot (CRM)
- **필요 능력:** deals(딜) 조회/검색, companies·contacts 조회, deal의 stage·amount·closedate·owner, engagements(이메일/미팅/노트), pipeline·deal stage 정의.
- **쓰는 스킬:** `CRO-forecast`(오픈 파이프라인·스테이지·확률·클로즈데이트), `CRO-deal`(단건 딜+연관 활동), `CRO-market`(리드 소스·폼 전환·company 기업 속성).
- **인증:** Private App Access Token (`HUBSPOT_ACCESS_TOKEN`). 스코프: `crm.objects.deals.read`, `crm.objects.companies.read`, `crm.objects.contacts.read`.

### Salesforce (CRM)
- **필요 능력:** SOQL 쿼리(Opportunity, Account, Contact, Lead, OpportunityLineItem, OpportunityHistory, Task/Event), 오브젝트 describe.
- **쓰는 스킬:** `CRO-forecast`(Opportunity StageName/Amount/CloseDate/Probability/ForecastCategory), `CRO-deal`(단건 Opportunity+관련 Task/Event), `CRO-market`(Account 산업/규모/지역), `CRO-coaching`(Activity 지표).
- **대표 SOQL 예:**
  - 오픈 파이프라인: `SELECT Id,Name,Amount,StageName,CloseDate,Probability,ForecastCategory,OwnerId FROM Opportunity WHERE IsClosed=false`
  - 단건 딜: `SELECT ... FROM Opportunity WHERE Id='006...'` + `SELECT Subject,ActivityDate FROM Task WHERE WhatId='006...'`
- **인증:** OAuth 또는 username+password+security token (`SALESFORCE_*`).

### Gong (대화 인텔리전스)
- **필요 능력:** calls 목록/검색(기간·계정·딜 기준), call 상세, transcript(스크립트), trackers/키워드.
- **쓰는 스킬:** `CRO-deal`(통화에서 3 Whys·MEDDPICC 자동 채점), `CRO-deal`(딜 관련 통화에서 챔피언/EB 언급·리스크 추출), `CRO-coaching`(통화 기반 스킬 진단).
- **인증:** Access Key + Secret (`GONG_ACCESS_KEY`, `GONG_ACCESS_KEY_SECRET`).

### Product/Billing (사용량·청구)
- **필요 능력:** account별 사용량, activation event, seats/licenses, invoices, ARR/MRR, renewal date, expansion/contraction, cohort retention.
- **쓰는 스킬:** `CRO-account`(리텐션·NRR·LIR), `CRO-forecast`(컨슘션 포캐스트), `CRO-market`(활성화 기반 ICP), `CRO-org`(보상/쿼터의 수익성 검증).
- **주의:** 청구·계약정보는 민감하다. 필요한 집계 수준으로만 출력한다.

### Company Knowledge (사내 문서·대화)
- **필요 능력:** 문서/메시지 검색, 문서 상세 읽기, 최신순 정렬, 링크/제목/수정일 확인.
- **대표 질의:** `pricing policy`, `discount approval`, `ICP`, `FY plan`, `board deck`, `QBR`, `sales playbook`, `compensation plan`, `quota`, `renewal policy`, `case study`, `win loss`.
- **쓰는 스킬:** 모든 `CRO-*`. 특히 `CRO-org`(보상·조직·리더십), `CRO-market`(ICP·메시지·캠페인), `CRO-deal`(고객 사례·가격정책), `CRO-account`(QBR·갱신정책).
- **주의:** Slack/메일은 소문과 노이즈가 섞인다. 공식 문서나 CRM 데이터로 교차검증한다.

## 3. MCP 탐색 출력 규약

스킬이 MCP를 사용했다면 답변 첫 줄 또는 근거 섹션에 다음 중 필요한 만큼 남긴다.

```text
데이터 소스: [MCP:Salesforce Opportunity + Gong calls + Notion pricing docs] [컨텍스트:.cro/context.md]
조회 근거: Opportunity open pipeline, Calls last 90d, "FY26 Pricing Policy" 문서
```

도구는 있으나 권한/검색결과가 없으면 다음처럼 말한다.

```text
데이터 소스: [MCP 연결됨: Salesforce, Notion] [결과 부족: 해당 account/call 없음] [자문 모드 병행]
```

## 4. 안전·정확성 규칙

- **읽기 전용 우선.** CRM 레코드를 자동으로 쓰기/수정하지 않는다. 쓰기(예: 딜 스테이지 변경, 노트 작성)는 사용자가 명시적으로 요청할 때만, 확인 후.
- **PII 최소화.** 필요한 필드만 조회하고, 출력에 개인정보를 불필요하게 노출하지 않는다.
- **데이터 없으면 지어내지 않는다.** 쿼리 결과가 비면 "해당 조건에 데이터 없음"이라 말하고 자문 모드로 전환.
- **표기.** 어떤 오브젝트/쿼리로 무엇을 가져왔는지 한 줄로 남긴다(재현성).
- **권위 순서.** 같은 주제에서 `공식 정책 문서 > CRM/청구 데이터 > 콜/Slack 정성 신호 > 오래된 플레이북 > 일반 프레임워크` 순으로 본다. 단, 실제 데이터가 정책과 다르면 둘 다 제시한다.
- **쓰기 금지 기본값.** MCP에 write/update/create 도구가 있어도 사용자가 명시적으로 요청하기 전에는 호출하지 않는다.

## 5. 설정 방법 (사용자 안내)

MCP 서버는 `~/.claude/mcp.json`(전역) 또는 프로젝트 루트 `.mcp.json`에 등록한다. 템플릿: 이 스위트의 `.mcp.json.template`.

```jsonc
{
  "mcpServers": {
    "hubspot":    { "command": "npx", "args": ["-y", "@hubspot/mcp-server"],
                    "env": { "PRIVATE_APP_ACCESS_TOKEN": "${HUBSPOT_ACCESS_TOKEN}" } },
    "salesforce": { "command": "npx", "args": ["-y", "@tsmztech/mcp-server-salesforce"],
                    "env": { "SALESFORCE_USERNAME": "${SF_USER}", "SALESFORCE_PASSWORD": "${SF_PASS}",
                             "SALESFORCE_TOKEN": "${SF_TOKEN}" } },
    "gong":       { "command": "npx", "args": ["-y", "gong-mcp"],
                    "env": { "GONG_ACCESS_KEY": "${GONG_KEY}", "GONG_ACCESS_KEY_SECRET": "${GONG_SECRET}" } }
  }
}
```

> 서버 패키지명·툴 구성은 벤더/커뮤니티 배포에 따라 바뀔 수 있다. 위는 **시작점 템플릿**이며,
> 실제 연결 후에는 세션 도구 목록에서 노출된 툴 이름을 확인해 사용한다(1번 절차).
> 자격 증명은 절대 스킬 파일이나 저장소에 커밋하지 말고 환경변수/시크릿 매니저로 주입한다.

Company Knowledge MCP는 조직마다 다르다. Notion, Google Drive, Confluence, SharePoint, Slack, Jira/Linear 중 실제로 쓰는 서버를 추가하고, 읽기 권한부터 시작한다.
