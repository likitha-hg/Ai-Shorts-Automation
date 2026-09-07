import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-flash-latest")


def research_topic(data: dict):

    title = data.get("title", "")
    hook = data.get("hook", "")
    keywords = data.get("keywords", [])
    target_audience = data.get("target_audience", "")

    prompt = f"""
You are a research assistant for YouTube Shorts creators.

Analyze this topic and collect useful information.

Title:
{title}

Hook:
{hook}

Keywords:
{", ".join(keywords)}

Target Audience:
{target_audience}

Find:

1. Important facts
2. Surprising statistics
3. Trending relevance
4. Common myths or mistakes
5. Real-world examples
6. Interesting insights people may not know

Rules:
- Keep it concise
- Keep it factual
- Focus on valuable content for short-form storytelling
- Make it useful for script writing
- Avoid filler

Return only research notes.
"""

    response = model.generate_content(prompt)

    if not response.text:
        raise Exception("Research generation failed")

    return response.text.strip()