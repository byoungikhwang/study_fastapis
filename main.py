from fastapi import FastAPI
app = FastAPI()
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
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import Response

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)

templates = Jinja2Templates(directory="templates/")

# http://localhost:8000/main_html
@app.get("/main_html")
async def main_html(request: Request):
    return templates.TemplateResponse("main.html"
                                      , {"request": request})

# http://localhost:8000/main_context_html
@app.get("/main_html_context")
async def main_html_context(request: Request):
    # 템플렛에 전달할 데이타
    context ={
        "request": request,
        "title": "fastapi + jinja exaple",
        "items": ["apple", "banana","cherry"],
        "user": {"name": "sanghun", "age": 33}
    }
    

    return templates.TemplateResponse("main_context.html"
                                      , context)

# http://localhost:8000/
@app.get("/users_list")
async def user_list(request: Request):
    sample_users = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 24, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"},
    ]
    context = {
        "request": request,
        "users_list": sample_users
        }
    return templates.TemplateResponse("users/list.html"
                                      , context)

# 정적 파일 설정
from fastapi.staticfiles import StaticFiles
app.mount("/images", StaticFiles(directory = "resources/images"))
app.mount("/css", StaticFiles(directory = "resources/css"))    


pass