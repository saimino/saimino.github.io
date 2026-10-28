#!/bin/sh
# 옵시디언 볼트의 Blog 폴더를 content/로 가져와 GitHub에 올린다.
# 사용법: sh scripts/publish.sh "커밋 메시지"
set -e
cd "$(dirname "$0")/.."

VAULT="${VAULT:-$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Keep going}"
SRC="$VAULT/Blog"
[ -d "$SRC" ] || { echo "볼트의 Blog 폴더를 찾을 수 없습니다: $SRC" >&2; exit 1; }

# iCloud에서 아직 내려받지 않은 파일이 있으면 먼저 받는다
if find "$SRC" -name '.*.icloud' | grep -q .; then
  brctl download "$SRC" 2>/dev/null || true
  echo "iCloud에서 아직 받지 않은 파일이 있습니다. 잠시 후 다시 실행하세요." >&2
  exit 1
fi

rsync -a --delete --exclude '.DS_Store' "$SRC/" content/

# Blog 글에 붙인 이미지가 볼트의 다른 폴더(예: Attachments)에 있으면 함께 복사한다
python3 - "$VAULT" <<'EOF'
import re, shutil, sys
from pathlib import Path

vault, content = Path(sys.argv[1]), Path("content")
have = {p.name for p in content.rglob("*") if p.is_file()}
want = set()
for md in content.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    want |= {m.split("|")[0].split("#")[0].strip() for m in re.findall(r"!\[\[([^\]]+)\]\]", text)}
    want |= {Path(m).name for m in re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", text) if "://" not in m}
missing = {Path(w).name for w in want} - have
if missing:
    (content / "attachments").mkdir(exist_ok=True)
    for p in vault.rglob("*"):
        if p.name in missing and ".obsidian" not in p.parts and p.is_file():
            shutil.copy2(p, content / "attachments" / p.name)
            missing.discard(p.name)
            print(f"이미지 복사: {p.relative_to(vault)}")
for name in sorted(missing):
    print(f"! 볼트에서 찾지 못한 이미지: {name}", file=sys.stderr)
EOF

git add -A
if git diff --cached --quiet; then
  echo "바뀐 내용이 없습니다."
  exit 0
fi
git commit -m "${1:-Update posts}"
git push -u origin main
echo "올렸습니다. 2~3분 뒤 https://saimino.github.io 에 반영됩니다."
