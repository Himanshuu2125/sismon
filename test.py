from app.services import generate_prompts_from_prompt
from app.services import generate_script_from_prompt
from app.services import generate_voice_from_segments
from app.services import generate_media_sequence
from app.services import process_media_segments

from app.services import add_audio_to_video
from app.services import concatenate_media
from app.services import add_multiple_texts
from app.services import add_audio_to_video
from app.services import generate_media_sequence


seg=generate_prompts_from_prompt("Make a 20-second promo video for a dating app in a modern, energetic style")
# seg=[{'segment_number': 1, 'type': 'image', 'duration_seconds': 2, 'prompt': "A stylish young person in their mid-20s sits alone at a small table in a modern, dimly lit coffee shop at night. They are looking down at their smartphone with a bored and uninspired expression. The coffee shop has minimalist decor with warm ambient light and a soft neon sign glowing in the background, out of focus. The shot is a medium close-up, focusing on the person's feeling of solitude and digital detachment. The color palette is moody with warm tones and deep shadows, creating a cinematic and relatable atmosphere."}, {'segment_number': 2, 'type': 'video', 'duration_seconds': 4, 'prompt': 'An extreme close-up shot of a smartphone held by a hand. The screen displays a vibrant, colorful, and modern dating app interface. For 4 seconds, a thumb performs a rapid series of swipes. The profiles are diverse, attractive, and dynamic, showing people engaged in fun activities. Each swipe is accompanied by a fluid, satisfying animation and a subtle haptic effect. The background is a stylishly blurred city scene at night with colorful bokeh lights. The motion is fast-paced and energetic, conveying excitement and possibility. The lighting on the hand and phone is sleek and professional.'}, {'segment_number': 3, 'type': 'video', 'duration_seconds': 4, 'prompt': 'A dynamic, fast-cut montage of a happy, stylish couple on an exciting date at night in a vibrant city. The 4-second sequence includes quick shots of them laughing while playing a brightly lit arcade game, clinking glasses at a trendy rooftop bar with a stunning skyline view, and sharing a dessert under warm string lights. Their chemistry is evident and their expressions are full of joy and connection. The camera work is handheld and energetic, with lens flares and a vibrant, saturated color grade to emphasize the fun and modern feel.'}, {'segment_number': 4, 'type': 'image', 'duration_seconds': 3, 'prompt': "A beautifully composed close-up shot of a smartphone lying on a dark wooden table at a rooftop bar. The screen is brightly lit, displaying the dating app's logo and a clear, compelling call-to-action: 'Start Your Story'. In the background, the hands of the happy couple from the date are gently intertwined, slightly out of focus. The blurred city lights from the bar's view create a magical bokeh effect. The image is warm, aspirational, and focused, serving as the final brand message. High-end commercial photography style."}]
# seg=[{'segment_number': 1,'type': 'image', 'duration_seconds': 3, 'prompt': "A"}, {'segment_number': 3,'type': 'image', 'duration_seconds': 3, 'prompt': "D"}, {'segment_number': 4,'type': 'video', 'duration_seconds': 5, 'prompt': "B"}]
script=generate_script_from_prompt(seg,"Make a 20-second promo video for a dating app in a modern, energetic style")
# script=[{'start_time': 0.0, 'end_time': 2.0, 'script': 'Tired of the same old scene?'}, {'start_time': 2.0, 'end_time': 6.0, 'script': "It's time to find a real connection. Endless possibilities are just a swipe away."}, {'start_time': 6.0, 'end_time': 10.0, 'script': "From that first spark, to a night you'll never forget."}, {'start_time': 10.0, 'end_time': 13.0, 'script': 'This is dating, reimagined. Start your story today.'}]
# print(process_media_segments(seg,script))
# generate_voice_from_segments(script,"public/audios/a.wav")
generate_media_sequence(seg,"public/media")

# segement = process_media_segments(seg,script)
# concatenate_media(segement[0], orientation='portrait')
# add_multiple_texts(
#     video_path="public/outputs/output.mp4",
#     output_path="public/outputs/output_with_texts.mp4",
#     texts=segement[1],
#     font_size=80,
#     color=(255,255,255,255),
#     stroke_color="black",
#     stroke_width=3,
#     margin=(50, 100),
#     )
# add_audio_to_video("public/outputs/output_with_texts.mp4","public/audios/a.wav","public/outputs/output_with_audio.mp4")
