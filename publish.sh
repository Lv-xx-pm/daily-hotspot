#!/bin/zsh
# 渲染网页并发布到 GitHub Pages(pages 分支)
cd "$(dirname "$0")" || exit 1
python3 render.py || exit 1
git add index.html data
git commit -qm "更新热点库 $(date +%F)" || exit 0
git push -q origin pages
