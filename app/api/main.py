from fastapi import FastAPI

from app.api.routers.applications import router as applications_router
from app.api.routers.companies import router as companies_router

app = FastAPI(
    title="CareerTrack API",
    description=(
        "API for tracking jobs, internships, applications, "
        "interviews, and follow-ups."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(companies_router)
app.include_router(applications_router)