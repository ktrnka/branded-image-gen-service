import random
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from txtai.embeddings import Embeddings
from openai import OpenAI

from .data import companies, prompt_templates
import uuid
from urllib.parse import urlparse

# Index the brands
embeddings = Embeddings(content=True, path="BAAI/bge-small-en-v1.5")
embeddings.index([f"{company['market']}\n{company['brand_identity']}" for company in companies])

# Setup OpenAI
openai_client = OpenAI()

image_cache_dir = "backend/static/images"

# Setup the API
api = FastAPI()
api.mount("/static", StaticFiles(directory="backend/static"), name="static")


def adjust_prompt(prompt: str, company_name: str) -> str:
    template = random.choice(prompt_templates)
    return template.format(prompt=prompt, company_name=company_name)


@api.get("/")
def route():
    return {"status": "ok"}

@api.get("/augment")
def augment(prompt: str):
    response = []

    for result in embeddings.search(prompt, limit=3):
        company_index = int(result['id'])
        company = companies[company_index]

        augmented_prompts = [adjust_prompt(prompt, company["name"]) for _ in range(3)]

        response.append({
            "company": company["name"],
            "company_match_score": result["score"],
            "augmented_prompts": augmented_prompts
        })

    return response

@api.get("/generate")
def generate(prompt: str):
    result = embeddings.search(prompt, limit=1)[0]
    company_index = int(result['id'])
    company = companies[company_index]
    augmented_prompt = adjust_prompt(prompt, company["name"])

    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=augmented_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    response_data = response.data[0]
    response_url = response_data.url

    # Extract the filename from the URL
    parsed_url = urlparse(response_url)
    image_filename = parsed_url.path.split("/")[-1]

    image_path = f"{image_cache_dir}/{image_filename}"
    with open(image_path, "wb") as f:
        f.write(requests.get(response_url).content)

    # Return the filename and image path
    return {
        "company": company["name"],
        "company_match_score": result["score"],
        "prompt": augmented_prompt,
        "openai_response": response_data,
        "local_path": f"/static/images/{image_filename}"
    }
