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
echo "다음 단계:"
echo "  1) (선택) MCP 연결: $SRC_ROOT/.mcp.json.template 를 ~/.claude/mcp.json 또는 프로젝트 .mcp.json 에 병합"
echo "  2) (선택) 사내 세일즈 자료 연결: export CRO_CORPUS_DIR=/path/to/notes"
echo "  3) 대화에서 'GTM', '리드 제너레이션', '딜 블로커', '파이프라인 설계', '캠페인' 등으로 스킬 호출"
echo "  4) 검증: python3 $SRC_ROOT/validate_skills.py"
