import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

from branding import BrandIndex
from prompting import adjust_prompt

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

brand_index = BrandIndex()

app = App(token=SLACK_BOT_TOKEN)


def format_response(image_url: str, engine: str, prompt: str):
    return [
        {
            "type": "image",
            "image_url": image_url,
            "alt_text": prompt,
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"_Engine:_ {engine}"},
        },
        {"type": "section", "text": {"type": "mrkdwn", "text": f"_Prompt:_ {prompt}"}},
    ]


@app.command("/futurejunk")
def respond_to_slack_within_3_seconds(ack, payload, respond, say):
    ack()

    prompt = payload["text"]

    company, match_score = brand_index.find_match(prompt)
    adjusted_prompt = adjust_prompt(prompt, company["name"])

    say(
        blocks=format_response(
            "https://future-junk-images.s3.us-west-2.amazonaws.com/public/00a1bed9-74fc-44a8-8c12-0bd069c86950.jpg",
            "AWS Titan",
            adjusted_prompt,
        ),
        text="Generated image",
    )


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
