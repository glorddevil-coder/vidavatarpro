"""
AuraStudio Omni - Main FastAPI Application
v3.0+ - AI Physicality, Multi-Avatar Social, Health & Wellness
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.config.settings import settings
from app.routes import audio, projects, advanced
from app.routes.advanced_v3 import all_routers as v3_routers

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager
    Startup and shutdown events
    """
    # Startup
    logger.info(f"🚀 Starting AuraStudio Omni v{settings.app_version}")
    logger.info(f"Environment: {settings.api_env}")
    logger.info(f"Database: {settings.database_url}")
    logger.info(f"Vector DB Type: {settings.vector_db_type}")
    
    # Initialize services
    if settings.feature_memory_engine:
        logger.info("✓ Memory Engine enabled")
    if settings.feature_translator:
        logger.info("✓ Global Translator enabled")
    if settings.feature_bonding_system:
        logger.info("✓ Bonding System enabled")
    if settings.feature_health_monitor:
        logger.info("✓ Health Monitor enabled")
    if settings.feature_autonomous_agents:
        logger.info("✓ Autonomous Agents enabled")
    if settings.feature_voice_dna_nft:
        logger.info("✓ Voice DNA NFT enabled")
    if settings.feature_ai_watermarking:
        logger.info("✓ AI Watermarking enabled")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down AuraStudio Omni")


# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.app_name,
    description="AuraStudio Omni - Hyper-Realistic Virtual Human Ecosystem with AI Memory, Translation, Health Monitoring, and Autonomous Agents",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(audio.router, prefix="/api/audio", tags=["Audio"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(advanced.router, prefix="/api/advanced", tags=["Advanced"])

# Include v3+ advanced routers (Digital Physique, Neural Persona, Autonomous Agency, Security/Privacy)
for router in v3_routers:
    app.include_router(router)


# Root endpoints
@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "environment": settings.api_env,
        "documentation": "/api/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.api_env,
    }


@app.get("/api/info")
async def api_info():
    """Get API information and feature status."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.api_env,
        "features": {
            "memory_engine": settings.feature_memory_engine,
            "translator": settings.feature_translator,
            "bonding_system": settings.feature_bonding_system,
            "health_monitor": settings.feature_health_monitor,
            "autonomous_agents": settings.feature_autonomous_agents,
            "voice_dna_nft": settings.feature_voice_dna_nft,
            "ai_watermarking": settings.feature_ai_watermarking,
        },
        "configuration": {
            "vector_db": settings.vector_db_type,
            "audio_sample_rate": settings.audio_sample_rate,
            "memory_vector_dimension": settings.memory_vector_dimension,
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.api_debug,
    )
