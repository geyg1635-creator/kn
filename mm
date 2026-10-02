import json
import urllib.request
import re
from datetime import datetime

# 公开财经新闻源（聚合接口）
SOURCES = [
    {
        "name": "财联社",
        "url": "https://api.vvhan.com/api/hotlist/caijing",
    },
    {
        "name": "华尔街见闻",
        "url": "https://api.vvhan.com/api/hotlist/36kr",
    },
]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"抓取失败: {url} -> {e}")
        return None

def main():
    news_list = []
    for src in SOURCES:
        data = fetch(src["url"])
        if not data:
            continue
        items = data.get("data", [])
        if isinstance(items, dict):
            items = items.get("list", [])
        for item in items[:8]:
            title = item.get("title") or item.get("name") or ""
            url = item.get("url") or item.get("link") or ""
            if title:
                news_list.append({
                    "title": re.sub(r"<[^>]+>", "", title).strip(),
                    "url": url,
                    "source": src["name"],
                })

    # 去重
    seen = set()
    unique = []
    for n in news_list:
        if n["title"] not in seen:
            seen.add(n["title"])
            unique.append(n)

    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "news": unique[:12],
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已抓取 {len(unique)} 条新闻")

if __name__ == "__main__":
    main()
