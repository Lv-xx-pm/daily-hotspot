#!/usr/bin/env python3
"""抓取红果短剧官网(hongguoduanju.com)公开榜单,存到 raw/hongguo-日期.json。
只抓公开的榜单文字信息:排名、剧名、热度、评分、题材标签、剧情简介、官网链接。不抓视频。
剧情简介只存在本地 raw/ 里供分析,不发布到公开网页(raw/ 已被 .gitignore 排除)。"""
import json, re, datetime, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).parent
SITE = "https://www.hongguoduanju.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
RANKS = [("真人剧", "/rank/hot-real-drama"), ("AI剧", "/rank/hot-ai-drama"),
         ("漫剧", "/rank/hot-comic-drama"), ("全部", "/rank/hot-drama")]


def get(path):
    req = urllib.request.Request(SITE + path, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9"})
    return urllib.request.urlopen(req, timeout=25).read().decode("utf8", "ignore")


def parse(html):
    soup = BeautifulSoup(html, "lxml")
    out, seen = [], set()
    for a in soup.select('a[href*="detail?series_id"]'):
        title = a.get_text(strip=True)
        sid = re.search(r"series_id=(\d+)", a["href"]).group(1)
        if not title or title.isdigit() or sid in seen:
            continue
        card = a
        for _ in range(4):
            card = card.parent
        parts = card.get_text("|", strip=True).split("|")
        heat = next((p for p in parts if p.endswith("热度")), "")
        score = next((p for p in parts if re.fullmatch(r"[\d.]+分", p)), "")
        tagline = next((p for p in parts if " · " in p), "")
        genre = tagline.split(" · ")[0] if tagline else ""
        synopsis = max(parts, key=len) if parts else ""
        if len(synopsis) < 30:
            synopsis = ""
        seen.add(sid)
        out.append({"rank": len(out) + 1, "title": title, "heat": heat, "score": score,
                    "genre": genre, "synopsis": synopsis, "url": f"{SITE}/detail?series_id={sid}"})
    return out


def main():
    day = datetime.date.today().isoformat()
    data, log = {"date": day, "lists": []}, []
    for name, path in RANKS:
        try:
            items = parse(get(path))
            data["lists"].append({"name": name, "items": items})
            log.append(f"{name}榜: {len(items)} 部")
        except Exception as e:
            log.append(f"{name}榜: 失败 {e}")
    (BASE / "raw").mkdir(exist_ok=True)
    (BASE / "raw" / f"hongguo-{day}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
