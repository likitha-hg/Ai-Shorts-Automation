def build_instruction(data: dict, research: str):

    title = data.get("title", "")
    hook = data.get("hook", "")
    keywords = data.get("keywords", [])
    target_audience = data.get("target_audience", "")

    prompt = f"""
You are an expert YouTube Shorts strategist.

Your job is to plan a viral short-form video strategy.

Video Information:

Title:
{title}

Hook:
{hook}

Keywords:
{", ".join(keywords)}

Target Audience:
{target_audience}

Research Context:
{research}

Build a content strategy with:

1. Best opening style
2. Audience pain points
3. Key talking points
4. Curiosity gaps to maintain retention
5. Emotional triggers
6. Best CTA style

Rules:
- Focus on virality
- Focus on retention
- Keep the flow logical
- Keep it optimized for short-form content
- Make it highly engaging

Return only the strategy.
"""

    return prompt.strip()