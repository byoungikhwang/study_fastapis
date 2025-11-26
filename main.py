from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Import both routers
from routes.todos import router as todos_router
from routes.notices import router as notices_router # New import

# Import database initializers
from services.todos_db import init_db as init_todos_db # Renamed for clarity
from services.notices_db import init_db as init_notices_db # New import

# Initialize both databases
init_todos_db()
init_notices_db() # New call

app = FastAPI(
    title="Combined App - Todos & Notices",
    description="FastAPI app with Todos (SQLite) and Notices (PostgreSQL).",
    version="1.0.0"
)

# Include both routers
app.include_router(todos_router)
app.include_router(notices_router) # New include

# Mount static files
app.mount("/images", StaticFiles(directory="resources/images"), name="images")
app.mount("/css", StaticFiles(directory="resources/css"), name="css")


@app.get("/")
def root():
    # Redirect to the todos list by default, or maybe a simple index page
    return RedirectResponse(url="/web/todos/")
 # Redirect to the HTML list of todos