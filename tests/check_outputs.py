#!/usr/bin/env python3
"""드라이런 산출물이 각 스킬의 '출력 형식' 계약을 충족하는지 검증.

scenarios/CRO-deal-output.md, CRO-market-output.md 가 스킬이 약속한 필수 요소를
실제로 담고 있는지 확인한다(프롬프트 스킬의 스모크 테스트). 종료코드 0=통과.
"""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (파일, [필수 요소 라벨: [허용 문자열들 중 하나 이상 포함]])
CHECKS = {
    "scenarios/CRO-deal-output.md": {
        "데이터 소스 표기": ["데이터 소스:"],
        "딜 스냅샷": ["스냅샷"],
        "MEDDPICC 점수표": ["MEDDPICC"],
        "8요소 전부": ["Metrics", "Economic Buyer", "Decision Criteria", "Decision Process",
                     "Identify Pain", "Paper Process", "Champion", "Competition"],
        "3 Whys 게이트": ["3 Whys", "Why buy", "Why us", "Why now"],
        "챔피언 vs 코치": ["챔피언", "코치"],
        "언블록 계획": ["언블록"],
        "EB 6질문 스크립트": ["6질문", "잠금 질문"],
        "포캐스트 판정": ["포캐스트 판정"],
        "핸드오프": ["핸드오프"],
        "근거 없는 수치 회피(정량화 갭 명시)": ["수치 없음", "정량화"],
    },
    "scenarios/CRO-market-output.md": {
        "데이터 소스 표기": ["데이터 소스:"],
        "3채널 진단(씨앗/그물/창)": ["씨앗", "그물", "창"],
        "Seeds/Nets/Spears 라벨": ["Seeds", "Nets", "Spears"],
        "아웃바운드 4조건": ["4조건"],
        "권장 믹스": ["권장 믹스", "믹스"],
        "30/60/90 플레이": ["30일", "60일", "90일"],
        "세일즈-마케팅 SLA": ["SLA"],
        "안티패턴": ["안티패턴"],
        "핸드오프": ["핸드오프"],
    },
    "scenarios/CRO-context-branching.md": {
        "동일 질문": ["MEDDPICC로 전부 관리해야"],
        "맥락 A(PLG/트랜잭셔널)": ["PLG", "트랜잭셔널"],
        "맥락 B(엔터프라이즈/위원회)": ["엔터프라이즈", "위원회"],
        "저장 카드 로드(재사용)": [".cro/context.md 로드", "재질문 없음"],
        "카드 없을 때 인테이크": ["5축 인테이크"],
        "분기: 경량 vs 풀": ["과잉", "풀 가동"],
        "분기 근거(상충 규약)": ["conflict-resolution.md"],
    },
}

def main() -> int:
    total_fail = 0
    for rel, checks in CHECKS.items():
        path = os.path.join(HERE, rel)
        print(f"\n== {rel} ==")
        if not os.path.isfile(path):
            print(f"  [FAIL] 파일 없음")
            total_fail += 1
            continue
        text = open(path, encoding="utf-8").read()
        for label, needles in checks.items():
            missing = [n for n in needles if n not in text]
            if missing:
                print(f"  [FAIL] {label} — 누락: {missing}")
                total_fail += 1
            else:
                print(f"  [ OK ] {label}")
    print()
    if total_fail:
        print(f"스모크 테스트 실패: {total_fail}개 항목")
        return 1
    print("스모크 테스트 통과: 모든 산출물이 출력 계약을 충족")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
