from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from openai import OpenAI  
from app.utils.decorators import handle_exception
from app.utils.logger import get_logger
import os


logger = get_logger(__name__)

router = APIRouter()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))   # temporaily key is not avaible

class TextInput(BaseModel):
    text : str
    language : str = "te" # "te" is the ISO 639-1 code for Telugu

# original
@handle_exception
@router.post("/prompt_chain")
async def prompt_chain(input : TextInput):

    #step 1 : Summerize Role -> User Input
    logger.info(f"Summarized the Text : {input.text}")
    summary = client.chat.completions.create(
        model = "gpt-4",
        messages = [
            {"role":"system" ,"content" : "Summarize the following text."},
            {"role":"user","content":input.text}
        ],
        temperature =0.4
    ).choices[0].message.content.strip()

    #step 2 fixed the grammer in text
    
    improved_text = client.chat.completions.create(
        model = "gpt-4",
        messages = [
            {"role":"system" ,"content" : "Improve grammer and clarity of this text."},
            {"role":"user","content":input.text}
        ],
        temperature =0.3
    ).choices[0].message.content.strip()
    logger.info(f"Sentence corrected the Text : {improved_text}")

    # step 3 translate 
    
    translated_text = client.chat.completions.create(
        model = "gpt-4",
        messages = [
            {"role":"system" ,"content" : f"Translate the following text to {input.language}."},
            {"role":"user","content":improved_text}
        ],
        temperature =0.3
    ).choices[0].message.content.strip()


    return {
        "Summary" : summary,
        "Improved_text" : improved_text,
        "translated_text" : translated_text 
    }
    