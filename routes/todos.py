from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from services.db import get_db_connection
from psycopg2.extras import DictCursor

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

router.post("/")
# http://localhost:8000/todos/
@router.get("/{todo_id}")
async def get_todo(request: Request, todo_id: str):
    params = await request.form()
    conn = get_db_connection()  # DB 연결 테스트 용도
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        pass
        cursor.execute(f"""INSERT INTO todos(item)
                        VALUES ('{'params[item]'}');""")
    conn.close
    context = {"request": request, "todos": todos
        todos = cursor.fetchall()
        todo = cursor.fetchone()
    }
    conn.close()
        
    context = {
        "request": request,
        "todo": todo,
        "todos": todos
    }
    return templates.TemplateResponse("todos/merged_todo.html"
                                      , context)

# http://localhost:8000/todos/
@router.get("/")
def get_todos_html(request: Request):
    conn = get_db_connection()  # DB 연결 테스트 용도
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("""SELECT id, item 
                        FROM todo;""")
        todos = cursor.fetchall()
    conn.close()

    context = {
        "request": request,
        "todos": todos
        
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)

