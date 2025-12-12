# fetch_news.py
import os
import uuid
import requests
import json
from datetime import datetime, timezone
from config.settings import BASE_URL, NEWS_API_KEY, DEFAULT_QUERY, MAX_PAGES, PAGE_SIZE, QUEUE_DIR, LOG_DIR
from utils.logger import get_logger
from utils.image_handler import handle_article_image

logger = get_logger("fetch_news")


def ensure_directories():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


def fetch_articles(query=DEFAULT_QUERY):
    all_articles = []
    for page in range(1, MAX_PAGES + 1):
        params = {
            "q": query,
            "pageSize": PAGE_SIZE,
            "page": page,
            "apiKey": NEWS_API_KEY
        }
        try:
            response = requests.get(BASE_URL, params=params)
            logger.info(f"Fetching page {page} -> {response.status_code} -> {response.url}")
            response.raise_for_status()
            data = response.json()
            if "articles" in data:
                all_articles.extend(data["articles"])
                logger.info(f"Page {page}: Retrieved {len(data['articles'])} articles.")
            else:
                logger.warning(f"Page {page}: No 'articles' key in response.")
        except Exception as e:
            logger.error(f"Error fetching page {page}: {e}")
    return all_articles


def save_article(article):
    article_id = str(uuid.uuid4())
    article["fetched_at"] = datetime.now(timezone.utc).isoformat()

    folder_path = os.path.join(QUEUE_DIR, article_id)
    os.makedirs(folder_path, exist_ok=True)

    image_path = handle_article_image(article.get("urlToImage"), folder_path, article_id)
    article["article_image_original"] = image_path.replace("\\", "/")

    json_path = os.path.join(folder_path, f"{article_id}.json")
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved article to {json_path}")
    except Exception as e:
        logger.error(f"Error saving article {article_id}: {e}")


def main():
    ensure_directories()
    logger.info(f"Starting fetch for query: '{DEFAULT_QUERY}'")
    articles = fetch_articles()
    logger.info(f"Total fetched: {len(articles)}")
    for idx, article in enumerate(articles):
        if article.get("title") and article.get("url"):
            save_article(article)
        else:
            logger.warning(f"Article at index {idx} missing title or url. Skipping.")


if __name__ == "__main__":
    main()