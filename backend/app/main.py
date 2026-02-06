"""
FastAPI Main Application
Financial Health Assessment Tool for SMEs
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from pathlib import Path

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, business, financial_data, assessment, reports

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create upload directory
Path(settings.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered financial health assessment platform for SMEs",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    logger.info("Starting Financial Health Assessment Tool...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup tasks on shutdown"""
    logger.info("Shutting down Financial Health Assessment Tool...")


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "error": str(exc) if settings.DEBUG else "Internal server error"
        }
    )


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.APP_VERSION
    }


# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    business.router,
    prefix=f"{settings.API_V1_PREFIX}/business",
    tags=["Business Management"]
)

app.include_router(
    financial_data.router,
    prefix=f"{settings.API_V1_PREFIX}/financial-data",
    tags=["Financial Data"]
)

app.include_router(
    assessment.router,
    prefix=f"{settings.API_V1_PREFIX}/assessment",
    tags=["Financial Assessment"]
)

app.include_router(
    reports.router,
    prefix=f"{settings.API_V1_PREFIX}/reports",
    tags=["Reports"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
