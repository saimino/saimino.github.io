"""옵시디언 볼트의 Resource 폴더를 content/로 복사한다. private 태그가 붙은 노트는 복사하지 않는다.

사용법: python3 scripts/sync_vault.py <볼트 경로> [--dry-run]

- 올리는 노트는 Resource 폴더 안의 노트뿐이다. 사이트에서는 Resource 단계를 빼고 올린다.
- 사이트 첫 화면 파일(index.md, 전체 글.base)은 볼트가 아니라 이 저장소의 site/ 폴더에 있다.
- 그중 private 태그가 없는 노트(.md, .base, .canvas)를 올린다.
  태그는 frontmatter의 tags(목록이나 문자열)와 본문의 #private 둘 다 본다.
- 이미지 같은 첨부 파일은 공개되는 노트가 실제로 쓰는 것만 올린다.
- 탐색기 정렬 규칙 파일(sortspec.md), 템플릿 폴더(.obsidian/templates.json의 folder)와 숨김 폴더(.obsidian, .trash 등)는 올리지 않는다.
"""
import json
import re
import shutil
import sys
from pathlib import Path

PRIVATE_TAG = "private"
NOTE_EXTS = {".md", ".base", ".canvas"}
# 볼트에서 "Resource" 또는 "3. Resource"처럼 번호가 붙은 Resource 폴더를 올린다
PUBLISH_DIR_PATTERN = re.compile(r"(\d+\.\s*)?Resource")
SITE = Path(__file__).resolve().parent.parent / "site"
CONTENT = Path(__file__).resolve().parent.parent / "content"


def tags_of(text):
    tags = set()
    fm = re.match(r"---\n(.*?)\n---", text, re.S)
    if fm:
        block = fm.group(1)
        m = re.search(r"^tags:[ \t]*(.*)$", block, re.M)
        if m:
            inline = m.group(1).strip()
            if inline:
                tags |= {t.strip(" '\"#") for t in inline.strip("[]").split(",")}
            else:
                rest = block[m.end():]
                for line in rest.split("\n")[1:] if rest.startswith("\n") else rest.split("\n"):
                    item = re.match(r"^\s*-\s*(.+)$", line)
                    if not item:
                        break
                    tags.add(item.group(1).strip(" '\"#"))
        body = text[fm.end():]
    else:
        body = text
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    tags |= set(re.findall(r"(?<![\w&/#\\])#([^\s#,.!?()\[\]]+)", body))
    return {t.lower() for t in tags if t}


def is_private(path):
    if path.suffix != ".md":
        return False
    tags = tags_of(path.read_text(encoding="utf-8", errors="replace"))
    return any(t == PRIVATE_TAG or t.startswith(PRIVATE_TAG + "/") for t in tags)


def template_dir(vault):
    try:
        folder = json.loads((vault / ".obsidian" / "templates.json").read_text(encoding="utf-8")).get("folder")
    except (OSError, ValueError):
        folder = None
    return Path(folder.strip("/")) if folder else Path("Templates")


def walk(vault):
    skip = template_dir(vault)
    for p in sorted(vault.rglob("*")):
        rel = p.relative_to(vault)
        if any(part.startswith(".") for part in rel.parts) or rel.parts[: len(skip.parts)] == skip.parts:
            continue
        if p.is_file():
            yield p, rel


def main():
    vault = Path(sys.argv[1]).expanduser()
    dry = "--dry-run" in sys.argv
    if not vault.is_dir():
        sys.exit(f"볼트를 찾을 수 없습니다: {vault}")

    files = list(walk(vault))
    if any(p.name.endswith(".icloud") for p, _ in files):
        sys.exit("iCloud에서 아직 내려받지 않은 파일이 있습니다. 볼트를 열어 동기화한 뒤 다시 실행하세요.")

    notes, private, by_name = [], [], {}
    for p, rel in files:
        if p.name == "sortspec.md":  # 탐색기 정렬 규칙 파일은 올리지 않는다
            continue
        if p.suffix in NOTE_EXTS:
            if PUBLISH_DIR_PATTERN.fullmatch(rel.parts[0]):
                (private if is_private(p) else notes).append((p, rel))
        else:
            by_name.setdefault(p.name, (p, rel))

    # 사이트에서는 Resource 단계를 빼고 AI, Dev, Math 같은 폴더가 바로 보이게 한다
    targets = [(p, Path(*rel.parts[1:])) for p, rel in notes]
    targets += [(p, p.relative_to(SITE)) for p in sorted(SITE.rglob("*")) if p.is_file()]

    # 공개 노트가 쓰는 첨부 파일만 고른다
    wanted = set()
    for p, _ in targets:
        if p.suffix != ".md":
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        wanted |= {m.split("|")[0].split("#")[0].strip() for m in re.findall(r"!\[\[([^\]]+)\]\]", text)}
        wanted |= {m for m in re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", text) if "://" not in m}
    assets = []
    for w in sorted(wanted):
        hit = by_name.get(Path(w).name)
        if hit:
            assets.append(hit)
        elif Path(w).suffix not in NOTE_EXTS and Path(w).suffix:
            print(f"! 볼트에서 찾지 못한 첨부 파일: {w}", file=sys.stderr)

    print(f"공개 노트 {len(targets)}개, 첨부 파일 {len(assets)}개, private 제외 {len(private)}개")
    for _, rel in private:
        print(f"  제외: {rel}")
    if dry:
        folders = {}
        for _, rel in targets:
            key = rel.parts[0] if len(rel.parts) > 1 else "(루트)"
            folders[key] = folders.get(key, 0) + 1
        for k, v in sorted(folders.items()):
            print(f"  공개: {k} {v}개")
        return

    shutil.rmtree(CONTENT, ignore_errors=True)
    for p, rel in targets + assets:
        dest = CONTENT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)


if __name__ == "__main__":
    main()
