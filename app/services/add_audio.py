from moviepy import AudioFileClip,VideoFileClip,afx
def add_audio_to_video(video_path, audio_path, output_path):
    """
    Adds or replaces the audio track of a video.

    Args:
        video_path: Path to the input video.
        audio_path: Path to the audio file (mp3, wav, etc.).
        output_path: Path to save the output video with audio.
    """

    print("Loading video and audio...")

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Match audio duration to video duration
    if audio.duration > video.duration:
        audio = audio.subclipped(0, video.duration)
    else:
        # Loop audio if too short
        audio = afx.audio_loop(audio, duration=video.duration)

    # Set audio to video
    final = video.with_audio(audio)

    print("Exporting final video...")

    final.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='ultrafast',
        threads=8,
        bitrate='50k',
        audio_bitrate='64k',
        ffmpeg_params=['-crf', '23'],
        logger='bar'
    )

    # Cleanup
    video.close()
    audio.close()
    final.close()

    print(f"Audio added successfully → {output_path}")
