from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from routes.todos import router as todos_router

app = FastAPI()

# Include routers
app.include_router(todos_router, prefix="/todos", tags=["todos"])

# Mount static files
app.mount("/images", StaticFiles(directory="resources/images"), name="images")
app.mount("/css", StaticFiles(directory="resources/css"), name="css")


@app.get("/")
def root():
    return RedirectResponse(url="/todos/")