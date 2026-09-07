import os
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips
)


def create_video(
    video_paths: list,
    audio_path: str = "output/voice.mp3",
    output_path: str = "output/final_video.mp4"
):

    if not video_paths:
        raise ValueError("No video clips provided")

    if not os.path.exists(audio_path):
        raise FileNotFoundError("Voice file not found")

    os.makedirs("output", exist_ok=True)

    audio = AudioFileClip(audio_path)
    total_audio_duration = audio.duration

    scene_duration = total_audio_duration / len(video_paths)

    clips = []

    for video_path in video_paths:

        if not os.path.exists(video_path):
            continue

        clip = VideoFileClip(video_path)

        # Trim or extend clip to fit scene duration
        if clip.duration > scene_duration:
            clip = clip.subclipped(0, scene_duration)
        else:
            clip = clip.with_duration(scene_duration)

        # Resize to Shorts format (1080x1920)
        clip = clip.resized((1080, 1920))

        clips.append(clip)

    if not clips:
        raise Exception("No valid clips found")

    final_video = concatenate_videoclips(
        clips,
        method="compose"
    )

    # Add voiceover
    final_video = final_video.with_audio(audio)

    final_video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    # Cleanup
    audio.close()
    final_video.close()

    for clip in clips:
        clip.close()

    return output_path