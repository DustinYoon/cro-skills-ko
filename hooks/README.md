# CRO Skills — SessionStart 부트스트랩 훅

이 훅은 CRO 스킬 스위트가 **"사용자가 `/CRO`를 기억해서 칠 때만"이 아니라, 세일즈·GTM 신호가
보이는 순간 자동으로 발화**하게 만든다. `obra/superpowers`의 `using-superpowers` 부트스트랩과 같은 방식이다.

훅이 없으면 스킬은 디스크에 있어도 잘 호출되지 않는다(트리거 키워드가 정확히 걸릴 때만 발화). 훅이 있으면
매 세션 시작·`/clear`·컨텍스트 압축(`compact`) 때 `BOOTSTRAP.md`의 라우팅 규칙과 불변 규율이 컨텍스트에 주입된다.

## 구성 파일

| 파일 | 역할 |
|:--|:--|
| `BOOTSTRAP.md` | 주입되는 내용 — 라우팅 규칙(1% 규칙) + 데이터 소스 표기·수치 날조 금지 등 불변 규율 |
| `session-start` | `BOOTSTRAP.md`를 읽어 Claude Code SessionStart 훅 JSON으로 내보내는 셸 스크립트 |
| `hooks.json` | 플러그인 설치 시 자동 로드되는 훅 설정(matcher: `startup\|clear\|compact`) |

## 설치

### 방법 1 — 플러그인 설치 (권장)

Claude Code 플러그인으로 설치하면 `hooks.json`이 자동 로드된다(`${CLAUDE_PLUGIN_ROOT}`가 플러그인 경로로 치환, `settings.json` 수정 없음). 별도 훅 설치가 필요 없다.

```bash
claude plugin marketplace add DustinYoon/cro-skills-ko
claude plugin install cro-skills-ko@cro-skills-ko
```

### 방법 2 — `install.sh` (로컬 클론에서)

리포지토리 루트의 `install.sh`가 스킬을 설치하면서 이 훅을 처리한다:

1. `hooks/`를 **`~/.claude/cro-hooks/`로 복사**한다(클론을 옮기거나 지워도 훅이 계속 동작 — self-contained).
2. `~/.claude/settings.json`에 그 복사본 경로를 **멱등적으로** 병합한다(이미 있으면 건너뜀). 기존 설정이 손상(JSON 파싱 불가)돼 있으면 덮어쓰지 않고 `*.corrupt.bak.<stamp>`로 백업한 뒤 중단하며, 성공 시에도 `settings.json.bak.<stamp>`를 남기고 임시파일 원자적 치환으로 쓴다.

훅을 원치 않으면:

```bash
CRO_INSTALL_HOOK=0 bash install.sh
```

> **`npx skills`로 설치한 경우:** `npx skills add …`는 `skills/`만 복사하고 `hooks/`는 가져오지 않는다. 즉 **자동 발화 훅은 설치되지 않는다.** 플러그인으로 설치하거나(방법 1), 로컬 클론에서 `bash install.sh`를 돌리거나, 아래 방법 3으로 수동 등록해야 자동 발화가 켜진다.

### 방법 3 — 수동으로 `~/.claude/settings.json`에 추가

`session-start`의 **절대 경로**를 넣는다(설치 위치에 맞게 수정):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          { "type": "command", "command": "/ABSOLUTE/PATH/TO/cro-skills/hooks/session-start" }
        ]
      }
    ]
  }
}
```

설정 후 Claude Code 세션을 재시작한다.

## 동작 확인

```bash
echo '{}' | bash hooks/session-start
# → {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"# CRO Revenue Skills ..."}}

python3 tests/check_hook.py     # 스모크 테스트
```

## 이식성

`session-start`는 `additionalContext`를 Claude Code 스키마로 내보낸다. Cursor·Copilot 등 다른 하네스는
필드명이 다를 수 있으니(`additional_context` 등) 해당 하네스 문서를 확인해 래핑을 바꾼다.
python3가 없으면 스크립트는 조용히 no-op 하며 세션을 막지 않는다.
