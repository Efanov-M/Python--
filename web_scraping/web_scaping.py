import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

KEYWORDS = [
    "дизайн",
    "фото",
    "web",
    "python",
]

URL = "https://habr.com/ru/articles/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("article")

for article in articles:
    title_tag = (
        article.select_one("h2 a")
        or article.select_one("a.tm-title__link")
        or article.select_one("a[data-test-id='article-snippet-title-link']")
    )

    time_tag = article.find("time")

    if not title_tag or not time_tag:
        continue

    title = title_tag.get_text(strip=True)
    link = urljoin(URL, title_tag.get("href"))
    date_text = time_tag.get("title") or time_tag.get("datetime") or time_tag.get_text(strip=True)

    preview_text = article.get_text(" ", strip=True).lower()

    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        print(f"{date_text} – {title} – {link}")
