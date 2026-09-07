import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_scenes(script: str, duration: int = 60):

    # Dynamic scene count based on duration
    scene_count = max(3, min(10, duration // 12))

    prompt = f"""
You are a cinematic scene planner for YouTube Shorts.

Break this narration into exactly {scene_count} visual scenes.

Narration:
{script}

Rules:
- Return exactly {scene_count} scenes
- One scene per line
- Follow the story in chronological order
- Describe ONLY visuals
- No narration text
- No numbering
- No bullet points
- No explanations
- Each scene must look different
- Cinematic
- Realistic
- High detail
- Suitable for stock video search
- Focus on actions, environments, emotions, objects

Return only scene descriptions.
"""

    response = model.generate_content(prompt)

    if not response.text:
        raise Exception("Scene generation failed")

    scenes = [
        line.strip()
        for line in response.text.split("\n")
        if line.strip()
    ]

    # Ensure exact scene count
    if len(scenes) < scene_count:
        while len(scenes) < scene_count:
            scenes.append(scenes[-1])

    scenes = scenes[:scene_count]

    return scenes