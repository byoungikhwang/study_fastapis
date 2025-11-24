from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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
