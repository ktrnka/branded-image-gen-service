from fastapi import FastAPI


api = FastAPI()


@api.get("/")
def route():
    return {"status": "ok"}
