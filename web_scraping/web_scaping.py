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
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_page_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"Ошибка при запросе страницы: {error}")
        return None


def parse_articles(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        return soup.find_all("article")
    except Exception as error:
        print(f"Ошибка при разборе HTML: {error}")
        return []


def extract_article_data(article):
    title_tag = (
        article.select_one("h2 a")
        or article.select_one("a.tm-title__link")
        or article.select_one("a[data-test-id='article-snippet-title-link']")
    )

    time_tag = article.find("time")

    if not title_tag or not time_tag:
        return None

    title = title_tag.get_text(strip=True)
    if not title:
        return None

    href = title_tag.get("href")
    if not href:
        return None

    link = urljoin(URL, href)

    date_text = (
        time_tag.get("title")
        or time_tag.get("datetime")
        or time_tag.get_text(strip=True)
    )

    preview_text = article.get_text(" ", strip=True)
    if not preview_text:
        preview_text = ""

    return {
        "title": title,
        "date": date_text,
        "link": link,
        "preview": preview_text.lower(),
    }


def contains_keywords(text, keywords):
    text = text.lower()
    return any(keyword.lower() in text for keyword in keywords)


def main():
    html = get_page_html(URL)
    if not html:
        return

    articles = parse_articles(html)
    if not articles:
        print("Статьи не найдены.")
        return

    for article in articles:
        article_data = extract_article_data(article)
        if not article_data:
            continue

        if contains_keywords(article_data["preview"], KEYWORDS):
            print(f"{article_data['date']} – {article_data['title']} – {article_data['link']}")


if __name__ == "__main__":
    main()
