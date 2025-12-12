from app.Utils.logger import get_logger
from app.Utils.decorators import handle_exceptions
import requests
import logging
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model
import json,os


logging = get_logger(__name__)



NEWS_API_URL = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey=c817dfe2893147c1ae5d0dae5e5458da"
API_KEY = "c817dfe2893147c1ae5d0dae5e5458da"
QUERY = "bitcoin"
ARTICLE_COUNT = 5
HEADLINE_COUNT = 5




# Load models and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id


@handle_exceptions
def mean_embedding(input_text):

   input_text_tokens = tokenizer(input_text, return_tensors="pt")
   if not input_text_tokens or len(input_text_tokens.get('input_ids', [])) == 0:
        raise ValueError("Input tokens are empty!")
   with torch.no_grad():
        embeddings = emb_model(**input_text_tokens)
        logging.info(f"Gnerated mean_embeddings")
   return embeddings.last_hidden_state.mean(dim=1)


@handle_exceptions
def fetch_news_articles(api_key:str, count:int) -> list[dict]:
    logging.info("Fetching news articles...")
    response = requests.get("https://newsapi.org/v2/everything", params={
        "q": QUERY,
        "apiKey": api_key,
        "pageSize": count
    })
    response.raise_for_status()
    articles = response.json().get("articles", [])
    logging.info(f"Fetched {len(articles)} articles")
    return articles


@handle_exceptions
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


@handle_exceptions
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


        results.sort(key=lambda x: x["score"], reverse=True)

    
        article["top_headline"] = results[:3]
        logging.info(f"Appended headlines for the article")
        

    
        
        # Print each article and its top headlines
        print(f"\n# Article #{idx+1}")
        print(f"\n*News Article:*\n{news_text}\n")
        for key, value in article.items():
            print(f"{key}: {value}")
        print("###############################################")
        print("###############################################")
        processed_articles.append(article)

        #results.sort(key=lambda x: x["score"], reverse=True)
        # top_headlines = results[:3]
        # article["top_headlines"] = top_headlines

        # logging.info(f"Appended top {len(top_headlines)} headlines for Article #{idx}")

        # print(f"\n# Article #{idx}")
        # print(f"\n*News Article:*\n{news_text}\n")
        # for i, h in enumerate(top_headlines, 1):
        #     print(f"{i}. {h['headline']} (Score: {h['score']:.4f})")
        # print("###############################################")
        # print("###############################################")

        # processed_articles.append(article)

    return {
        "status": "ok",
        "totalResults": len(processed_articles),
        "articles": processed_articles
    }
