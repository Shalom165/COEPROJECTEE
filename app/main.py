from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from app.api.search import router as search_router
from app.api.documents import router as documents_router
from app.api.analytics import router as analytics_router
from app.api.feedback import router as feedback_router
from app.api.audit import router as audit_router
from app.api.ranking_config import router as ranking_config_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Evidence-Ranked Enterprise Search Tool for Architecture Decisions API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(search_router)
app.include_router(documents_router)
app.include_router(analytics_router)
app.include_router(feedback_router)
app.include_router(audit_router)
app.include_router(ranking_config_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
