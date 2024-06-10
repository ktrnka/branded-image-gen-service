import json
from typing import Optional
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles

from .code_version import git_sha

from .core import Brand, Cost, ImageGeneratorABC

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

image_cache_dir = "backend/static/images"
titan = aws_bedrock.Titan(image_cache_dir)
dalle = openai.DallE(image_cache_dir)

engine_lookup = {
    "titan": titan,
    "dalle": dalle,
}

database = Database("./data.db")
database.setup()

# Setup the API
api = FastAPI()

class StaticFilesCache(StaticFiles):
    """
    Wrapper to add cache control headers to static files.
    """
    def __init__(self, *args, cachecontrol="public, max-age=31536000, s-maxage=31536000, immutable", **kwargs):
        self.cachecontrol = cachecontrol
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        return resp

api.mount("/static", StaticFilesCache(directory="backend/static", cachecontrol="public, max-age=3600"), name="static")

@api.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "max-age=600"
    return response

templates = Jinja2Templates(directory="backend/templates")

#### ROUTES #####


@api.get("/")
def route():
    with open("backend/static/demo.html", "r") as file:
        content = file.read()
    return HTMLResponse(content)


def generate_image(prompt: str, unmodified_prompt: bool, engine: ImageGeneratorABC):
    """
    Generate an image based on the prompt using the given engine.
    """

    print(f"unmodified_prompt: {unmodified_prompt}")

    if unmodified_prompt:
        augmented_prompt = prompt

        company = Brand(None, None, None, None)
        match_score = 0
    else:
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
    
    debug_info = {
        "git_sha": git_sha,
    }
    if image_result.debug_info:
        debug_info.update(image_result.debug_info)

    database.log_image(
        prompt,
        company.name,
        augmented_prompt,
        engine.model_name,
        image_result.filename,
        debug_info,
    )

    return {
        "company": company.name,
        "company_match_score": match_score,
        "prompt": augmented_prompt,
        "model_backend": engine.model_name,
        "image_url": public_image_url,
    }

def eval_generate_image(prompt: str, engine: ImageGeneratorABC):
    """
    Generate an image based on the prompt using the given engine for evaluation only.
    """
    company, match_score = brand_index.find_match(prompt, randomization_pool_size=1)

    prompter = MetaPrompter(cost=Cost.LOW)
    augmented_prompt = prompter.adjust_prompt(
        prompt,
        company,
        image_engine_hints=engine.hints,
    )

    debug_info = {
        "git_sha": git_sha,
    }

    try:
        image_result = engine.generate(augmented_prompt, cost=Cost.LOW)

        _ = publish_to_s3(image_result.path)    

        if image_result.debug_info:
            debug_info.update(image_result.debug_info)

        database.log_evaluation_image(
            prompt,
            company.name,
            augmented_prompt,
            engine.model_name,
            git_sha,
            image_result.filename,
            debug_info,
        )
    except aws_bedrock.InappropriatePromptError as e:
        debug_info["error"] = str(e)

        database.log_evaluation_image(
            prompt,
            company.name,
            augmented_prompt,
            engine.model_name,
            git_sha,
            None,
            debug_info,
        )




@api.get("/generate/dalle")
def generate_dalle(prompt: str, unmodified_prompt: bool = False):
    return generate_image(prompt, unmodified_prompt, dalle)


@api.get("/generate/titan")
def generate_aws(prompt: str, unmodified_prompt: bool = False):
    return generate_image(prompt,unmodified_prompt,  titan)




@api.get("/images", response_class=HTMLResponse)
def show_images(request: Request):
    rows = database.get_all_images()

    return templates.TemplateResponse(
        request=request, name="images.html", context={"image_results": rows}
    )

@api.get("/image/{filename}", response_class=HTMLResponse)
def show_image(request: Request, filename: str):
    rows = database.get_all_images()

    # TOOD: Search in SQL not here lol
    row = next((row for row in rows if row.filename == filename), None)

    engine_prompt_revision = None
    pretty_debug_info = None
    if row.debug_info:
        parsed_debug_info = json.loads(row.debug_info)
        pretty_debug_info = json.dumps(parsed_debug_info, indent=3)

        if "response" in parsed_debug_info:
            engine_prompt_revision = parsed_debug_info["response"].get("revised_prompt")
        else:
            engine_prompt_revision = parsed_debug_info.get("revised_prompt")

    return templates.TemplateResponse(
        request=request, name="image.html", context={"result": row, "pretty_debug_info": pretty_debug_info, "engine_prompt_revision": engine_prompt_revision}
    )

@api.get("/brands", response_class=HTMLResponse)
def show_brands(request: Request):
    brands = brand_index.get_all_brands()
    brands = sorted(brands, key=lambda brand: brand.name)

    return templates.TemplateResponse(
        request=request, name="brands.html", context={"brands": brands}
    )

EVALUATION_PROMPTS = """
A dog sitting behind an office desk reading reports
A painting of a serious-looking dog sitting behind an office desk reading reports
A serene lake during sunset with calm waters reflecting a cluster of trees on a small island. The horizon features a line of trees and buildings under a soft, pastel sky transitioning from light pink to pale blue.
An impressionist oil painting showing a middle age man sitting at a table that is balanced on top of a 10 foot tall pyramid of friend chicken. The man is staring at a laptop on the desk which has a colorful sticker of a robot on it. He has a wistful look on his face, as if he's questioning his life choices
College girl studying at a desk listening to lofi hiphop beats with rain outside
parents dropping their kids off at school but with beer ads
the ultimate high-definition technicolor coffee experience in a classic grungy Seattle coffee shop
a humanoid cat hipster barista is looking at you judgmentally while making your frappuccino
i want to see a former tech ceo joyously eating a chicken sandwich in front of the restaurant he started, while a former tech bro stands behind him working furiously on his computer
a poor product manager should be making his roadmap right now, but is instead playing around with a fun gen AI toy that his friend made. as a PM, he understands that life is all about tradeoffs, and this is the tradeoff he made
Two high schoolers are trying to joust with one another using pool noodles while on rollerblades. They have serious, intense expressions while children watch in awe
"""

@api.get("/evaluation/{model_name}", response_class=HTMLResponse)
def evaluate_titan(request: Request, model_name: str, reference_version: str = None):
    engine = engine_lookup[model_name]
        
    # Re-generate images from all prompts if they don't exist yet
    if not database.has_evaluation(git_sha, engine.model_name):
        for prompt in EVALUATION_PROMPTS.strip().split("\n"):
            try:
                eval_generate_image(prompt, engine)
            except Exception as e:
                print(f"Skipping prompt due to error: {e}")
    
    evaluation_rows = database.get_evaluation(engine.model_name, git_sha, reference_version)
    return templates.TemplateResponse(
        request=request, name="evaluation.html", context={"image_results": evaluation_rows, "current_version": git_sha, "reference_version": reference_version}
    )
