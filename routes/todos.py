from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from services.todos_db import get_db_connection # Renamed import
from models.todos import Todo, TodoCreate, TodoUpdate # new import
from typing import List

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# API Endpoints (RESTful, return JSON)

@router.post("/todos/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo_json(todo: TodoCreate, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    sql = "INSERT INTO todos (content, status, deadline_time) VALUES (?, ?, ?) RETURNING id, content, status, create_time, deadline_time;"
    cursor.execute(sql, (todo.content, todo.status, todo.deadline_time))
    new_todo_record = cursor.fetchone()
    conn.commit()
    conn.close()
    if not new_todo_record:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create todo.")
    return Todo(**new_todo_record)

@router.get("/todos/", response_model=List[Todo])
async def read_all_todos_json(conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, status, create_time, deadline_time FROM todos ORDER BY id ASC;")
    todos_records = cursor.fetchall()
    conn.close()
    return [Todo(**record) for record in todos_records]

@router.get("/todos/{todo_id}", response_model=Todo)
async def read_single_todo_json(todo_id: int, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, status, create_time, deadline_time FROM todos WHERE id = ?", (todo_id,))
    todo_record = cursor.fetchone()
    conn.close()
    if not todo_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return Todo(**todo_record)

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo_json(todo_id: int, todo: TodoUpdate, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    sql = "UPDATE todos SET content = ?, status = ?, deadline_time = ? WHERE id = ? RETURNING id, content, status, create_time, deadline_time;"
    cursor.execute(sql, (todo.content, todo.status, todo.deadline_time, todo_id))
    updated_todo = cursor.fetchone()
    conn.commit()
    conn.close()
    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return Todo(**updated_todo)

@router.patch("/todos/{todo_id}", response_model=Todo)
async def partial_update_todo_json(todo_id: int, todo: TodoUpdate, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, status, create_time, deadline_time FROM todos WHERE id = ?", (todo_id,))
    existing_todo_record = cursor.fetchone()
    if not existing_todo_record:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    existing_todo = Todo(**existing_todo_record)
    
    update_fields = []
    update_values = []
    
    # Only update fields that are provided in the request
    if todo.content is not None:
        update_fields.append("content = ?")
        update_values.append(todo.content)
    if todo.status is not None:
        update_fields.append("status = ?")
        update_values.append(todo.status)
    if todo.deadline_time is not None:
        update_fields.append("deadline_time = ?")
        update_values.append(todo.deadline_time)

    if not update_fields:
        conn.close()
        return existing_todo # No changes requested

    update_values.append(todo_id)
    sql = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ? RETURNING id, content, status, create_time, deadline_time;"
    cursor.execute(sql, tuple(update_values))
    updated_todo = cursor.fetchone()
    conn.commit()
    conn.close()
    return Todo(**updated_todo)

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_json(todo_id: int, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ? RETURNING id;", (todo_id,))
    deleted_id = cursor.fetchone()
    conn.commit()
    conn.close()
    if not deleted_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return

# HTML Endpoints (for web UI, these will be used for redirects and template rendering)

@router.get("/web/todos/", response_class=HTMLResponse)
def read_todos_html_list(request: Request, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, status, create_time, deadline_time FROM todos ORDER BY id ASC;")
    todos_records = cursor.fetchall()
    conn.close()
    todos = [Todo(**record) for record in todos_records]
    context = {
        "request": request,
        "todos": todos
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)

@router.get("/web/todos/{todo_id}", response_class=HTMLResponse)
async def read_todo_html_detail(request: Request, todo_id: int, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, status, create_time, deadline_time FROM todos WHERE id = ?", (todo_id,))
    todo_record = cursor.fetchone()
    
    # Also fetch all todos for the merged_todo.html template context
    cursor.execute("SELECT id, content, status, create_time, deadline_time FROM todos ORDER BY id ASC")
    todos_records = cursor.fetchall()
    conn.close()

    if not todo_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todo = Todo(**todo_record)
    todos = [Todo(**record) for record in todos_records] # For merged_todo.html context

    context = {
        "request": request,
        "todo": todo,
        "todos": todos
    }
    return templates.TemplateResponse("todos/merged_todo.html", context)

# Original create_todo that redirects to HTML list
@router.post("/web/todos/create/", response_class=RedirectResponse, status_code=status.HTTP_303_SEE_OTHER)
async def create_todo_html_redirect(request: Request, conn=Depends(get_db_connection)):
    params = await request.form()
    content = params.get("item") # Assuming the form field is named "item"
    # Assuming status and deadline_time are optional or handled by default in DB
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty")
    
    cursor = conn.cursor()
    sql = "INSERT INTO todos (content) VALUES (?) RETURNING id;" # Default status and deadline
    cursor.execute(sql, (content,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/web/todos/", status_code=status.HTTP_303_SEE_OTHER)

# Original delete_todo that redirects to HTML list
@router.get("/web/todos/delete/{todo_id}", response_class=RedirectResponse, status_code=status.HTTP_303_SEE_OTHER)
async def delete_todo_html_redirect(todo_id: int, conn=Depends(get_db_connection)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ? RETURNING id;", (todo_id,))
    deleted_id = cursor.fetchone()
    conn.commit()
    conn.close()
    if not deleted_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return RedirectResponse(url="/web/todos/", status_code=status.HTTP_303_SEE_OTHER)
