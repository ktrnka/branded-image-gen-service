from pprint import pprint
from fastapi.responses import HTMLResponse
import re


from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .publish_to_s3 import publish_to_s3


from .generators import aws_bedrock, openai
from .database import Database
from .prompting import MetaPrompter, adjust_prompt

from botocore.errorfactory import ClientError
from openai import OpenAIError

from .branding import BrandIndex
from dotenv import load_dotenv

# Set up any access keys, etc
load_dotenv()


brand_index = BrandIndex()


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


@api.get("/augment_v2")
def augment_v2(prompt: str):
    company, match_score = brand_index.find_match(prompt)

    prompter = MetaPrompter()
    augmented_prompt = prompter.adjust_prompt(prompt, company["name"])

    return {
        "company": company["name"],
        "company_match_score": match_score,
        "augmented_prompt": augmented_prompt,
    }


@api.get("/generate/dalle")
def generate(prompt: str):
    company, match_score = brand_index.find_match(prompt)
    augmented_prompt = adjust_prompt(prompt, company["name"])

    dalle = openai.DallE(image_cache_dir)
    image_result = dalle.generate(augmented_prompt)

    local_relative_url = f"/static/images/{image_result.filename}"

    database.log_image(
        prompt,
        company["name"],
        match_score,
        augmented_prompt,
        dalle.model_name,
        local_relative_url,
        image_result.response_metadata,
    )

    return {
        "company": company["name"],
        "company_match_score": match_score,
        "prompt": augmented_prompt,
        "model_backend": dalle.model_name,
        "local_path": local_relative_url,
    }


@api.get("/generate/titan")
def generate_aws(prompt: str):
    company, match_score = brand_index.find_match(prompt)

    try:
        prompter = MetaPrompter()
        augmented_prompt = prompter.adjust_prompt(
            prompt, company["name"], max_chars=400
        )
    except OpenAIError as e:
        pprint(e)
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {e}")

    titan = aws_bedrock.Titan(image_cache_dir)

    try:
        image_result = titan.generate(augmented_prompt)
        public_image_url = publish_to_s3(image_result.path)
    except ClientError as e:
        pprint(e.response)
        raise HTTPException(
            status_code=400, detail=f"AWS Error: {e.response['Error']['Message']}"
        )

    local_relative_url = f"/static/images/{image_result.filename}"

    database.log_image(
        prompt,
        company["name"],
        match_score,
        augmented_prompt,
        titan.model_name,
        local_relative_url,
        image_result.response_metadata,
    )

    # Return the filename and image path
    return {
        "company": company["name"],
        "company_match_score": match_score,
        "prompt": augmented_prompt,
        "model_backend": titan.model_name,
        "local_path": public_image_url,
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
