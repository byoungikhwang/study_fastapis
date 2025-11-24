from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

# http://localhost:8000/
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# http://localhost:8000/html
@app.get("/html")
async def root_html():
    html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Otter</title>
        </head>
        <body>
            <div>My name is Otter!</div>
        </body>
        </html>
        '''
    return html_content

# http://localhost:8000/main_html
@app.get("/main_html")
async def main_html(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# http://localhost:8000/concept_01_html
@app.get("/concept_01_html")
async def concept_01_html(request: Request):
    return templates.TemplateResponse("concept_01.html", {"request": request})

# http://localhost:8000/concept_02_html
@app.get("/concept_02_html")
async def concept_02_html(request: Request):
    return templates.TemplateResponse("concept_02.html", {"request": request})
