from playwright.sync_api import sync_playwright
import csv
import re

SITES = [
    ("誠品", "https://www.eslite.com/best-sellers/online"),
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

all_results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for source, url in SITES:
        print(f"正在抓取：{source}")
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(8000)

        text = page.locator("body").inner_text()

        with open(f"{source}_page.txt", "w", encoding="utf-8-sig") as f:
            f.write(text)

        parsed = parse_books_top(text, source)
        print(f"{source} 抓到 {len(parsed)} 筆")

        all_results.extend(parsed)

    browser.close()

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