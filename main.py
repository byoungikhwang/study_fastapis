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

# http://localhost:8000/main_html -->guests 변경
@app.get("guests/main_html")        # 과제 경로 guests 폴더
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


# http://localhost:8000/
@app.get("/")     # http://123.1.42.1:8000
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

# http://localhost:8000/board/detail_json?title=Third%20Post&content=This%20is%20the%20third%20post.
@app.get("/board/detail_json")
async def board_details_json(request: Request): # 변수명을 소문자 'request'로 수정 (일반적인 파이썬 컨벤션)
    # 쿼리 파라미터 전체를 딕셔너리로 가져옵니다.
    params = dict(request.query_params)
    
    # 딕셔너리에서 'title'과 'content' 값을 안전하게 추출합니다.
    # 만약 파라미터가 없으면 None을 사용합니다.
    title_value = params.get("title")
    content_value = params.get("content")
    
    # 추출한 변수 값을 JSON 응답에 포함합니다.
    return {
        "title": title_value,   # 'params.title' (문자열) 대신 title_value (변수) 사용
        "content": content_value
    }

# http://localhost:8000/board/detail_post_json?title=Third%20Post&content=This%20is%20the%20third%20post.
# post는 노출하면 안된다. post 방식으로 바꿔 줘야 한다.
@app.post("/board/detail_post_json")
async def board_details_post_json(request: Request): # 변수명을 소문자 'request'로 수정 (일반적인 파이썬 컨벤션)
    # 쿼리 파라미터 전체를 딕셔너리로 가져옵니다.
    params = dict(await request.query_params.form())
    # 딕셔너리에서 'title'과 'content' 값을 안전하게 추출합니다.
    # 만약 파라미터가 없으면 None을 사용합니다.
    title_value = params.get("title")
    content_value = params.get("content")
    
    # 추출한 변수 값을 JSON 응답에 포함합니다.
    return {
        "title": title_value,   # 'params.title' (문자열) 대신 title_value (변수) 사용
        "content": content_value
    }
# http://localhost:8000/board/detail_html
@app.get("/board/detail_html")        # 과제 경로 폴더
async def main_html(request: Request):
    return templates.TemplateResponse("board/detail.html"
                                      , {"request": request})

    
# 정적 파일 설정
from fastapi.staticfiles import StaticFiles
app.mount("/images", StaticFiles(directory = "resources/images"))
app.mount("/css", StaticFiles(directory = "resources/css"))    


pass