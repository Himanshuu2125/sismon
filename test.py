from app.services import generate_prompts_from_prompt
from app.services import generate_script_from_prompt

seg=generate_prompts_from_prompt("Make a 30-second promo video for a fitness app in a modern, energetic style")
print(seg)
print(generate_script_from_prompt(seg,"Make a 30-second promo video for a fitness app in a modern, energetic style"))