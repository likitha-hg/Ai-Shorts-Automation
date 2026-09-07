from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio

from agents.research_service import research_topic
from agents.instruction import build_instruction
from agents.script_service import generate_script
from agents.scene_service import generate_scenes
from agents.stock_video_service import get_stock_video
from agents.voice_service import generate_voice
from agents.video_service import create_video
from agents.fallback_script import description_to_script


app = FastAPI(
    title="AI Shorts Automation",
    description="Generate AI-powered Shorts",
    version="2.0.0"
)

# Static folders
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

# Global pipeline status tracker
pipeline_status = {
    "step": "Idle"
}


class VideoRequest(BaseModel):
    title: str
    hook: str
    keywords: list[str]
    target_audience: str
    duration: int = 60


@app.get("/")
def home():
    return FileResponse("templates/index.html")


# Status endpoint for frontend polling
@app.get("/status")
def get_status():
    return pipeline_status


@app.post("/generate")
def generate_video(request: VideoRequest):
    try:
        # Reset pipeline status
        pipeline_status["step"] = "Starting..."

        print("\n==============================")
        print(f"TITLE: {request.title}")
        print(f"DURATION: {request.duration}")
        print("==============================")

        # Step 1: Create idea object
        idea = {
            "title": request.title,
            "hook": request.hook,
            "keywords": request.keywords,
            "target_audience": request.target_audience,
            "duration": request.duration
        }

        # Step 2: Research
        pipeline_status["step"] = "Researching topic..."
        print("Researching topic...")
        research = research_topic(idea)

        # Step 3: Build strategy
        pipeline_status["step"] = "Building content strategy..."
        print("Building content strategy...")
        strategy = build_instruction(
            idea,
            research
        )

        # Step 4: Generate script
        pipeline_status["step"] = "Generating script..."
        print("Generating script...")

        try:
            script = generate_script(
                idea,
                research,
                strategy
            )
        except Exception as e:
            print(f"Script generation failed: {e}")
            print("Using fallback script...")

            script = description_to_script(
                request.title,
                request.duration
            )

        # Step 5: Generate scenes
        pipeline_status["step"] = "Generating scenes..."
        print("Generating scenes...")

        scenes = generate_scenes(
            script,
            request.duration
        )

        # Step 6: Fetch stock videos
        pipeline_status["step"] = "Fetching stock videos..."
        print("Fetching stock videos...")

        video_paths = []

        for i, scene in enumerate(scenes, start=1):
            pipeline_status["step"] = f"Downloading scene {i}..."

            video_path = get_stock_video(
                scene,
                output_path=f"output/scene_{i}.mp4"
            )

            video_paths.append(video_path)

            print(f"Downloaded scene {i}: {video_path}")

        # Step 7: Generate voice
        pipeline_status["step"] = "Generating voice..."
        print("Generating voice...")

        audio_path = asyncio.run(
            generate_voice(script)
        )

        # Step 8: Create final video
        pipeline_status["step"] = "Creating final video..."
        print("Creating final video...")

        final_video = create_video(
            video_paths=video_paths,
            audio_path=audio_path
        )

        # Final status
        pipeline_status["step"] = "Completed ✅"
        print("Pipeline completed successfully!")

        return {
            "status": "success",
            "idea": idea,
            "research": research,
            "strategy": strategy,
            "script": script,
            "scenes": scenes,
            "audio": audio_path,
            "video": final_video
        }

    except Exception as e:
        pipeline_status["step"] = "Failed ❌"
        print(f"Pipeline Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )