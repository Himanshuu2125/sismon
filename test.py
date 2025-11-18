from app.services import generate_prompts_from_prompt
from app.services import generate_script_from_prompt
from app.services import generate_voice_from_segments

seg=generate_prompts_from_prompt("Make a 10-second promo video for a dating app in a modern, energetic style")
script=generate_script_from_prompt(seg,"Make a 10-second promo video for a dating app in a modern, energetic style")
generate_voice_from_segments(script,"public/audios/a.wav")