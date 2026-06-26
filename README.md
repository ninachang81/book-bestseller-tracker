# 📚 Book Bestseller Tracker

每天自動追蹤博客來與誠品排行榜，並比較指定書籍的排名變化。

---

# 功能

- ✅ 自動抓取博客來排行榜
- ✅ 自動抓取誠品排行榜
- ✅ 自訂追蹤書籍
- ✅ 判斷是否入榜
- ✅ 顯示排名
- ✅ 排名升降追蹤
- ✅ 每日產生 Markdown 報告
- ✅ GitHub Actions 自動更新

---

# 專案架構

```
book-bestseller-tracker
│
├── tracked_books.csv        # 追蹤書單
├── rankings.csv             # 最新排行榜
├── data/                    # 每日排行榜歷史
├── reports/                 # 每日報告
│
├── fetch_rankings.py        # 抓排行榜
├── main.py                  # 產生報告
├── requirements.txt
└── README.md
```

---

# 執行方式

## 安裝

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 更新排行榜

```bash
python fetch_rankings.py
```

---

## 產生報告

```bash
python main.py
```

---

# 報告範例

```
# 今日書籍追蹤報告

## 今日重點

📚 今日追蹤：3 本

今天沒有排名變化 🎉

## Rewire

博客來：第13名（無變化）
誠品：第7名（無變化）
```

---

# 使用技術

- Python
- Playwright
- CSV
- GitHub Actions
- Markdown

---

# Roadmap

- [x] 博客來排行榜
- [x] 誠品排行榜
- [x] 排名升降追蹤
- [x] GitHub Actions
- [x] 每日 Markdown 報告
- [ ] Email 通知
- [ ] GitHub Pages
- [ ] 排名歷史圖表
- [ ] LINE Notify

---

# License

MIT