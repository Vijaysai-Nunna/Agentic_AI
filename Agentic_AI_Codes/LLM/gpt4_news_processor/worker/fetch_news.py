# fetch_news : Get the news and save news article
import os
import requests
import json
import uuid
from config.settings import BASE_URL, NEWS_API_KEY, DEFAULT_QUERY,MAX_PAGES, PAGE_SIZE, QUEUE_DIR, LOG_DIR
from utils.logger import get_logger
from datetime import datetime, timezone

logger = get_logger('fetch_news')

def fetch_articles(query):
    all_articles = []
    for page in range(1, MAX_PAGES +1):
        params = {
            "q" : query,
            "page_size" : PAGE_SIZE,
            "page": page, 
            "apiKey" : NEWS_API_KEY
        }
        response = requests.get(BASE_URL, params= params)
        logger.info (f"Fetching the Page {page} -> {response.status_code} -> {response.url} ")
        response.raise_for_status()
        data = response.json()
        if "articles" in data:
            all_articles.extend(data["articles"])
            logger.info (f"Page {page} : Retrived {len(data["articles"])} articles.")
        else:
            logger.info (f"Page {page} : Dose not have articles ")
    return all_articles


def save_article (article,article_number):
    article_id = str (uuid.uuid4())
    article["fetched_at"] = datetime.now(timezone.utc).isoformat()
    file_name = f"article_{article_number}.json"
    file_path = os.path.join(QUEUE_DIR, f"{article_id}.json")
    with open (file_path, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=2)
        logger.info (f"Saved article to {file_path}")
    return True

def main():
    logger.info ("Starting fetch for api....")
    # Fetch Articles
    articles = fetch_articles(query = DEFAULT_QUERY)
    logger.info (f"Total Fetched Articles are {len(articles)}")

    # Save Articles in Folder

    for idx, article in enumerate (articles, start=1):
        if article.get("title") and article.get("url"):
            save_article(article,idx)



if __name__ == "__main__":
    main()