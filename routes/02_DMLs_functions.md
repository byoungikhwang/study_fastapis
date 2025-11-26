```
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.db import get_db_connection

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


@router.post("/")
async def create_todo(request: Request):
    params = await request.form()
    conn = get_db_connection()
    with conn:
        conn.execute("INSERT INTO todos (item) VALUES (?)", (params.get("item"),))
    conn.close()
    return RedirectResponse(url="/todos/", status_code=303)


# http://localhost:8000/todos/
@router.get("/{todo_id}")
async def get_todo(request: Request, todo_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item FROM todos WHERE id = ?", (todo_id,))
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item FROM todos ORDER BY id ASC;")
    todos = cursor.fetchall()
    conn.close()

    context = {
        "request": request,
        "todos": todos
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)


@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: str):
    conn = get_db_connection()
    with conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.close()
    return RedirectResponse(url="/todos/", status_code=303)
```
