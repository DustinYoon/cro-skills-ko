#!/usr/bin/env bash
# CRO GTM 스킬 스위트 설치기.
# skills/<name>/ 를 ~/.claude/skills/<name>/ 로 복사한다 (기존 폴더는 타임스탬프 백업).
# 사용: bash install.sh [설치_대상_스킬_루트]   (기본: ~/.claude/skills)
set -euo pipefail

SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_SKILLS="$SRC_ROOT/skills"
DEST="${1:-$HOME/.claude/skills}"
STAMP="$(date +%Y%m%d-%H%M%S)"

if [ ! -d "$SRC_SKILLS" ]; then
  echo "ERROR: skills 디렉토리를 찾을 수 없음: $SRC_SKILLS" >&2
  exit 1
fi

mkdir -p "$DEST"
echo "설치 대상: $DEST"
echo

copy_one() {
  local name="$1" src="$SRC_SKILLS/$1" dst="$DEST/$1"
  if [ -d "$dst" ]; then
    mv "$dst" "$dst.bak.$STAMP"
    echo "  백업: $name -> $name.bak.$STAMP"
  fi
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$src/" "$dst/"
  else
    mkdir -p "$dst" && cp -R "$src/." "$dst/"
  fi
  echo "  설치: $name"
}

count=0
for dir in "$SRC_SKILLS"/*/; do
  [ -f "${dir}SKILL.md" ] || continue
  copy_one "$(basename "$dir")"
  count=$((count + 1))
done

echo
echo "완료: ${count}개 스킬 설치됨 -> $DEST"
echo

# ── SessionStart 훅 설치 (선택, 기본 on) ──────────────────────────────────────
# CRO 스킬이 세일즈·GTM 신호에 자동 발화하도록 ~/.claude/settings.json 에 훅을 멱등적으로 병합.
# 훅 스크립트는 클론 위치에 의존하지 않게 ~/.claude/cro-hooks/ 로 복사한다(클론을 옮기거나 지워도 동작).
# 끄려면: CRO_INSTALL_HOOK=0 bash install.sh
if [ "${CRO_INSTALL_HOOK:-1}" = "1" ] && [ -f "$SRC_ROOT/hooks/session-start" ]; then
  if command -v python3 >/dev/null 2>&1; then
    # 1) 훅을 사용자 홈의 안정 경로로 복사(BOOTSTRAP.md 포함) — self-contained.
    HOOK_DIR="$HOME/.claude/cro-hooks"
    mkdir -p "$HOME/.claude"
    if command -v rsync >/dev/null 2>&1; then
      rsync -a "$SRC_ROOT/hooks/" "$HOOK_DIR/"
    else
      mkdir -p "$HOOK_DIR" && cp -R "$SRC_ROOT/hooks/." "$HOOK_DIR/"
    fi
    chmod +x "$HOOK_DIR/session-start" 2>/dev/null || true
    SETTINGS="$HOME/.claude/settings.json"
    HOOK_CMD="$HOOK_DIR/session-start"
    # 2) settings.json 에 멱등적으로 병합 (손상 파일은 백업 후 중단, 성공 경로는 백업+원자적 치환).
    set +e
    RESULT="$(python3 - "$SETTINGS" "$HOOK_CMD" "$STAMP" <<'PY'
import json, os, sys
settings_path, hook_cmd, stamp = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(os.path.dirname(settings_path) or ".", exist_ok=True)

raw = None
if os.path.exists(settings_path):
    with open(settings_path, encoding="utf-8") as f:
        raw = f.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        # 손상된 기존 설정을 절대 덮어쓰지 않는다 — 백업하고 중단.
        with open(f"{settings_path}.corrupt.bak.{stamp}", "w", encoding="utf-8") as f:
            f.write(raw)
        print("ERROR_CORRUPT", end="")
        sys.exit(3)
else:
    data = {}

if not isinstance(data, dict):
    print("ERROR_SHAPE", end="")
    sys.exit(3)

hooks = data.setdefault("hooks", {})
if not isinstance(hooks, dict):
    print("ERROR_SHAPE", end="")
    sys.exit(3)
starts = hooks.setdefault("SessionStart", [])
if not isinstance(starts, list):
    print("ERROR_SHAPE", end="")
    sys.exit(3)

def has_cmd(entries):
    for e in entries:
        for h in (e.get("hooks", []) if isinstance(e, dict) else []):
            if isinstance(h, dict) and h.get("command") == hook_cmd:
                return True
    return False

if has_cmd(starts):
    print("SKIP", end="")
    sys.exit(0)

starts.append({
    "matcher": "startup|clear|compact",
    "hooks": [{"type": "command", "command": hook_cmd}],
})

# 성공 경로: 기존 파일 백업 → 임시파일에 쓰고 원자적 치환(중단돼도 원본 보존).
if raw is not None:
    with open(f"{settings_path}.bak.{stamp}", "w", encoding="utf-8") as f:
        f.write(raw)
tmp = f"{settings_path}.tmp.{stamp}"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
os.replace(tmp, settings_path)
print("ADDED", end="")
PY
)"
    RC=$?
    set -e
    case "$RESULT" in
      ADDED) echo "  훅: SessionStart 부트스트랩을 $SETTINGS 에 추가 (스크립트: $HOOK_CMD)";;
      SKIP)  echo "  훅: SessionStart 부트스트랩 이미 설치됨 — 건너뜀 ($HOOK_CMD)";;
      ERROR_CORRUPT) echo "  훅: 기존 settings.json 손상 → $SETTINGS.corrupt.bak.$STAMP 로 백업하고 병합 중단. hooks/README.md 수동 설치 참고" >&2;;
      *) echo "  훅: settings.json 병합 실패(rc=$RC) — hooks/README.md 의 수동 설치 참고" >&2;;
    esac
  else
    echo "  훅: python3 없음 — hooks/README.md 의 수동 설치 참고" >&2
  fi
  echo
fi

# ── 슬래시 커맨드 설치 (선택, 기본 on) ───────────────────────────────────────
# 저마찰 진입점: /cro-deal <url·전사·파일> 처럼 아티팩트를 바로 넘겨 스킬을 부른다.
# commands/*.md 를 ~/.claude/commands/ 로 복사한다(같은 이름 있으면 타임스탬프 백업).
# 끄려면: CRO_INSTALL_COMMANDS=0 bash install.sh
if [ "${CRO_INSTALL_COMMANDS:-1}" = "1" ] && [ -d "$SRC_ROOT/commands" ]; then
  CMD_DEST="$HOME/.claude/commands"
  mkdir -p "$CMD_DEST"
  cmd_count=0
  for cmd in "$SRC_ROOT/commands"/*.md; do
    [ -f "$cmd" ] || continue
    base="$(basename "$cmd")"
    dst="$CMD_DEST/$base"
    # 내용이 같으면 백업 없이 건너뛰고, 다르면 기존본을 백업한 뒤 갱신.
    # (cmp 부재 환경에선 비교를 건너뛰고 항상 백업+갱신 — 매 실행 백업이 쌓일 수 있음.)
    if [ -f "$dst" ] && command -v cmp >/dev/null 2>&1 && cmp -s "$cmd" "$dst"; then
      continue
    fi
    if [ -f "$dst" ]; then
      cp "$dst" "$dst.bak.$STAMP"
      echo "  커맨드 백업: $base -> $base.bak.$STAMP"
    fi
    cp "$cmd" "$dst"
    cmd_count=$((cmd_count + 1))
  done
  echo "  커맨드: ${cmd_count}개 설치/갱신 -> $CMD_DEST (/cro-deal, /cro-forecast, … )"
  echo
fi

echo "다음 단계:"
echo "  1) Claude Code 세션 재시작"
echo "  2) (선택) MCP 연결: $SRC_ROOT/.mcp.json.template 를 ~/.claude/mcp.json 또는 프로젝트 .mcp.json 에 병합"
echo "  3) (선택) 사내 세일즈 자료 연결: export CRO_CORPUS_DIR=/path/to/notes"
echo "  4) 대화에서 '/CRO' 또는 'GTM', '리드 제너레이션', '딜 블로커', '파이프라인 설계', '캠페인' 등으로 스킬 호출"
echo "     저마찰 진입: '/cro-deal <Gong URL>' · '/cro-forecast pipeline.csv' 처럼 아티팩트를 바로 전달"
echo "  5) 검증: python3 $SRC_ROOT/validate_skills.py"
echo
echo "GitHub에서 바로 설치하려면:"
echo "  npx skills add Diseon/cro-skills-ko --skill CRO CRO-market CRO-deal CRO-account CRO-forecast CRO-org CRO-coaching -a claude-code -g"
