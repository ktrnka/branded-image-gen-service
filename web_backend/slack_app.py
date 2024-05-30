from pprint import pprint
import random
from typing import Dict, NamedTuple
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

from branding import BrandIndex
from prompting import MetaPrompter
from database import Database
from generators import aws_bedrock, openai
from publish_to_s3 import publish_to_s3

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

brand_index = BrandIndex(embedding_path="BAAI/bge-large-en-v1.5")
image_cache_dir = "web_backend/static/images"

database = Database("./data.db")
database.setup()

app = App(token=SLACK_BOT_TOKEN)

generation_backends = [
    aws_bedrock.Titan(image_cache_dir),
    openai.DallE(image_cache_dir),
]

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
            "text": {"type": "mrkdwn", "text": f"This creation was brought to you by <@{user_id}>"},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"_Engine:_ {response.engine}"},
        },
        {"type": "section", "text": {"type": "mrkdwn", "text": f"_Prompt after brand-injection:_ {response.prompt}"}},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "\n".join([f"{key}: {value}" for key, value in sorted(response.about.items())])
				}
			]
		}
    ]


def generate_image(prompt: str):
    """
    Generate an image based on the prompt and log it to the database.

    Errors:
    OpenAIError: If there is an error with the OpenAI API.
    ClientError: If there is an error with the AWS API.
    """
    company, match_score = brand_index.find_match(prompt)

    prompter = MetaPrompter()
    augmented_prompt = prompter.adjust_prompt(
        prompt, company["name"], max_chars=400
    )

    # titan = aws_bedrock.Titan(image_cache_dir)
    engine = random.choice(generation_backends)

    image_result = engine.generate(augmented_prompt)

    local_relative_url = f"/static/images/{image_result.filename}"

    database.log_image(
        prompt,
        company["name"],
        match_score,
        augmented_prompt,
        engine.model_name,
        local_relative_url,
        image_result.response_metadata,
    )

    public_image_url = publish_to_s3(image_result.path)

    return GenerationResponse(
        image_url=public_image_url,
        engine=engine.model_name,
        prompt=augmented_prompt,
        about={
            "Brand selection": f"{company['name']} ({match_score:.2f})",
            "Original prompt": prompt,
        }
    )

@app.command("/futurecrap")
def respond_to_slack_within_3_seconds(ack, payload, say):
    ack("Processing...")

    pprint(payload)

    prompt = payload["text"]

    try:
        response = generate_image(prompt)
        say(
            blocks=format_response(payload, response),
            text="Generated image",
        )
    except Exception as e:
        pprint(e)
        say(f"An error occurred while generating the image: {e}")
        return


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
