from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from psycopg2.extras import DictCursor
from typing import List

from ..models.notices import Notice, NoticeCreate, NoticeUpdate
from ..services.db import get_cursor

router = APIRouter(
    prefix="/notices",
    tags=["notices"]
)

# Setup templates
templates = Jinja2Templates(directory="toyproject_fastapis/templates")

@router.post("/", response_model=Notice, status_code=201)
def create_notice(notice: NoticeCreate, cursor: DictCursor = Depends(get_cursor)):
    """
    Create a new notice.
    """
    sql = "INSERT INTO notices (title, content) VALUES (%s, %s) RETURNING id, title, content, created_at;"
    cursor.execute(sql, (notice.title, notice.content))
    new_notice_record = cursor.fetchone()
    if not new_notice_record:
        raise HTTPException(status_code=500, detail="Failed to create notice.")
    cursor.connection.commit()
    return new_notice_record

@router.get("/", response_class=HTMLResponse)
def read_notices_html(request: Request, cursor: DictCursor = Depends(get_cursor)):
    """
    Retrieve all notices and display them in an HTML page.
    """
    sql = "SELECT id, title, content, created_at FROM notices ORDER BY created_at DESC;"
    cursor.execute(sql)
    notices = cursor.fetchall()
    return templates.TemplateResponse("notices.html", {"request": request, "notices": notices})

@router.get("/{notice_id}", response_model=Notice)
def read_notice(notice_id: int, cursor: DictCursor = Depends(get_cursor)):
    """
    Read a single notice by its ID.
    """
    sql = "SELECT id, title, content, created_at FROM notices WHERE id = %s;"
    cursor.execute(sql, (notice_id,))
    notice = cursor.fetchone()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.put("/{notice_id}", response_model=Notice)
def update_notice(notice_id: int, notice: NoticeUpdate, cursor: DictCursor = Depends(get_cursor)):
    """
    Update a notice by its ID.
    """
    sql = "UPDATE notices SET title = %s, content = %s WHERE id = %s RETURNING id, title, content, created_at;"
    cursor.execute(sql, (notice.title, notice.content, notice_id))
    updated_notice = cursor.fetchone()
    if not updated_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    cursor.connection.commit()
    return updated_notice

@router.delete("/{notice_id}", status_code=204)
def delete_notice(notice_id: int, cursor: DictCursor = Depends(get_cursor)):
    """
    Delete a notice by its ID.
    """
    sql = "DELETE FROM notices WHERE id = %s RETURNING id;"
    cursor.execute(sql, (notice_id,))
    deleted = cursor.fetchone()
    if not deleted:
        raise HTTPException(status_code=404, detail="Notice not found")
    cursor.connection.commit()
    return

