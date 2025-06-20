"""
Main entry point for the Robot Arm Control System.

This module initializes and runs the FastAPI application.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router as api_router
from .api.middleware import LoggingMiddleware


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI application
app = FastAPI(
    title="Robot Arm Control System",
    description="REST API for controlling a robotic arm",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include API router
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Robot Arm Control System",
        "version": "1.0.0",
        "description": "REST API for controlling a robotic arm",
        "documentation": "/docs"  # Swagger UI endpoint
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 