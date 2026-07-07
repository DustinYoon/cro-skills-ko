#!/usr/bin/env python3
"""슬래시 커맨드(저마찰 진입점) 구조 검증.

commands/*.md 각 파일이:
  - frontmatter 에 description + argument-hint 키를 갖는가
  - 본문에서 대상 CRO 스킬을 정확히 참조하는가
  - 아티팩트 전달용 $ARGUMENTS 를 사용하는가
  - 아티팩트 우선 경로로 진입하도록 지시하는가
  - fan-out 커맨드(forecast/market/cro)는 병렬 규약을 언급하는가
를 확인한다. 종료코드 0=통과, 1=실패.
"""
from __future__ import annotations
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CMD_DIR = os.path.join(ROOT, "commands")

# 커맨드 파일 -> 참조해야 하는 스킬명
EXPECTED = {
    "cro.md": "CRO",
    "cro-deal.md": "CRO-deal",
    "cro-forecast.md": "CRO-forecast",
    "cro-market.md": "CRO-market",
    "cro-account.md": "CRO-account",
    "cro-coaching.md": "CRO-coaching",
    "cro-org.md": "CRO-org",
}
# fan-out 을 언급해야 하는 커맨드(오케스트레이터 + fan-out 홈 스킬)
FANOUT_CMDS = {"cro.md", "cro-forecast.md", "cro-market.md"}
FANOUT_MARKERS = ["병렬", "fan-out"]


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end].strip("\n"), text[end + 4:]


def fm_has_value(fm: str, key: str) -> bool:
    """키가 있고 값이 비어 있지 않은가 (빈 description:/argument-hint: 는 무효)."""
    return re.search(rf"^{re.escape(key)}\s*:\s*\S", fm, re.MULTILINE) is not None


def main() -> int:
    if not os.path.isdir(CMD_DIR):
        print(f"[FAIL] commands 디렉토리 없음: {CMD_DIR}")
        return 1

    present = {f for f in os.listdir(CMD_DIR) if f.endswith(".md")}
    total_errors = 0
    print(f"검증 대상 {len(EXPECTED)}개 커맨드 @ {CMD_DIR}\n")

    # 기대 커맨드가 모두 존재하는가
    for missing in sorted(set(EXPECTED) - present):
        print(f"[FAIL] {missing} — 파일 없음")
        total_errors += 1

    for fname in sorted(EXPECTED):
        if fname not in present:
            continue
        errors = []
        skill = EXPECTED[fname]
        with open(os.path.join(CMD_DIR, fname), encoding="utf-8") as f:
            text = f.read()
        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append("frontmatter(--- ... ---) 없음")
        else:
            if not fm_has_value(fm, "description"):
                errors.append("description 키 없음/값 비어 있음")
            if not fm_has_value(fm, "argument-hint"):
                errors.append("argument-hint 키 없음/값 비어 있음")
        if "$ARGUMENTS" not in body:
            errors.append("$ARGUMENTS 미사용(아티팩트 전달 불가)")
        if f"`{skill}`" not in body:
            errors.append(f"대상 스킬 `{skill}` 참조 없음")
        if "아티팩트 우선" not in body:
            errors.append("'아티팩트 우선' 경로 지시 없음")
        if fname in FANOUT_CMDS and not any(m in body for m in FANOUT_MARKERS):
            errors.append("fan-out 커맨드인데 병렬 규약 언급 없음")

        if errors:
            total_errors += len(errors)
            print(f"[FAIL] {fname}")
            for e in errors:
                print(f"        - {e}")
        else:
            print(f"[ OK ] {fname} -> {skill}")

    print()
    if total_errors:
        print(f"검증 실패: {total_errors}개 문제")
        return 1
    print(f"검증 통과: {len(EXPECTED)}개 커맨드 모두 정상")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
