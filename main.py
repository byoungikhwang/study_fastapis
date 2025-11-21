# FastAPI 기본 구현

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

async def root():

    return {"message": "Hello World"}
##