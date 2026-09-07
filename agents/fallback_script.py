import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def description_to_script(topic: str, duration: int = 60):

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty")

    min_words = int(duration * 2.2)
    max_words = int(duration * 3)

    prompt = f"""
You are a YouTube Shorts creator.

Write a simple and engaging narration script based on this topic.

Topic:
{topic}

Rules:
- Start with an attention-grabbing hook
- Conversational tone
- Easy to understand
- Keep curiosity high
- End with a short call-to-action
- Length between {min_words} and {max_words} words
- Output only plain narration text
- No headings
- No bullet points
- No markdown
"""

    response = model.generate_content(prompt)

    if not response.text:
        raise Exception("Fallback script generation failed")

    return response.text.strip()