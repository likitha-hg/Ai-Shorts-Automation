import os
import edge_tts


async def generate_voice(
    script: str,
    output_path: str = "output/voice.mp3"
):

    if not script or not script.strip():
        raise ValueError("Script cannot be empty")

    os.makedirs("output", exist_ok=True)

    communicate = edge_tts.Communicate(
        text=script,
        voice="en-US-AriaNeural",   # natural female voice
        rate="+5%"                  # slightly faster for Shorts
    )

    await communicate.save(output_path)

    return output_path