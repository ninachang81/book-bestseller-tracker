import requests

url = "https://www.books.com.tw/web/sys_saletopb/books/"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.books.com.tw/"
}

response = requests.get(url, headers=headers, timeout=30)

print("狀態碼:", response.status_code)
print()
print("前500個字:")
print(response.text[:500])