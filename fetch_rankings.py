from playwright.sync_api import sync_playwright
import csv
import re

SITES = [
    ("誠品", "https://www.eslite.com/category/1/3"),
    ("博客來", "https://www.books.com.tw/web/sys_saletopb/books/"),
]

def parse_books_top(text, source):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    results = []

    for i in range(len(lines) - 2):
        if lines[i] == "TOP" and lines[i + 1].isdigit():
            rank = lines[i + 1]
            title = lines[i + 2]

            if title.startswith("作者："):
                continue
            if title.startswith("優惠價"):
                continue
            if title in ["收藏", "加入購物車"]:
                continue

            results.append({
                "source": source,
                "rank": rank,
                "title": title
            })

    return results


def parse_eslite(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    results = []

    for i in range(len(lines) - 1):

        if lines[i].isdigit():

            rank = int(lines[i])

            if 1 <= rank <= 50:

                title = lines[i + 1]

                if (
                    len(title) > 5
                    and not title.isdigit()
                    and "排行榜" not in title
                    and "榜" not in title
                ):

                    results.append({
                        "source": "誠品",
                        "rank": rank,
                        "title": title
                    })

    return results


all_results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36"
)

    for source, url in SITES:
        print(f"正在抓取：{source}")
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)

        text = page.locator("body").inner_text()

        with open(f"{source}_page.txt", "w", encoding="utf-8-sig") as f:
            f.write(text)

        if source == "誠品":
           parsed = parse_eslite(text)
        else:
           parsed = parse_books_top(text, source)
        print(f"{source} 抓到 {len(parsed)} 筆")

        if len(parsed) == 0 and source == "博客來":
           print("博客來本次抓取失敗，略過更新博客來資料")
        else:
            all_results.extend(parsed)

    browser.close()

    def read_existing_rankings():
        existing = []

        try:
           with open("rankings.csv", encoding="utf-8-sig") as f:
               reader = csv.DictReader(f)
           
               for row in reader:
                   existing.append(row)
        except FileNotFoundError:
            pass

        return existing


existing_rankings = read_existing_rankings()

sources_updated = set(item["source"] for item in all_results)

for item in existing_rankings:
    if item["source"] not in sources_updated:
        all_results.append(item)

from datetime import datetime
import os

today = datetime.now().strftime("%Y-%m-%d")

os.makedirs("data", exist_ok=True)

# 最新版
with open("rankings.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["source", "rank", "title"])
    writer.writeheader()
    writer.writerows(all_results)

# 歷史備份
history_file = f"data/rankings_{today}.csv"

with open(history_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["source", "rank", "title"])
    writer.writeheader()
    writer.writerows(all_results)

print("rankings.csv 已更新")
print(f"{history_file} 已備份")

