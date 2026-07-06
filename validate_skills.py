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
REQUIRED_SECTIONS = ["참조", "데이터 소스", "워크플로", "출력 형식", "안티패턴", "핸드오프"]
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
