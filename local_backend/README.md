
# Web app (web_app.py)

This runs a web app locally where I test the system. It's setup to run in low-cost mode which uses lower quality settings for the models.

# Slack Bot (slack_app.py)

This is a demo of running Slack Bolt in Socket Mode on my local machine to respond to Slack messages in the ex-98point6 Slack group.

Nice aspects of this:
- Easy to install dependencies
- Easy to install / cache the embedding model on lookup
- Easy to control secrets

Not so nice aspects:
- It only runs on my machine
- It probably wouldn't be able to run long-term
