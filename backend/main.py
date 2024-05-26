from fastapi import FastAPI
from txtai.embeddings import Embeddings
from .data import companies, prompt_templates
import random

embeddings = Embeddings(content=True, path="BAAI/bge-small-en-v1.5")
embeddings.index([f"{company['market']}\n{company['brand_identity']}" for company in companies])

api = FastAPI()

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
