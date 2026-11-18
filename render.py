#!/usr/bin/env python3
"""把 data/*.json 渲染成一个独立网页 index.html(含历史日期切换、分类筛选、搜索)。"""
import json, glob
from pathlib import Path
B=Path(__file__).parent
days={Path(f).stem:json.load(open(f,encoding="utf8"))["items"] for f in sorted(glob.glob(str(B/"data/*.json")))}
html='''<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>每日热点库</title><style>
body{font-family:-apple-system,"PingFang SC",sans-serif;margin:0;background:#f2f5fa;color:#222}
header{background:#2E6DB4;color:#fff;padding:20px 24px}h1{margin:0;font-size:22px}header p{margin:6px 0 0;opacity:.85;font-size:13px}
.bar{display:flex;flex-wrap:wrap;gap:8px;padding:12px 24px;background:#fff;border-bottom:1px solid #e3e8ef;align-items:center;position:sticky;top:0;z-index:2}
select,input{padding:6px 10px;border:1px solid #cfd7e3;border-radius:6px;font-size:14px}
.chip{padding:4px 12px;border-radius:14px;background:#eaf0f8;cursor:pointer;font-size:13px;white-space:nowrap}.chip.on{background:#2E6DB4;color:#fff}
main{max-width:1240px;margin:0 auto;padding:18px 24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.card{background:#fff;border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:10px;box-shadow:0 1px 3px #0001;border-top:4px solid #2E6DB4}
.card.c中{border-top-color:#e0a21b}.card.c低{border-top-color:#b8c0cc}
.top{display:flex;justify-content:space-between;font-size:12px;color:#6b7686}
.hook{font-size:18px;line-height:1.5;font-weight:700;color:#1b2a41}
.ev{font-size:13px;color:#4a5565;line-height:1.6}
.tags{display:flex;flex-wrap:wrap;gap:6px}.tag{padding:1px 8px;border-radius:10px;font-size:12px;background:#eaf0f8;color:#2E6DB4}
.高{background:#dff5e3;color:#1b7a36}.中{background:#fff3d6;color:#9a6a00}.低{background:#eee;color:#666}.需虚构化{background:#fde8e8;color:#b42318}
.foot{margin-top:auto;font-size:12px;color:#8a94a3;display:flex;justify-content:space-between}.foot a{color:#2E6DB4;text-decoration:none}
footer{text-align:center;color:#8a94a3;font-size:12px;padding:20px}</style></head><body>
<header><h1>每日热点库</h1><p>每天自动整理 50 条热点素材卡。钩子与事件描述均不含真实人名、公司名和地名;“可改编性”是分析判断,不是投放数据。</p></header>
<div class="bar"><select id="d"></select><input id="q" placeholder="搜索"><span id="cats"></span></div>
<main id="list"></main><footer>数据来源:新浪、凤凰、搜狐、网易、腾讯新闻、TMZ、The Daily Beast、Drudge Report、Bored Panda、今日热榜</footer>
<script>const D=__DATA__;let cat="全部";const $=i=>document.getElementById(i);
const ds=Object.keys(D).sort().reverse();$("d").innerHTML=ds.map(x=>`<option>${x}</option>`).join("");
function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]))}
function draw(){const it=D[$("d").value],q=$("q").value.trim();
const cs=["全部",...new Set(it.map(x=>x.type))];
$("cats").innerHTML=cs.map(c=>`<span class="chip ${c==cat?"on":""}" onclick="cat='${c}';draw()">${c}</span>`).join(" ");
$("list").innerHTML=it.filter(x=>(cat=="全部"||x.type==cat)&&(!q||x.hook.includes(q)||x.event.includes(q))).map(x=>
`<div class="card c${x.adapt}"><div class="top"><span>#${x.rank}</span><span class="tag ${x.adapt}">可改编性:${x.adapt}</span></div>
<div class="hook">${esc(x.hook)}</div><div class="ev">${esc(x.event)}</div>
<div class="tags"><span class="tag">${esc(x.type)}</span><span class="tag">情绪:${esc(x.emotion)}</span><span class="tag">冲突:${esc(x.conflict)}</span>${x.compliance=="需虚构化"?'<span class="tag 需虚构化">需虚构化</span>':""}</div>
<div class="foot"><span>来源:${esc(x.source)}</span><a href="${esc(x.url)}" target="_blank" rel="noopener">查看原文</a></div></div>`).join("")}
$("d").onchange=()=>{cat="全部";draw()};$("q").oninput=draw;draw();</script></body></html>'''
(B/"index.html").write_text(html.replace("__DATA__",json.dumps(days,ensure_ascii=False)),encoding="utf8")
print("ok",list(days))
