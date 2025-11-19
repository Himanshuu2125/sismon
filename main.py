from moviepy import VideoFileClip, ImageClip, concatenate_videoclips, ColorClip, CompositeVideoClip, vfx, afx
from moviepy import TextClip,AudioFileClip

def resize_and_center(clip, target_width, target_height):
    """
    Resizes clip to cover the entire target dimensions while maintaining aspect ratio,
    then centers it (cropping excess if necessary).
    """
    clip_width, clip_height = clip.size
    clip_aspect = clip_width / clip_height
    target_aspect = target_width / target_height
    
    if clip_aspect > target_aspect:
        new_height = target_height
        new_width = int(target_height * clip_aspect)
    else:
        new_width = target_width
        new_height = int(target_width / clip_aspect)
    
    resized_clip = clip.resized((new_width, new_height))
    
    x_center = (target_width - new_width) // 2
    y_center = (target_height - new_height) // 2
    
    bg = ColorClip(size=(target_width, target_height), 
                   color=(0, 0, 0), 
                   duration=resized_clip.duration)
    
    resized_clip = resized_clip.with_position((x_center, y_center))
    final = CompositeVideoClip([bg, resized_clip], size=(target_width, target_height))
    
    return final

def apply_pan_effect(clip, target_width, target_height, direction='zoom', intensity=1.15):
    """
    Applies a slow pan/zoom effect to an image clip while ensuring frame is always covered.
    
    Args:
        clip: The image clip to animate
        target_width: Target width for the output
        target_height: Target height for the output
        direction: 'left', 'right', 'up', 'down', 'zoom_in', 'zoom_out', 'zoom' (alias for zoom_in)
        intensity: How much to scale/move (1.15 = 15% larger/movement)
    """
    clip_width, clip_height = clip.size
    duration = clip.duration
    clip_aspect = clip_width / clip_height
    target_aspect = target_width / target_height
    
    # First, scale image to COVER the frame (matching the larger dimension needed)
    if clip_aspect > target_aspect:
        # Clip is wider, match HEIGHT
        base_height = target_height
        base_width = int(target_height * clip_aspect)
    else:
        # Clip is taller, match WIDTH
        base_width = target_width
        base_height = int(target_width / clip_aspect)
    
    # Scale up further by intensity to allow for movement while staying covered
    scale_factor = intensity
    scaled_width = int(base_width * scale_factor)
    scaled_height = int(base_height * scale_factor)
    
    # Apply zoom effects
    if direction in ['zoom_in', 'zoom']:
        def zoom_func(t):
            progress = t / duration
            # Start at base size (covering frame), end at scaled size
            start_w, start_h = base_width, base_height
            end_w, end_h = scaled_width, scaled_height
            current_w = int(start_w + (end_w - start_w) * progress)
            current_h = int(start_h + (end_h - start_h) * progress)
            return (current_w, current_h)
        
        def position_func(t):
            current_size = zoom_func(t)
            x = -(current_size[0] - target_width) // 2
            y = -(current_size[1] - target_height) // 2
            return (x, y)
        
        animated_clip = clip.with_effects([vfx.Resize(zoom_func)]).with_position(position_func)
        
    elif direction == 'zoom_out':
        def zoom_func(t):
            progress = t / duration
            # Start at scaled size, end at base size (covering frame)
            start_w, start_h = scaled_width, scaled_height
            end_w, end_h = base_width, base_height
            current_w = int(start_w - (start_w - end_w) * progress)
            current_h = int(start_h - (start_h - end_h) * progress)
            return (current_w, current_h)
        
        def position_func(t):
            current_size = zoom_func(t)
            x = -(current_size[0] - target_width) // 2
            y = -(current_size[1] - target_height) // 2
            return (x, y)
        
        animated_clip = clip.with_effects([vfx.Resize(zoom_func)]).with_position(position_func)
    
    else:
        # Pan effects - use scaled size
        scaled_clip = clip.resized((scaled_width, scaled_height))
        
        def position_func(t):
            progress = t / duration  # 0 to 1
            
            if direction == 'left':
                # Pan from right to left
                max_offset = scaled_width - target_width
                x = -int(max_offset * progress)
                y = -(scaled_height - target_height) // 2
                
            elif direction == 'right':
                # Pan from left to right
                max_offset = scaled_width - target_width
                x = -int(max_offset * (1 - progress))
                y = -(scaled_height - target_height) // 2
                
            elif direction == 'up':
                # Pan from bottom to top
                max_offset = scaled_height - target_height
                x = -(scaled_width - target_width) // 2
                y = -int(max_offset * progress)
                
            elif direction == 'down':
                # Pan from top to bottom
                max_offset = scaled_height - target_height
                x = -(scaled_width - target_width) // 2
                y = -int(max_offset * (1 - progress))
            
            else:
                # No movement (center)
                x = -(scaled_width - target_width) // 2
                y = -(scaled_height - target_height) // 2
            
            return (x, y)
        
        animated_clip = scaled_clip.with_position(position_func)
    
    # Create background and composite
    bg = ColorClip(size=(target_width, target_height), 
                   color=(0, 0, 0), 
                   duration=duration)
    
    final = CompositeVideoClip([bg, animated_clip], size=(target_width, target_height))
    
    return final

def concatenate_media(media_list, output_filename="public/outputs/output.mp4", orientation='portrait'):
    """
    Concatenates images and video clips based on the provided list.
    
    Args:
        media_list: List of tuples.
            - For images: ('image.jpg', duration_in_seconds, direction, intensity)
              direction can be: 'left', 'right', 'up', 'down', 'zoom_in', 'zoom_out', 'zoom', or None
              intensity is optional (default 1.15)
            - For videos: ('video.mp4', start_time, end_time)
        output_filename: Name for the output video file.
        orientation: 'portrait' or 'landscape'
    
    Example:
        media_list = [
            ('i1.jpg', 3, 'zoom_in', 1.2),  # Image with zoom effect
            ('v1.mp4', 2, 4),                # Video clip
            ('i2.jpg', 4, 'left'),           # Image panning left
            ('i3.jpg', 3, 'up', 1.3),        # Image panning up with custom intensity
        ]
    """
    clips = []
    
    # Set target dimensions based on orientation
    if orientation == 'portrait':
        target_width, target_height = 1080, 1920
    else:
        target_width, target_height = 1920, 1080
    
    for item in media_list:
        filename = item[0]
        
        # Determine if it's an image or video based on number of parameters
        if len(item) >= 2 and len(item) <= 4 and not isinstance(item[1], (int, float)) or (len(item) == 2):
            # This is ambiguous, default to image
            pass
        
        # Check if second parameter looks like a duration (for images) or start time (for videos)
        is_video = len(item) == 3 and isinstance(item[1], (int, float)) and isinstance(item[2], (int, float)) and item[2] > item[1]
        
        if is_video:  # Video
            start, end = item[1], item[2]
            video_clip = VideoFileClip(filename).subclipped(start, end)
            clip = resize_and_center(video_clip, target_width, target_height)
        
        else:  # Image with optional pan effect
            duration = item[1]
            direction = item[2] if len(item) > 2 else None
            intensity = item[3] if len(item) > 3 else 1.15
            
            img_clip = ImageClip(filename).with_duration(duration)
            
            if direction:
                clip = apply_pan_effect(img_clip, target_width, target_height, direction, intensity)
            else:
                clip = resize_and_center(img_clip, target_width, target_height)
        
        clips.append(clip)
    
    # Concatenate clips
    final_clip = concatenate_videoclips(clips, method='chain')
    
    # Write to file
    final_clip.write_videofile(
        output_filename,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='ultrafast',
        threads=8,
        bitrate='50k',
        audio_bitrate='2k',
        ffmpeg_params=['-crf', '23'],
        logger='bar'
    )
    
    # Close clips to free memory
    final_clip.close()
    for clip in clips:
        clip.close()
    
    print(f"Video saved as {output_filename}")

def add_multiple_texts(
    video_path,
    output_path,
    texts,
    font='E:/hackathon/sismon/public/fonts/font1.ttf',
    font_size=70,
    color='white',
    bg_color=None,
    stroke_color=None,
    stroke_width=0,
    method='caption',
    text_align='center',
    horizontal_align='center',
    vertical_align='center',
    size=(800, None),
    margin=(10, 10),
    interline=4,
    transparent=True,
):
    video = VideoFileClip(video_path)
    text_clips = []

    def zoom_in(t):
        zoom_duration = 0.3
        start_scale = 1.2
        end_scale = 1.0
        if t >= zoom_duration:
            return end_scale
        return start_scale - (start_scale - end_scale) * (t / zoom_duration)

    for text_content, start_time, end_time in texts:
        duration = end_time - start_time

        txt = TextClip(
            text=text_content,
            font=font,
            font_size=font_size,
            color=color,
            bg_color=bg_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            method=method,
            text_align=text_align,
            horizontal_align=horizontal_align,
            vertical_align=vertical_align,
            size=size,
            margin=margin,
            interline=interline,
            transparent=transparent
        )

        txt = (
            txt.with_position((horizontal_align, vertical_align))
               .with_start(start_time)
               .with_duration(duration)
               .with_effects([
                   vfx.CrossFadeIn(0.1),
                   vfx.CrossFadeOut(0.1),
                   vfx.Resize(zoom_in),
               ])
        )

        text_clips.append(txt)

    final = CompositeVideoClip([video] + text_clips)

    final.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='ultrafast',
        threads=8,
        bitrate='50k',
        audio_bitrate='2k',
        ffmpeg_params=['-crf', '23'],
        logger='bar'
    )

    video.close()
    for c in text_clips:
        c.close()
    final.close()

def add_audio(video_path, audio_path, output_path):
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
        audio = audio.subclip(0, video.duration)
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


# # Example usage
# if __name__ == "__main__":
#     media_list = [
#     ('images/img4.jpeg', 2, 'zoom_in', 1.2),          # Strong opening – zoom in on gym scene
#     ('videos/v4.mp4', 0, 2),                         # Dynamic workout clip
#     ('images/img5.jpeg', 2, 'left', 1.15),            # Pan left across equipment/athletes
#     ('videos/v5.mp4', 0, 2),                         # High-energy training moment
#     ('images/img6.jpeg', 2, 'up', 1.1),               # Pan upward for a powerful finish
# ]
    
#     concatenate_media(media_list, orientation='portrait')
    
#     texts = [
#     ("Push\nYour\nLimits", 0, 2),
#     ("Train\nHarder", 2, 4),
#     ("Feel\nStronger", 4, 6),
#     ("Become\nUnstoppable", 6, 8),
#     ("Your\nFitness\nJourney\nStarts\nNow", 8, 10)
# ]


#     add_multiple_texts(
#         video_path="outputs/output.mp4",
#         output_path="outputs/output_with_texts.mp4",
#         texts=texts,
#         font_size=80,
#         color=(255,255,255,255),
#         stroke_color="black",
#         stroke_width=3,
#         margin=(50, 100),
    
#     )

from app.services import generate_prompts_from_prompt
from app.services import generate_script_from_prompt
from app.services import generate_voice_from_segments
from app.services import generate_media_sequence
from app.services import process_media_segments
from app.services import add_audio_to_video
seg=[{'segment_number': 1, 'type': 'image', 'duration_seconds': 2, 'prompt': "A stylish young person in their mid-20s sits alone at a small table in a modern, dimly lit coffee shop at night. They are looking down at their smartphone with a bored and uninspired expression. The coffee shop has minimalist decor with warm ambient light and a soft neon sign glowing in the background, out of focus. The shot is a medium close-up, focusing on the person's feeling of solitude and digital detachment. The color palette is moody with warm tones and deep shadows, creating a cinematic and relatable atmosphere."}, {'segment_number': 2, 'type': 'video', 'duration_seconds': 4, 'prompt': 'An extreme close-up shot of a smartphone held by a hand. The screen displays a vibrant, colorful, and modern dating app interface. For 4 seconds, a thumb performs a rapid series of swipes. The profiles are diverse, attractive, and dynamic, showing people engaged in fun activities. Each swipe is accompanied by a fluid, satisfying animation and a subtle haptic effect. The background is a stylishly blurred city scene at night with colorful bokeh lights. The motion is fast-paced and energetic, conveying excitement and possibility. The lighting on the hand and phone is sleek and professional.'}, {'segment_number': 3, 'type': 'image', 'duration_seconds': 3, 'prompt': "A beautifully composed close-up shot of a smartphone lying on a dark wooden table at a rooftop bar. The screen is brightly lit, displaying the dating app's logo and a clear, compelling call-to-action: 'Start Your Story'. In the background, the hands of the happy couple from the date are gently intertwined, slightly out of focus. The blurred city lights from the bar's view create a magical bokeh effect. The image is warm, aspirational, and focused, serving as the final brand message. High-end commercial photography style."}, {'segment_number': 4, 'type': 'video', 'duration_seconds': 4, 'prompt': 'A dynamic, fast-cut montage of a happy, stylish couple on an exciting date at night in a vibrant city. The 4-second sequence includes quick shots of them laughing while playing a brightly lit arcade game, clinking glasses at a trendy rooftop bar with a stunning skyline view, and sharing a dessert under warm string lights. Their chemistry is evident and their expressions are full of joy and connection. The camera work is handheld and energetic, with lens flares and a vibrant, saturated color grade to emphasize the fun and modern feel.'}]

script=generate_script_from_prompt(seg,"Make a 10-second promo video for a dating app in a modern, energetic style")
# generate_media_sequence(seg,'public/media')
seg2=process_media_segments(seg,script)

print(seg2)
concatenate_media(seg2[0], orientation='portrait')    


add_multiple_texts(
        video_path="public/outputs/output.mp4",
        output_path="public/outputs/output_with_texts.mp4",
        texts=seg2[1],
        font_size=80,
        color=(255,255,255,255),
        stroke_color="black",
        stroke_width=3,
        margin=(50, 100),
    
    )