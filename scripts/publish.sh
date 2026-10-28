#!/bin/sh
# 옵시디언 볼트 전체를 content/로 가져와 GitHub에 올린다. private 태그가 붙은 노트는 빠진다.
# 사용법: sh scripts/publish.sh "커밋 메시지"
#         sh scripts/publish.sh --dry-run   (올라갈 목록만 확인)
set -e
cd "$(dirname "$0")/.."

VAULT="${VAULT:-$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Keep going}"

if [ "$1" = "--dry-run" ]; then
  python3 scripts/sync_vault.py "$VAULT" --dry-run
  exit 0
fi

python3 scripts/sync_vault.py "$VAULT"

git add -A
if git diff --cached --quiet; then
  echo "바뀐 내용이 없습니다."
  exit 0
fi
git commit -m "${1:-Update notes}"
git push -u origin main
echo "올렸습니다. 2~3분 뒤 https://saimino.github.io 에 반영됩니다."
