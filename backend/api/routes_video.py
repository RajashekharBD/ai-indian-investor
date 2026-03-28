from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
import uuid
from tools.video_builder import VideoBuilder

router = APIRouter()
video_builder = VideoBuilder()
jobs: Dict[str, dict] = {}

class VideoRequest(BaseModel):
    type: str = "market_wrap"
    symbols: list = ["NIFTY", "BANKNIFTY"]
    duration_seconds: int = 60

@router.post("/generate-video")
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    job_id = f"vid_{uuid.uuid4().hex[:8]}"
    
    jobs[job_id] = {
        "status": "processing",
        "type": request.type,
        "symbols": request.symbols
    }
    
    background_tasks.add_task(
        video_builder.generate,
        job_id=job_id,
        video_type=request.type,
        symbols=request.symbols,
        duration=request.duration_seconds
    )
    
    return {
        "job_id": job_id,
        "status": "processing",
        "estimated_time_seconds": 45
    }

@router.get("/video-status/{job_id}")
async def get_video_status(job_id: str):
    if job_id not in jobs:
        return {"status": "not_found"}
    return jobs[job_id]

@router.get("/videos")
async def list_videos():
    return {"videos": list(jobs.values())}
