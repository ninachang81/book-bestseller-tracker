import csv
from datetime import datetime

def read_tracked_books():
    books = []
    with open("tracked_books.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["enabled"].strip().upper() == "TRUE":
                books.append(row)
    return books

def read_rankings():
    rankings = []
    with open("rankings.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rankings.append(row)
    return rankings

def find_rank(book, source, rankings):
    title = book["title"].strip()
    keywords = book.get("keywords", "").strip()

    for item in rankings:
        if item["source"] != source:
            continue

        ranking_title = item["title"]

        if title and (title in ranking_title or ranking_title in title):
            return f"第 {item['rank']} 名"

        for keyword in keywords.split(";"):
            keyword = keyword.strip()
            if keyword and keyword in ranking_title:
                return f"第 {item['rank']} 名"

    return "未入榜"

def add_top_list(lines, rankings, source, limit=20):
    lines.append(f"# {source} Top {limit}")
    lines.append("")

    items = [
        item for item in rankings
        if item["source"] == source and item["rank"].isdigit()
    ]

    items = sorted(items, key=lambda x: int(x["rank"]))

    for item in items[:limit]:
        lines.append(f"{item['rank']}. {item['title']}")

    lines.append("")

books = read_tracked_books()
rankings = read_rankings()

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append(f"# 今日書籍追蹤報告 ({today})")
lines.append("")

for book in books:
    lines.append(f"## {book['title']}")
    lines.append(f"- 博客來：{find_rank(book, '博客來', rankings)}")
    lines.append(f"- 誠品：{find_rank(book, '誠品', rankings)}")
    lines.append("")

add_top_list(lines, rankings, "博客來", 20)
add_top_list(lines, rankings, "誠品", 20)

import os

os.makedirs("reports", exist_ok=True)

report_filename = f"reports/{today}.md"

with open(report_filename, "w", encoding="utf-8-sig") as f:
    f.write("\n".join(lines))

print(f"{report_filename} 已產生")