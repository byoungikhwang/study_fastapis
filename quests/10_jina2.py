from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"))

products = [
    {
        "name": "Laptop",
        "price": 1200,
        "tags": ["electronics", "office"]
    },
    {
        "name": "Smartphone",
        "price": 800,
        "tags": ["mobile", "electronics"]
    },
    {
        "name": "Keyboard",
        "price": 100,
        "tags": ["accessories"]
    }
]

@app.get("/")
async def read_products(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "products": products})
