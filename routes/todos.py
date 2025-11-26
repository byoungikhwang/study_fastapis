from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.db import get_db_connection
from psycopg2.extras import DictCursor
from uuid import UUID

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


@router.post("/")
async def create_todo(request: Request):
    params = await request.form()
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("INSERT INTO todos (item) VALUES (%s)", (params.get("item"),))
        conn.commit()
    conn.close()
    return RedirectResponse(url="/todos/", status_code=303)


# http://localhost:8000/todos/
@router.get("/{todo_id}")
async def get_todo(request: Request, todo_id: UUID):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("SELECT id, item FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()
        cursor.execute("SELECT id, item FROM todos ORDER BY id ASC")
        todos = cursor.fetchall()
    conn.close()

    context = {
        "request": request,
        "todo": todo,
        "todos": todos
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)


# http://localhost:8000/todos/
@router.get("/")
def get_todos_html(request: Request):
    conn = get_db_connection()  # DB 연결 테스트 용도
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("""SELECT id, item 
                        FROM todos ORDER BY id ASC;""")
        todos = cursor.fetchall()
    conn.close()

    context = {
        "request": request,
        "todos": todos
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)


@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: UUID):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()
    conn.close()
    return RedirectResponse(url="/todos/", status_code=303)
