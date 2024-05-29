import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

@app.command("/futurejunk")
def respond_to_slack_within_3_seconds(ack, payload, respond, say):
    ack()

    time.sleep(2)
    say(f"What's up? I'm a Chalice app running on a laptop :wave:. You said: {payload['text']}")



if __name__ == "__main__":
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()