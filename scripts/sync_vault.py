"""옵시디언 볼트 전체를 content/로 복사한다. private 태그가 붙은 노트는 복사하지 않는다.

사용법: python3 scripts/sync_vault.py <볼트 경로> [--dry-run]

- 노트(.md, .base, .canvas)는 private 태그가 없으면 모두 올린다.
  태그는 frontmatter의 tags(목록이나 문자열)와 본문의 #private 둘 다 본다.
- 이미지 같은 첨부 파일은 공개되는 노트가 실제로 쓰는 것만 올린다.
- Templates 폴더와 숨김 폴더(.obsidian, .trash 등)는 올리지 않는다.
- 볼트 루트에 index.md가 없으면 Blog/index.md를 사이트 첫 화면으로 쓴다.
"""
import re
import shutil
import sys
from pathlib import Path

PRIVATE_TAG = "private"
SKIP_DIRS = {"Templates"}
NOTE_EXTS = {".md", ".base", ".canvas"}
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


def walk(vault):
    for p in sorted(vault.rglob("*")):
        rel = p.relative_to(vault)
        if any(part.startswith(".") for part in rel.parts) or rel.parts[0] in SKIP_DIRS:
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
        if p.suffix in NOTE_EXTS:
            (private if is_private(p) else notes).append((p, rel))
        else:
            by_name.setdefault(p.name, (p, rel))

    has_root_index = any(rel == Path("index.md") for _, rel in notes)
    targets = []
    for p, rel in notes:
        if not has_root_index and rel == Path("Blog/index.md"):
            rel = Path("index.md")
        targets.append((p, rel))

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
