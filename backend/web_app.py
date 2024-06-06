import json
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles

from .code_version import git_sha

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

image_cache_dir = "backend/static/images"
titan = aws_bedrock.Titan(image_cache_dir)
dalle = openai.DallE(image_cache_dir)

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


@api.get("/generate/dalle")
def generate_dalle(prompt: str):
    return generate_image(prompt, dalle)


@api.get("/generate/titan")
def generate_aws(prompt: str):
    return generate_image(prompt, titan)




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

