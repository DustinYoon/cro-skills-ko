#!/usr/bin/env python3
"""CRO GTM 스킬 스위트 구조 검증기 (외부 의존성 없음).

각 skills/<name>/SKILL.md 에 대해:
  - YAML frontmatter 존재 + name/description/allowed-tools 키
  - frontmatter의 name 이 폴더명과 일치
  - description 에 'Triggers'(또는 '트리거') 포함
  - 본문에 필수 섹션 존재 (오케스트레이터 제외한 기능 스킬)
  - 본문에서 참조하는 ~/.claude/skills/CRO/references/<f>.md 가 이 스위트에 실제 존재
사용: python3 validate_skills.py [스위트_루트]   (기본: 스크립트 위치)
종료코드: 0=통과, 1=실패.
"""
from __future__ import annotations
import os, re, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__))
# dev 레이아웃(<root>/skills/<name>) 또는 설치 레이아웃(<root>/<name>, 즉 ~/.claude/skills) 모두 지원.
_nested = os.path.join(ROOT, "skills")
SKILLS_DIR = _nested if os.path.isdir(os.path.join(_nested, "CRO")) else ROOT
REF_DIR = os.path.join(SKILLS_DIR, "CRO", "references")

# 기능 스킬 본문 필수 섹션 (오케스트레이터 CRO 는 예외)
# '철칙' = Iron Law 한 줄(압박 하에서도 지키는 불변 규율), '합리화 차단' = 변명→현실 표.
# '아티팩트 우선' = 저마찰 진입점(URL·전사·CSV·파일을 바로 받는 fast path).
REQUIRED_SECTIONS = ["철칙", "아티팩트 우선", "참조", "데이터 소스", "워크플로",
                     "출력 형식", "안티패턴", "합리화 차단", "핸드오프"]
# Task 툴을 선언한 스킬(오케스트레이터·forecast·market)은 fan-out 규약을 본문에 명시해야 한다.
FANOUT_MARKERS = ["병렬 처리", "fan-out"]
REF_LINK_RE = re.compile(r"~/\.claude/skills/CRO/references/([A-Za-z0-9._-]+\.md)")

def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[3:end].strip("\n")
    body = text[end + 4:]
    return fm, body

def fm_get_scalar(fm: str, key: str):
    m = re.search(rf"^{re.escape(key)}\s*:\s*(.*)$", fm, re.MULTILINE)
    return m.group(1).strip() if m else None

def fm_has_key(fm: str, key: str) -> bool:
    return re.search(rf"^{re.escape(key)}\s*:", fm, re.MULTILINE) is not None

def main() -> int:
    if not os.path.isdir(SKILLS_DIR):
        print(f"[FAIL] skills dir 없음: {SKILLS_DIR}")
        return 1
    # CRO 스위트 스킬만 검증 (설치 디렉토리엔 다른 스킬도 있으므로 CRO/CRO-* 로 스코프).
    skills = sorted(
        d for d in os.listdir(SKILLS_DIR)
        if (d == "CRO" or d.startswith("CRO-")) and ".bak" not in d
        and os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
    )
    if not skills:
        print(f"[FAIL] SKILL.md 를 가진 스킬이 없음: {SKILLS_DIR}")
        return 1

    available_refs = set(os.listdir(REF_DIR)) if os.path.isdir(REF_DIR) else set()
    total_errors = 0
    print(f"검증 대상 {len(skills)}개 스킬 @ {SKILLS_DIR}\n")

    for name in skills:
        errors = []
        path = os.path.join(SKILLS_DIR, name, "SKILL.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append("frontmatter(--- ... ---) 없음")
        else:
            fm_name = fm_get_scalar(fm, "name")
            if fm_name != name:
                errors.append(f"name '{fm_name}' != 폴더명 '{name}'")
            if not fm_has_key(fm, "description"):
                errors.append("description 키 없음")
            elif not re.search(r"[Tt]riggers|트리거", fm):
                errors.append("description 에 Triggers 문구 없음")
            if not fm_has_key(fm, "allowed-tools"):
                errors.append("allowed-tools 키 없음")

        # 기능 스킬만 섹션 검사 (오케스트레이터 CRO 제외)
        if name != "CRO":
            for sec in REQUIRED_SECTIONS:
                if sec not in body:
                    errors.append(f"필수 섹션 누락: '{sec}'")

        # Task 툴을 선언했으면 fan-out 규약이 본문에 있어야 한다 (문서 없는 병렬 실행 방지)
        declares_task = fm is not None and re.search(r"^\s*-\s*Task\s*$", fm, re.MULTILINE)
        if declares_task and not any(m in body for m in FANOUT_MARKERS):
            errors.append("allowed-tools 에 Task 선언했으나 fan-out 규약(병렬 처리) 본문 없음")

        # 참조 무결성: 본문이 가리키는 reference 파일이 실제 존재하는가
        for ref in sorted(set(REF_LINK_RE.findall(text))):
            if ref not in available_refs:
                errors.append(f"참조 파일 없음: references/{ref}")

        if errors:
            total_errors += len(errors)
            print(f"[FAIL] {name}")
            for e in errors:
                print(f"        - {e}")
        else:
            print(f"[ OK ] {name}")

    print()
    if total_errors:
        print(f"검증 실패: {total_errors}개 문제")
        return 1
    print(f"검증 통과: {len(skills)}개 스킬 모두 정상")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
