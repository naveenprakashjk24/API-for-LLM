from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_CREDITS = {os.getenv('API_KEY'): 10}

app = FastAPI()

def verify_api_key(x_api_key:str = Header(None)):
    credit = API_KEY_CREDITS.get(x_api_key, 0)
    if credit<=0:
        raise HTTPException(status_code=401, detail='Invalid API Key, or No credits')

    return x_api_key


@app.post('/generate')
def generate_text(prompt:str, x_api_key: str= Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content":prompt}])
    return {"response": response['message']['content']}
