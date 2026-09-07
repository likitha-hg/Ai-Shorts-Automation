import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-flash-latest")


def generate_script(data: dict, research: str, strategy: str):

    title = data.get("title", "")
    hook = data.get("hook", "")
    keywords = data.get("keywords", [])
    target_audience = data.get("target_audience", "")
    duration = data.get("duration", 60)

    # Approximate speaking speed
    min_words = int(duration * 2.2)
    max_words = int(duration * 3)

    prompt = f"""
You are an expert YouTube Shorts scriptwriter.

Write a highly engaging YouTube Shorts narration.

Video Details:

Title:
{title}

Hook:
{hook}

Keywords:
{", ".join(keywords)}

Target Audience:
{target_audience}

Research Notes:
{research}

Content Strategy:
{strategy}

Rules:
- Start exactly with the hook
- Conversational and natural
- Fast-paced and engaging
- Keep curiosity high throughout
- Use storytelling flow
- Include valuable insights
- Keep audience retention strong
- End with a strong call-to-action
- Length between {min_words} and {max_words} words
- Match the duration naturally
- Output ONLY narration text
- No headings
- No bullet points
- No markdown symbols
"""

    response = model.generate_content(prompt)

    if not response.text:
        raise Exception("Script generation failed")

    return response.text.strip()