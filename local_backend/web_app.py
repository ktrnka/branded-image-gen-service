from fastapi.responses import HTMLResponse
import re


from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .core import Cost, ImageGeneratorABC

from .publish_to_s3 import publish_to_s3


from .generators import aws_bedrock, openai
from .database import Database
from .prompting import MetaPrompter


from .branding import BrandIndex
from dotenv import load_dotenv

# Set up any access keys, etc
load_dotenv()

# cost setting
COST = Cost.LOW

brand_index = BrandIndex()

image_cache_dir = "local_backend/static/images"
titan = aws_bedrock.Titan(image_cache_dir)
dalle = openai.DallE(image_cache_dir)

database = Database("./data.db")
database.setup()

# Setup the API
api = FastAPI()
api.mount("/static", StaticFiles(directory="local_backend/static"), name="static")


#### ROUTES #####


@api.get("/")
def route():
    with open("local_backend/static/demo.html", "r") as file:
        content = file.read()
    return HTMLResponse(content)


def generate_image(prompt: str, engine: ImageGeneratorABC):
    """
    Generate an image based on the prompt using the given engine.
    """
    company, match_score = brand_index.find_match(prompt, randomization_pool_size=1)

    try:
        prompter = MetaPrompter(cost=Cost.LOW)
        augmented_prompt = prompter.adjust_prompt(
            prompt,
            company,
            image_engine_hints=engine.hints,
        )
    except BaseException as e:
        raise HTTPException(status_code=500, detail=f"Prompt error: {e}")

    try:
        image_result = engine.generate(augmented_prompt, cost=Cost.HIGH)
        public_image_url = publish_to_s3(image_result.path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

    database.log_image(
        prompt,
        company.name,
        augmented_prompt,
        engine.model_name,
        image_result.filename,
        image_result.debug_info,
    )

    return {
        "company": company.name,
        "company_match_score": match_score,
        "prompt": augmented_prompt,
        "model_backend": engine.model_name,
        "image_url": public_image_url,
    }


@api.get("/generate/dalle")
def generate_dalle(prompt: str):
    return generate_image(prompt, dalle)


@api.get("/generate/titan")
def generate_aws(prompt: str):
    return generate_image(prompt, titan)

import os.path
def munge_local_path(path: str) -> str:
    filename = os.path.basename(path)
    return f"/static/images/{filename}"


@api.get("/images", response_class=HTMLResponse)
def show_images():
    rows = database.get_all_images()

    # Generate the HTML table
    table = "<table>"
    table += "<tr><th>Prompt</th><th>Brand Name</th><th>Augmented Prompt</th><th>Model Backend</th><th>Image Path</th><th>Debug info</th></tr>"
    for row in rows:
        table += "<tr>"
        table += f"<td>{row.prompt}</td>"
        table += f"<td>{row.brand_name}</td>"
        table += f"<td>{row.augmented_prompt}</td>"
        table += f"<td>{row.model_backend}</td>"
        table += f"<td><a href='{munge_local_path(row.image_path)}'>{os.path.basename(row.image_path)}</a></td>"
        table += f"<td>{row.debug_info}</td>"
        table += "</tr>"
    table += "</table>"

    # Return the HTML table
    return table


@api.get("/brands", response_class=HTMLResponse)
def show_brands():
    brands = brand_index.get_all_brands()
    brands = sorted(brands, key=lambda brand: brand.name)
    # Generate the HTML table
    table = "<table>"
    table += "<tr><th>Name</th><th>Market</th><th>Brand Identity</th></tr>"
    for brand in brands:
        table += "<tr>"
        table += f"<td>{brand.name}</td>"
        table += f"<td>{brand.market}</td>"
        table += f"<td>{brand.brand_identity}</td>"
        table += "</tr>"
    table += "</table>"
    # Return the HTML table
    return table