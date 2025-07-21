from fastapi import FastAPI
from pydantic import BaseModel
from url_reputation import check_url_reputation
from html import escape
from intent_classifier import classify_intent
import re
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

class Message(BaseModel):
    text: str

def ask_duckduckgo(query):
    # Basic DuckDuckGo Instant Answer API call
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "skip_disambig": 1,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        # Prefer AbstractText, else Answer, else fallback message
        answer = data.get("AbstractText") or data.get("Answer") or "Sorry, I couldn't find an answer."
        return answer
    except Exception as e:
        logging.error(f"DuckDuckGo API error: {e}")
        return "Sorry, I'm having trouble finding an answer right now."

@app.post("/chat")
async def chat(message: Message):
    original_text = escape(message.text.strip())
    logging.info(f"Original message: {original_text}")

    intent = classify_intent(original_text.lower())
    logging.info(f"Detected intent: {intent}")

    url_pattern = r"(https?://[^\s]+)"
    urls = re.findall(url_pattern, original_text.lower())

    if intent == "check_url" and urls:
        url = urls[0]
        result = check_url_reputation(url)
        logging.info(f"Checked URL: {url} | Result: {result}")
        response = f"VirusTotal results for {url}: {result}"
    else:
        response = ask_duckduckgo(original_text)

    logging.info(f"Final response: {response}")

    return {"response": response}
