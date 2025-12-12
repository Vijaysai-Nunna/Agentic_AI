from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F
 
 
# define model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
 
#   reed articel from txt
with open("articles.txt","r",encoding="utf-8") as f:
    article = f.read().strip()
 
 
# Get Possible Candidates
headlines = [
    "US and India remove tariffs to boost trade ties",
   "India launches lunar probe to explore moon's south pole",
    "Tariff rollback improves US-India manufacturing access",
    "Stock markets dip amid inflation concerns in Asia",
    "Improved trade relations could strengthen US-India alliance",
    "India bans certain Chinese tech products from ports"
]
 
 
 
def get_mean_embeddings(input_text):
   
    model_input = tokenizer(input_text,return_tensors = "pt")
 
    with torch.no_grad():
        model_output = model(**model_input)
        mean_embeddings = model_output.last_hidden_state.mean(dim=1)
    return mean_embeddings
 
article_embeddings = get_mean_embeddings(article)  # saves to vector
 
results =[]  # empty list for saving similar top 4 headlines
for headline in headlines:
    headline_embeddings = get_mean_embeddings(headline)
    score = F.cosine_similarity(article_embeddings,headline_embeddings).item()
    results.append((headline,score))
 
# sorting results.
results.sort(key=lambda x:x[1],reverse=True)
# Print the results
print (f"\nFile content: {article} \n")

print ("Top 4 Similar headlines are: \n")

 
for i in range(4):
    headline,score = results[i]
 
    print  (f"{i + 1} - {headline} - Score {score:.4f}")
 
 
print("All headlines as per score : ")
 
for headline, score in results:
    print (f"{score:.4f} -> {headline}")
 
 