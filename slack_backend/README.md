Development notes and subtleties

- If there's a requirements.txt, Chalice will package it automatically (if not you need to install into vendor)
- config.json needs to be edited appropriately with secrets and such
- app.py can lead to timeouts
- If the API gateway URL is BASE/api/, you need to set Slack to BASE/api/slack/events or else it will just say dispatch failed
- It was tricky to figure out permissions on the Slack config side. I ended up copy pasting a manifest from a "basic app" tutorial

Limitations

- Chalice is setup to make simple functions very easy
- It can install and zip dependencies but it does them via the Lambda zip package
- It can support multiple files BUT you need to put the importable ones into a chalicelib folder
- The main file must be called app.py

TODO
- I can't tell if it's possible to install txtai in this... it ran for like 20 minutes and spammed the terminal but didn't complete