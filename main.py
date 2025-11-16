from moviepy import VideoFileClip, ImageClip, concatenate_videoclips, ColorClip, CompositeVideoClip, vfx
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

def resize_and_center(clip, target_width, target_height):
    """
    Resizes clip to cover the entire target dimensions while maintaining aspect ratio,
    then centers it (cropping excess if necessary).
    """
    clip_width, clip_height = clip.size
    clip_aspect = clip_width / clip_height
    target_aspect = target_width / target_height
    
    # Determine if we should match width or height
    # CHANGED: Now we match the dimension that will COVER the frame
    if clip_aspect > target_aspect:
        # Clip is wider (landscape-ish), match HEIGHT to cover frame
        new_height = target_height
        new_width = int(target_height * clip_aspect)
    else:
        # Clip is taller (portrait-ish), match WIDTH to cover frame
        new_width = target_width
        new_height = int(target_width / clip_aspect)
    
    # Resize the clip
    resized_clip = clip.resized((new_width, new_height))
    
    # Center position
    x_center = (target_width - new_width) // 2
    y_center = (target_height - new_height) // 2
    
    # Create background
    bg = ColorClip(size=(target_width, target_height), 
                   color=(0, 0, 0), 
                   duration=resized_clip.duration)
    
    # Position the resized clip on the background
    resized_clip = resized_clip.with_position((x_center, y_center))
    
    # Composite the clip on the background
    final = CompositeVideoClip([bg, resized_clip], size=(target_width, target_height))
    
    return final
def concatenate_media(media_list, output_filename="output.mp4", orientation='portrait'):
    """
    Concatenates images and video clips based on the provided list.
    
    Args:
        media_list: List of tuples.
            - For images: ('image.jpg', duration_in_seconds)
            - For videos: ('video.mp4', start_time, end_time)
        output_filename: Name for the output video file.
        orientation: 'portrait' or 'landscape'
    
    Example:
        media_list = [('i1.jpg', 3), ('v1.mp4', 2, 4), ('v2.mp4', 1, 5), ('i2.jpg', 4)]
    """
    clips = []
    
    # Set target dimensions based on orientation
    if orientation == 'portrait':
        target_width, target_height = 1080, 1920
    else:
        target_width, target_height = 1920, 1080
    
    for item in media_list:
        filename = item[0]
        
        if len(item) == 2:  # Image
            duration = item[1]
            img_clip = ImageClip(filename).with_duration(duration)
            clip = resize_and_center(img_clip, target_width, target_height)
        
        elif len(item) == 3:  # Video
            start, end = item[1], item[2]
            video_clip = VideoFileClip(filename).subclipped(start, end)
            clip = resize_and_center(video_clip, target_width, target_height)
        
        else:
            raise ValueError(f"Invalid item format: {item}")
        
        clips.append(clip)
    
    # Concatenate clips - method='chain' is faster but 'compose' needed for different sizes
    final_clip = concatenate_videoclips(clips, method='chain')
    
    # Write to file with optimized settings for SPEED
    final_clip.write_videofile(
        output_filename,
        codec='libx264',
        audio_codec='aac',
        fps=30,  # Fixed FPS for consistency
        preset='ultrafast',  # FASTEST encoding (larger file size)
        threads=8,  # Use more threads (adjust based on your CPU)
        bitrate='50k',  # Control quality vs size
        audio_bitrate='2k',
        ffmpeg_params=['-crf', '23'],  # Constant Rate Factor for quality
        logger='bar'  # Progress bar instead of verbose logging
    )
    
    # Close clips to free memory
    final_clip.close()
    for clip in clips:
        clip.close()
    
    print(f"Video saved as {output_filename}")

def add_multiple_texts(
    video_path,
    output_path,
    texts,   # LIST OF TEXT ITEMS → [("Hello", 0, 2), ("Everyone", 2, 4), ...]
    font='E:/C++/Contest/font1.otf',
    font_size=70,
    color='white',
    bg_color=None,
    stroke_color=None,
    stroke_width=0,
    method='label',
    text_align='center',
    horizontal_align='center',
    vertical_align='center',
    size=(None, None),
    margin=(10, 10),
    interline=4,
    transparent=True,
):
    video = VideoFileClip(video_path)

    text_clips = []

    # ---- Zoom function (same for all clips) ----
    def zoom_in(t):
        zoom_duration = 0.3
        start_scale = 1.2
        end_scale = 1.0
        if t >= zoom_duration:
            return end_scale
        return start_scale - (start_scale - end_scale) * (t / zoom_duration)

    # ---- Create every text clip ----
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

    # ---- Composite final video ----
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
# Example usage
if __name__ == "__main__":
    media_list = [
        ('img1.jpg', 3),
        ('v1.mp4', 0, 2),
        ('v2.mp4', 0, 2),
        ('img2.jpg', 4)
    ]
    concatenate_media(media_list, orientation='portrait')
    
    texts = [
    ("Hello", 0, 2),
    ("Everyone", 2, 4),
    ("Welcome", 4, 6),
    ("Back", 6, 8)
    ]

    add_multiple_texts(
        video_path="output.mp4",
        output_path="output_with_texts.mp4",
        texts=texts,
        font_size=80,
        color=(255,255,255,255),
        stroke_color="black",
        stroke_width=3,
        margin=(50, 100)
    )

    