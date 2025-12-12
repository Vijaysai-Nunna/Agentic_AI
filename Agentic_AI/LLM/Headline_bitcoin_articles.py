import requests
import logging
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model
import json, os

file_path = "headline_articles.json"
NEWS_API_URL = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey=c817dfe2893147c1ae5d0dae5e5458da"
API_KEY = "c817dfe2893147c1ae5d0dae5e5458da"
QUERY = "bitcoin"
ARTICLE_COUNT = 5
HEADLINE_COUNT = 5


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load models and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

def mean_embedding(input_text):
    tokens = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = emb_model(**tokens)
    logging.info("Generated mean_embedding")
    return embeddings.last_hidden_state.mean(dim=1)

def fetch_news_articles(api_key, query, count) -> list[dict]:
    logging.info("Fetching news articles...")
    response = requests.get("https://newsapi.org/v2/everything", params={
        "q": query,
        "apiKey": api_key,
        "pageSize": count
    })
    response.raise_for_status()
    articles = response.json().get("articles", [])
    logging.info(f"Fetched {len(articles)} articles")
    return articles

def generate_headlines(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt",truncation=True).input_ids
    outputs = gen_model.generate(
        input_ids,
        num_return_sequences=5,
        do_sample=True,
        max_new_tokens=50,
        temperature=0.8,
        top_k=50,
        top_p=0.95
    )
    logging.info("Returning generated headlines")
    return [tokenizer.decode(output, skip_special_tokens=True).replace(prompt, "").strip() for output in outputs]

def process_news_articles(news_articles):
    processed_articles = []

    for idx, article in enumerate(news_articles):
        content = article.get("content") or ""
        title = article.get("title") or ""
        description = article.get("description") or ""

        news_text = f"{title}. {description}. {content}".strip()

        if not news_text:
            continue

        prompt = f"Generate a headline for this news:\n{news_text}\nHeadline:"
        headline_candidates = generate_headlines(prompt)
        news_text_embedding = mean_embedding(prompt)

        results = []
        for headline in headline_candidates:
            headline_embedding = mean_embedding(headline)
            score = F.cosine_similarity(headline_embedding, news_text_embedding).item()
            results.append({"headline": headline, "score": round(score, 4)})


        # results.sort(key=lambda x: x["score"], reverse=True)

    
        # top_headline = results
        # logging.info(f"Appended headlines for the article")
        # processed_articles.append(top_headline)

    
        
        # # Print each article and its top headlines
        # for key, value in top_headline.items():
        #     print(f"{key}: {value}")
        # print("###############################################")
        # print("###############################################")

        results.sort(key=lambda x: x["score"], reverse=True)
        top_headlines = results[:3]
        article["top_headlines"] = top_headlines

        logging.info(f"Appended top {len(top_headlines)} headlines for Article #{idx}")

        print(f"\n# Article #{idx}")
        print(f"\n*News Article:*\n{news_text}\n")
        for i, h in enumerate(top_headlines, 1):
            print(f"{i}. {h['headline']} (Score: {h['score']:.4f})")
        print("###############################################")
        print("###############################################")

        processed_articles.append(article)

    return {
        "status": "ok",
        "totalResults": len(processed_articles),
        "articles": processed_articles
    }

def save_to_json(data, filename="headline_articles.json"):
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info(f"Saved output to {filename}")

def ensure_json_file_exists(filename="headline_articles.json"):
    if not os.path.exists(filename):
        logging.warning(f"{filename} not found. Creating an empty file.")
        empty_structure = {"status": "ok", "totalResults": 0, "articles": []}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(empty_structure, f, indent=2, ensure_ascii=False)
        logging.info(f"Created empty JSON file: {filename}")

if __name__ == "__main__":
    try:
        ensure_json_file_exists(file_path)
        articles = fetch_news_articles(API_KEY, QUERY, ARTICLE_COUNT)
        data = process_news_articles(articles)
        # save_to_json(data)
    except Exception as e:
        logging.error(str(e))
