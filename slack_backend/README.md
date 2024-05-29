Development notes and subtleties

- If there's a requirements.txt, Chalice will package it automatically (if not you need to install into vendor)
- config.json needs to be edited appropriately with secrets and such
- app.py can lead to timeouts


Limitations

- Chalice is setup to make simple functions very easy
- It can install and zip dependencies but it does them via the Lambda zip package
- It can support multiple files BUT you need to put the importable ones into a chalicelib folder
- The main file must be called app.py