import json
from pprint import pprint
import random
from typing import Dict, NamedTuple
from openai import OpenAIError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

from .branding import BrandIndex
from .prompting import MetaPrompter
from .database import Database
from .generators import aws_bedrock, openai
from .publish_to_s3 import publish_to_s3
from .core import Cost
from .code_version import git_sha

load_dotenv(verbose=True)

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

brand_index = BrandIndex(embedding_path="BAAI/bge-small-en-v1.5")
image_cache_dir = "backend/static/images"

database = Database("./data.db")
database.setup()

app = App(token=SLACK_BOT_TOKEN)

generation_backends = [
    aws_bedrock.Titan(image_cache_dir),
    openai.DallE(image_cache_dir),
]

COST = Cost.HIGH

class GenerationResponse(NamedTuple):
    image_url: str
    engine: str
    prompt: str
    about: Dict[str, str]


def format_response(payload, response: GenerationResponse):
    user_id = payload["user_id"]
    return [
        {
            "type": "image",
            "image_url": response.image_url,
            "alt_text": response.prompt,
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"This creation was brought to you by <@{user_id}>",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"_Engine:_ {response.engine}"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"_Prompt after brand-injection:_ {response.prompt}",
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "\n".join(
                        [
                            f"{key}: {value}"
                            for key, value in sorted(response.about.items())
                        ]
                    ),
                }
            ],
        },
    ]


def generate_image(prompt: str):
    """
    Generate an image based on the prompt and log it to the database.

    Errors:
    OpenAIError: If there is an error with the OpenAI API.
    ClientError: If there is an error with the AWS API.
    """
    company, match_score = brand_index.find_match(prompt, randomization_pool_size=3)

    engine = random.choice(generation_backends)

    # For some reason the high cost prompter is just worse
    prompter = MetaPrompter(cost=Cost.LOW)
    augmented_prompt = prompter.adjust_prompt(
        prompt,
        company,
        image_engine_hints=engine.hints,
    )

    image_result = engine.generate(augmented_prompt, cost=COST)

    local_relative_url = f"/static/images/{image_result.filename}"

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
        local_relative_url,
        debug_info,
    )

    public_image_url = publish_to_s3(image_result.path)

    about = {
        "Brand selection": f"{company.name} ({match_score:.2f})",
        "Original prompt": prompt,
    }

    try:
        about["DALL-E's revision"] = image_result.debug_info["response"]["revised_prompt"]
    except:
        pass

    return GenerationResponse(
        image_url=public_image_url,
        engine=engine.model_name,
        prompt=augmented_prompt,
        about=about,
    )


@app.command("/futurecrap")
def process_prompt(ack, payload, say, respond):
    pprint(payload)

    prompt = payload["text"]

    ack(f"Imagining crappy ads with _{prompt}_ (takes a few seconds)...")

    try:
        response = generate_image(prompt)
        say(
            blocks=format_response(payload, response),
            text="Generated image",
        )
    except OpenAIError as e:
        respond(f"OpenAI error: {e}")
    except Exception as e:
        # TODO: For Inapprop error, retry using OpenAI instead of AWS
        respond(f"Error: {e}")


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
