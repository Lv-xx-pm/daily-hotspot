#!/usr/bin/env python3
"""每天抓取10个来源的头条,存到 raw/日期.json(不调用AI,纯程序)。"""
import json, sys, re, datetime, urllib.request, urllib.parse
from bs4 import BeautifulSoup
from pathlib import Path
BASE = Path(__file__).parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
SITES = [("新浪网","https://www.sina.com.cn","国内"),("凤凰网","https://www.ifeng.com","国内"),
 ("搜狐网","https://www.sohu.com","国内"),("网易新闻","https://www.163.com","国内"),
 ("腾讯新闻","https://news.qq.com","国内"),("TMZ","https://www.tmz.com","海外"),
 ("The Daily Beast","https://www.thedailybeast.com","海外"),("Drudge Report","https://www.drudgereport.com","海外"),
 ("Bored Panda","https://www.boredpanda.com","海外")]
TOPHUB = ["微博","知乎","微信","百度","抖音","快手","哔哩哔哩","百度贴吧","腾讯新闻","豆瓣电影","百度视频","实时榜中榜"]
def get(u):
    r = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
    return urllib.request.urlopen(r, timeout=25).read()
def generic(name, url, region):
    s = BeautifulSoup(get(url), "lxml"); seen=set(); out=[]
    minlen = 8 if region=="国内" else 20
    for a in s.find_all("a", href=True):
        t = re.sub(r"\s+"," ",a.get_text(" ",strip=True))
        h = urllib.parse.urljoin(url, a["href"])
        if len(t)<minlen or len(t)>90 or t in seen or not h.startswith("http"): continue
        if re.search(r"登录|注册|下载|关于|联系|隐私|版权|广告|订阅|Subscribe|Privacy|Terms|Cookie",t): continue
        seen.add(t); out.append({"title":t,"url":h})
    return out[:50]
def tophub():
    s = BeautifulSoup(get("https://tophub.today/"), "lxml"); res={}
    for c in s.select(".cc-cd"):
        lb = c.select_one(".cc-cd-lb"); n = lb.get_text(strip=True) if lb else ""
        if n not in TOPHUB or n in res: continue
        items=[]
        for a in c.select(".cc-cd-cb-l a")[:30]:
            t = re.sub(r"^\d+\s*","",a.get_text(" ",strip=True))
            items.append({"title":t,"url":a.get("href","")})
        res[n]=items
    return res
def main():
    day = datetime.date.today().isoformat(); data={"date":day,"sources":[]}; log=[]
    for n,u,r in SITES:
        try: items=generic(n,u,r); data["sources"].append({"name":n,"region":r,"items":items}); log.append(f"{n}: {len(items)}")
        except Exception as e: log.append(f"{n}: 失败 {e}")
    try:
        for n,items in tophub().items():
            data["sources"].append({"name":"今日热榜·"+n,"region":"榜单","items":items}); log.append(f"今日热榜·{n}: {len(items)}")
    except Exception as e: log.append(f"今日热榜: 失败 {e}")
    (BASE/"raw"/f"{day}.json").write_text(json.dumps(data,ensure_ascii=False,indent=1),encoding="utf8")
    print("\n".join(log))
main()
