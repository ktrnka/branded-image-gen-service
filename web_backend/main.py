from pprint import pprint
from fastapi.responses import HTMLResponse
import re


from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from txtai.embeddings import Embeddings

from .generators import aws_bedrock, openai
from .database import Database
from .prompting import MetaPrompter, adjust_prompt

from botocore.errorfactory import ClientError
from openai import OpenAIError

from .data import companies

# Index the brands
embeddings = Embeddings(content=True, path="BAAI/bge-small-en-v1.5")
embeddings.index(
    [f"{company['market']}\n{company['brand_identity']}" for company in companies]
)


image_cache_dir = "web_backend/static/images"

database = Database("./data.db")
database.setup()

# Setup the API
api = FastAPI()
api.mount("/static", StaticFiles(directory="web_backend/static"), name="static")


@api.get("/")
def route():
    with open("web_backend/static/demo.html", "r") as file:
        content = file.read()
    return HTMLResponse(content)


@api.get("/augment")
def augment(prompt: str):
    response = []

    for result in embeddings.search(prompt, limit=3):
        company_index = int(result["id"])
        company = companies[company_index]

        augmented_prompts = [adjust_prompt(prompt, company["name"]) for _ in range(3)]

        response.append(
            {
                "company": company["name"],
                "company_match_score": result["score"],
                "augmented_prompts": augmented_prompts,
            }
        )

    return response


@api.get("/augment_v2")
def augment_v2(prompt: str):
    result = embeddings.search(prompt, limit=1)[0]
    company_index = int(result["id"])
    company = companies[company_index]

    prompter = MetaPrompter()
    augmented_prompt = prompter.adjust_prompt(prompt, company["name"])

    return {
        "company": company["name"],
        "company_match_score": result["score"],
        "augmented_prompt": augmented_prompt,
    }


@api.get("/generate/dalle")
def generate(prompt: str):
    result = embeddings.search(prompt, limit=1)[0]
    company_index = int(result["id"])
    company = companies[company_index]
    augmented_prompt = adjust_prompt(prompt, company["name"])

    dalle = openai.DallE(image_cache_dir)
    image_result = dalle.generate(augmented_prompt)

    local_relative_url = f"/static/images/{image_result.filename}"

    database.log_image(
        prompt,
        company["name"],
        result["score"],
        augmented_prompt,
        dalle.model_name,
        local_relative_url,
        image_result.response_metadata,
    )

    return {
        "company": company["name"],
        "company_match_score": result["score"],
        "prompt": augmented_prompt,
        "model_backend": dalle.model_name,
        "local_path": local_relative_url,
    }


@api.get("/generate/titan")
def generate_aws(prompt: str):
    result = embeddings.search(prompt, limit=1)[0]
    company_index = int(result["id"])
    company = companies[company_index]

    try:
        prompter = MetaPrompter()
        augmented_prompt = prompter.adjust_prompt(prompt, company["name"], max_chars=400)
    except OpenAIError as e:
        pprint(e)
        raise HTTPException(
            status_code=500, detail=f"OpenAI Error: {e}"
        )

    titan = aws_bedrock.Titan(image_cache_dir)

    try:
        image_result = titan.generate(augmented_prompt)
    except ClientError as e:
        pprint(e.response)
        raise HTTPException(
            status_code=400, detail=f"AWS Error: {e.response['Error']['Message']}"
        )

    local_relative_url = f"/static/images/{image_result.filename}"

    database.log_image(
        prompt,
        company["name"],
        result["score"],
        augmented_prompt,
        titan.model_name,
        local_relative_url,
        image_result.response_metadata,
    )

    # Return the filename and image path
    return {
        "company": company["name"],
        "company_match_score": result["score"],
        "prompt": augmented_prompt,
        "model_backend": titan.model_name,
        "local_path": local_relative_url,
    }


def munge_local_path(path: str) -> str:
    return re.sub(r"^(backend|web_backend)", "", path)


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