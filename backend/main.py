from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Indian Investor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api import routes_chat, routes_radar, routes_analysis, routes_video, routes_market

app.include_router(routes_chat.router, prefix="/api")
app.include_router(routes_radar.router, prefix="/api")
app.include_router(routes_analysis.router, prefix="/api")
app.include_router(routes_video.router, prefix="/api")
app.include_router(routes_market.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Indian Investor API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
