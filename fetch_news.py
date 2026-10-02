import json
import urllib.request
import re
from datetime import datetime

SOURCES = [
    {"name": "澎湃财经", "url": "https://api.vvhan.com/api/hotlist/thepaper"},
    {"name": "百度财经", "url": "https://api.vvhan.com/api/hotlist/baidu"},
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

    seen = set()
    unique = []
    for n in news_list:
        if n["title"] not in seen:
            seen.add(n["title"])
            unique.append(n)

    news = unique[:12]
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")

    items_html = ""
    for item in news:
        link = f'<a href="{item["url"]}" target="_blank">🔗 原文</a>' if item["url"] else ""
        items_html += f'''
        <div class="news-item">
          <div class="title">{item["title"]}</div>
          <div class="meta">
            <span class="tag">{item["source"]}</span>
            {link}
          </div>
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日金融时政</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, "PingFang SC", "微软雅黑", Arial, sans-serif; background: #eef3fa; min-height: 100vh; padding: 12px; color: #333; font-size: 16px; }}
  .container {{ max-width: 640px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 16px rgba(26,58,107,0.1); padding: 18px 16px 24px; }}
  .header {{ text-align: center; margin-bottom: 16px; }}
  .header h1 {{ font-size: 22px; color: #1a3a6b; margin-bottom: 4px; }}
  .header .date {{ font-size: 13px; color: #888; }}
  .section-title {{ font-size: 15px; font-weight: bold; color: #1a3a6b; margin: 18px 0 10px 2px; padding-bottom: 6px; border-bottom: 2px solid #f0f4f8; }}
  .news-item {{ padding: 13px 12px; border-radius: 12px; border: 1.5px solid #eef2f7; background: #fafcff; margin-bottom: 8px; }}
  .news-item .title {{ font-size: 14px; font-weight: 600; color: #2c3e50; line-height: 1.5; margin-bottom: 6px; }}
  .news-item .meta {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .news-item .tag {{ font-size: 11px; color: #4a90d9; background: #e8f0fe; padding: 2px 8px; border-radius: 6px; }}
  .news-item a {{ font-size: 12px; color: #4a90d9; text-decoration: none; }}
  .footer {{ text-align: center; font-size: 12px; color: #aaa; margin-top: 20px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📰 每日金融时政</h1>
    <div class="date">更新于 {updated}</div>
  </div>
  <div class="section-title">🏦 今日财经要闻</div>
  {items_html}
  <div class="footer">每天早上 8:00 自动更新</div>
</div>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump({"date": datetime.now().strftime("%Y-%m-%d"), "updated": updated, "news": news}, f, ensure_ascii=False, indent=2)

    print(f"已更新 {len(news)} 条新闻")

if __name__ == "__main__":
    main()
