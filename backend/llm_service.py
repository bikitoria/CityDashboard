# Flask backend (llm_service.py)
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

PROMPT_TMPL = (
    "Translate this user request into JSON filter conditions for Calgary building data.\n"
    "The possible filter keys are:\n"
    "- area_min (number, minimum area in m)\n"
    "- area_max (number, maximum height in m)\n"
    "- length_min (number, minimum length in m)\n"
    "- length_max (number, maxmimum length in m)\n"
    "- description (string, building type)\n"
    "Return JSON only.\n\nUser request: \"{q}\""
)

import re

def parse_query(user_text):
    prompt = PROMPT_TMPL.format(q=user_text)
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    response.raise_for_status()
    result = response.json()

    try:
        # Attempt to extract JSON block from generated text using regex
        raw_output = result[0]["generated_text"]
        match = re.search(r"{.*}", raw_output, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {}
    except (KeyError, json.JSONDecodeError):
        return {}

def building_matches(building, filters):
    if "area_min" in filters and building.get("area", 0) < filters["area_min"]:
        return False
    if "area_max" in filters and building.get("area", 0) > filters["area_max"]:
        return False
    if "length_min" in filters and building.get("length", 0) < filters["length_min"]:
        return False
    if "length_max" in filters and building.get("length", 0) > filters["length_max"]:
        return False
    if "description" in filters and building.get("description", "") != filters["description"]:
        return False
    return True
