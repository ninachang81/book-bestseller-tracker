import os
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


def read_rankings_by_date(date_text):
    filename = f"data/rankings_{date_text}.csv"

    if not os.path.exists(filename):
        return []

    rankings = []

    with open(filename, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rankings.append(row)

    return rankings


def find_rank(book, source, rankings):
    title = book["title"]
    keywords = book.get("keywords", "")

    for item in rankings:
        if item["source"] != source:
            continue

        ranking_title = item["title"]

        if title in ranking_title or ranking_title in title:
            return f"第 {item['rank']} 名"

        for keyword in keywords.split(";"):
            keyword = keyword.strip()

            if keyword and keyword in ranking_title:
                return f"第 {item['rank']} 名"

    return "未入榜"


def find_rank_number(book, source, rankings):
    result = find_rank(book, source, rankings)

    if result == "未入榜":
        return None

    return int(result.replace("第", "").replace("名", "").strip())


def rank_change_text(today_rank, previous_rank):
    if today_rank is None and previous_rank is None:
        return "無變化"

    if today_rank is None:
        return "今日未入榜"

    if previous_rank is None:
        return "新進榜"

    diff = previous_rank - today_rank

    if diff > 0:
        return f"↑ 上升 {diff} 名"

    if diff < 0:
        return f"↓ 下降 {abs(diff)} 名"

    return "無變化"


def get_previous_rankings(today):
    if not os.path.exists("data"):
        return [], "無"

    previous_files = sorted([
        filename
        for filename in os.listdir("data")
        if filename.startswith("rankings_")
        and filename.endswith(".csv")
        and today not in filename
    ])

    if not previous_files:
        return [], "無"

    previous_file = previous_files[-1]
    previous_date = previous_file.replace("rankings_", "").replace(".csv", "")

    return read_rankings_by_date(previous_date), previous_date


def get_highlights(books, rankings, previous_rankings):
    highlights = []

    for book in books:
        for source in ["博客來", "誠品"]:
            today_rank = find_rank_number(book, source, rankings)
            previous_rank = find_rank_number(book, source, previous_rankings)
            change = rank_change_text(today_rank, previous_rank)

            if change == "新進榜":
                highlights.append(f"🆕 {book['title']}（{source}）新進榜")

            elif change.startswith("↑"):
                highlights.append(f"📈 {book['title']}（{source}）{change}")

            elif change.startswith("↓"):
                highlights.append(f"📉 {book['title']}（{source}）{change}")

    return highlights


def add_top_list(lines, rankings, source, limit=20):
    lines.append(f"# {source} Top {limit}")
    lines.append("")

    items = [
        item
        for item in rankings
        if item["source"] == source and item["rank"].isdigit()
    ]

    items = sorted(items, key=lambda x: int(x["rank"]))

    for item in items[:limit]:
        lines.append(f"{item['rank']}. {item['title']}")

    lines.append("")


books = read_tracked_books()
rankings = read_rankings()

today = datetime.now().strftime("%Y-%m-%d")
previous_rankings, previous_date = get_previous_rankings(today)

print("比較基準：", previous_date)

lines = []
lines.append(f"# 今日書籍追蹤報告 ({today})")
lines.append("")

highlights = get_highlights(books, rankings, previous_rankings)

lines.append("## 今日重點")
lines.append("")

lines.append(f"📚 今日追蹤：{len(books)} 本")
lines.append("")

if highlights:

    lines.append("### 排名異動")

    for item in highlights:
        lines.append(f"- {item}")

else:

    lines.append("今天沒有排名變化 🎉")

lines.append("")



for book in books:
    lines.append(f"## {book['title']}")

    for source in ["博客來", "誠品"]:
        today_text = find_rank(book, source, rankings)

        today_number = find_rank_number(book, source, rankings)
        previous_number = find_rank_number(book, source, previous_rankings)

        change = rank_change_text(today_number, previous_number)

        lines.append(f"- {source}：{today_text}（{change}）")

    lines.append("")

add_top_list(lines, rankings, "博客來", 20)
add_top_list(lines, rankings, "誠品", 20)

report = "\n".join(lines)

with open("report.md", "w", encoding="utf-8-sig") as f:
    f.write(report)

os.makedirs("reports", exist_ok=True)

report_filename = f"reports/{today}.md"

with open(report_filename, "w", encoding="utf-8-sig") as f:
    f.write(report)

print("report.md 已產生")
print(f"{report_filename} 已產生")