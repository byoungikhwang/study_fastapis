from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routes import notices

app = FastAPI(
    title="Toy Project - Notices CRUD",
    description="A simple FastAPI project to demonstrate CRUD operations for notices.",
    version="1.0.0"
)

# Include the router for the notices API
app.include_router(notices.router)

@app.get("/", include_in_schema=False)
def root():
    """
    Redirects the root URL to the notices HTML list page.
    """
    return RedirectResponse(url="/notices/")