from fastapi import FastAPI
from .auth.routers import router as auth_router  # Import the router from auth/routers.py    
from .tasks.routers import router as task_router  # Import the router from tasks/routers.py
# from analytics.routers import router as analytics_router  # Import the router from analytics/routers.py

app = FastAPI(
    title="Task Management",
    description="Task Management API.",
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
# app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

# Run using: uvicorn app.main:app --reload