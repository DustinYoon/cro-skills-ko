#!/usr/bin/env python3
"""SessionStart 훅 스모크 테스트.

hooks/session-start 를 실행해서:
  - 유효한 JSON 을 내보내는가
  - Claude Code SessionStart 스키마(hookSpecificOutput.additionalContext)를 따르는가
  - additionalContext 에 라우팅 규칙·불변 규율 핵심 문구가 들어 있는가
를 확인한다. 종료코드 0=통과.
"""
from __future__ import annotations
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOOK = os.path.join(ROOT, "hooks", "session-start")

# additionalContext 에 반드시 있어야 할 신호(라우팅 + 불변 규율).
MUST_CONTAIN = [
    "CRO",              # 스위트 식별
    "1%",               # 1% 라우팅 규칙
    "데이터 소스",       # 첫 줄 소스 표기 규율
    "지어내지",          # 수치 날조 금지
    "느리게",            # 진단 먼저(전술 금지)
]


def main() -> int:
    if not os.path.isfile(HOOK):
        print(f"[FAIL] 훅 스크립트 없음: {HOOK}")
        return 1

    try:
        proc = subprocess.run(
            ["bash", HOOK],
            input='{"source":"startup"}',
            capture_output=True, text=True, timeout=15,
        )
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] 훅 실행 예외: {e}")
        return 1

    if proc.returncode != 0:
        print(f"[FAIL] 훅 종료코드 {proc.returncode}\n{proc.stderr}")
        return 1

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        print(f"[FAIL] 출력이 유효한 JSON 아님: {e}\n--- stdout ---\n{proc.stdout[:500]}")
        return 1

    fails = 0
    hso = data.get("hookSpecificOutput", {})
    if hso.get("hookEventName") != "SessionStart":
        print(f"[FAIL] hookEventName != SessionStart (got {hso.get('hookEventName')!r})")
        fails += 1
    ctx = hso.get("additionalContext", "")
    if not ctx:
        print("[FAIL] additionalContext 비어 있음")
        fails += 1
    for needle in MUST_CONTAIN:
        if needle not in ctx:
            print(f"[FAIL] additionalContext 에 '{needle}' 없음")
            fails += 1
        else:
            print(f"  [ OK ] '{needle}' 포함")

    print()
    if fails:
        print(f"훅 스모크 테스트 실패: {fails}개 항목")
        return 1
    print("훅 스모크 테스트 통과: SessionStart 부트스트랩 정상")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
