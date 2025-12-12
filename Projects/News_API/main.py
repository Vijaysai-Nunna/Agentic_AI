from app.Data.User_data import save_to_json
from app.Service.news_service import (
    mean_embedding,
    fetch_news_articles,
    generate_headlines,
    process_news_articles
)


file_path = "app\\Data\\llm_headline_articles.json"


NEWS_API_URL = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey=c817dfe2893147c1ae5d0dae5e5458da"
API_KEY = "c817dfe2893147c1ae5d0dae5e5458da"
QUERY = "bitcoin"
ARTICLE_COUNT = 5
HEADLINE_COUNT = 5




def main():
    articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
    processed_data=process_news_articles(articles)
    save_to_json(processed_data,file_path)


if __name__ == "__main__":
    main()
