# # FastAPI 기본 구현
from fastapi import FastAPI
app = FastAPI()             # 웹 네트웍에서 함수를 사용하기 위해 app에 담음
#http://localhost:8000/html 
@app.get("/html")           # 펑션을 호출
async def root():
    return {"message": "saintjin Hello, World!"}
def root_html():
    html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <div>My name saintjin </div>
        </body>
        </html>
        '''
    return html_content
pass








# # FastAPI 기본 구현
# from fastapi import FastAPI

# app = FastAPI()         # 웹 네트웍에서 함수를 사용하기 위해 app에 담음

# @app.get("/")           # 펑션을 호출
# async def root():
    
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>
# <div> my name saintjin </div>
# </body>
# </html>
#     return {"message": "Hello World"}
# pass
