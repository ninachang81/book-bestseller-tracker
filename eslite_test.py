import requests

url = "https://www.eslite.com/best-sellers/online"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

with open("eslite.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("已儲存 eslite.html")