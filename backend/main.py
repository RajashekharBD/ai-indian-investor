from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Indian Investor API",
    description="Multi-agent investment intelligence platform for the ET AI Hackathon 2026.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from api import routes_chat, routes_radar, routes_analysis, routes_video, routes_market

# Register routers
app.include_router(routes_chat.router, prefix="/api", tags=["Chat"])
app.include_router(routes_radar.router, prefix="/api", tags=["Radar"])
app.include_router(routes_analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(routes_video.router, prefix="/api", tags=["Video"])
app.include_router(routes_market.router, prefix="/api", tags=["Market"])

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint for the AI Indian Investor API.
    """
    return {
        "name": "AI Indian Investor API",
        "version": "1.0.0",
        "hackathon": "ET AI Hackathon 2026",
        "status": "online",
        "documentation": "/api/docs"
    }

@app.get("/health", tags=["General"])
async def health():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy", "timestamp": "2026-03-28T23:25:00Z"}
