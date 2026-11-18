#!/usr/bin/env python3
"""把 data/*.json 渲染成一个独立网页 index.html(含历史日期切换、分类筛选、搜索)。"""
import json, glob
from pathlib import Path
B=Path(__file__).parent
days={Path(f).stem:json.load(open(f,encoding="utf8"))["items"] for f in sorted(glob.glob(str(B/"data/*.json")))}
html='''<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>每日热点库</title><style>
body{font-family:-apple-system,"PingFang SC",sans-serif;margin:0;background:#f5f7fa;color:#222}
header{background:#2E6DB4;color:#fff;padding:20px 24px}h1{margin:0;font-size:22px}header p{margin:6px 0 0;opacity:.85;font-size:13px}
.bar{display:flex;flex-wrap:wrap;gap:8px;padding:14px 24px;background:#fff;border-bottom:1px solid #e3e8ef;align-items:center}
select,input{padding:6px 10px;border:1px solid #cfd7e3;border-radius:6px;font-size:14px}
.chip{padding:4px 12px;border-radius:14px;background:#eaf0f8;cursor:pointer;font-size:13px}.chip.on{background:#2E6DB4;color:#fff}
main{max-width:980px;margin:0 auto;padding:16px 24px}
.card{background:#fff;border-radius:8px;padding:12px 16px;margin-bottom:10px;display:flex;gap:14px;box-shadow:0 1px 2px #0001}
.no{font-size:20px;font-weight:700;color:#2E6DB4;min-width:34px}.t a{color:#222;text-decoration:none;font-weight:600}.t a:hover{color:#2E6DB4}
.m{font-size:12px;color:#6b7686;margin-top:4px}.s{font-size:13px;color:#444;margin-top:4px}
.tag{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;margin-right:6px;background:#eaf0f8;color:#2E6DB4}
.高{background:#dff5e3;color:#1b7a36}.中{background:#fff3d6;color:#9a6a00}.低{background:#eee;color:#666}
footer{text-align:center;color:#8a94a3;font-size:12px;padding:20px}</style></head><body>
<header><h1>每日热点库</h1><p>每天自动抓取 10 个来源并整理 50 条热点。“前贴适配度”为分析判断,不是投放数据。</p></header>
<div class="bar"><select id="d"></select><input id="q" placeholder="搜索标题"><span id="cats"></span></div>
<main id="list"></main><footer>数据来源:新浪、凤凰、搜狐、网易、腾讯新闻、TMZ、The Daily Beast、Drudge Report、Bored Panda、今日热榜</footer>
<script>const D=__DATA__;let cat="全部";const $=i=>document.getElementById(i);
const ds=Object.keys(D).sort().reverse();$("d").innerHTML=ds.map(x=>`<option>${x}</option>`).join("");
function esc(s){return s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]))}
function draw(){const it=D[$("d").value],q=$("q").value.trim();
const cs=["全部",...new Set(it.map(x=>x.category))];
$("cats").innerHTML=cs.map(c=>`<span class="chip ${c==cat?"on":""}" onclick="cat='${c}';draw()">${c}</span>`).join(" ");
$("list").innerHTML=it.filter(x=>(cat=="全部"||x.category==cat)&&(!q||x.title.includes(q)||x.summary.includes(q))).map(x=>
`<div class="card"><div class="no">${x.rank}</div><div><div class="t"><a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)}</a></div>
<div class="s">${esc(x.summary)}</div><div class="m"><span class="tag">${esc(x.category)}</span><span class="tag ${x.teaser_fit}">前贴适配度:${x.teaser_fit}</span>来源:${esc(x.source)}</div></div></div>`).join("")}
$("d").onchange=()=>{cat="全部";draw()};$("q").oninput=draw;draw();</script></body></html>'''
(B/"index.html").write_text(html.replace("__DATA__",json.dumps(days,ensure_ascii=False)),encoding="utf8")
print("ok",list(days))
