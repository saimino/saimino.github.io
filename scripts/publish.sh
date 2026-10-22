#!/bin/sh
# 블로그 변경사항을 GitHub에 올린다. 사용법: sh scripts/publish.sh "커밋 메시지"
set -e
cd "$(dirname "$0")/.."
git add -A
git commit -m "${1:-Update posts}" || true
git push -u origin main
open "https://github.com/saimino/saimino.github.io/actions"
