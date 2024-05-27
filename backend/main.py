import random
from fastapi.responses import HTMLResponse
import requests
from urllib.parse import urlparse
import re


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from txtai.embeddings import Embeddings
from openai import OpenAI

from backend.database import Database

from .data import companies, prompt_templates

# Index the brands
embeddings = Embeddings(content=True, path="BAAI/bge-small-en-v1.5")
embeddings.index([f"{company['market']}\n{company['brand_identity']}" for company in companies])

# Setup OpenAI
openai_client = OpenAI()

image_cache_dir = "backend/static/images"

database = Database("./data.db")
database.setup()

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
            "augmented_prompts": augmented_prompts,
            "model_backend": "DEMO",
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

    local_relative_url = f"/static/images/{image_filename}"

    database.log_image(prompt, company["name"], result["score"], augmented_prompt, "dall-e-3", local_relative_url, response_data.to_json())

    # Return the filename and image path
    return {
        "company": company["name"],
        "company_match_score": result["score"],
        "prompt": augmented_prompt,
        "openai_response": response_data,
        "model_backend": "dall-e-3",
        "local_path": local_relative_url
    }

def munge_local_path(path: str) -> str:
    return re.sub(r"^backend", "", path)

@api.get("/images", response_class=HTMLResponse)
def show_images():
    rows = database.get_all_images()

    # Generate the HTML table
    table = "<table>"
    table += "<tr><th>Prompt</th><th>Brand Name</th><th>Brand Score</th><th>Augmented Prompt</th><th>Model Backend</th><th>Image Path</th><th>OpenAI Response</th></tr>"
    for row in rows:
        table += "<tr>"
        table += f"<td>{row[0]}</td>"
        table += f"<td>{row[1]}</td>"
        table += f"<td>{row[2]}</td>"
        table += f"<td>{row[3]}</td>"
        table += f"<td>{row[4]}</td>"
        table += f"<td><a href='{munge_local_path(row[5])}'>{row[5]}</a></td>"
        table += f"<td>{row[6]}</td>"
        table += "</tr>"
    table += "</table>"

    # Return the HTML table
    return table