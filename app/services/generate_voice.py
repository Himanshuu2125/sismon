from google import genai
from google.genai import types
import wave
import os

# Save PCM data to WAV
def save_wav(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# Generate voice using Google TTS
def generate_voice_from_segments(segments, out_file="output.wav"):
    # Initialize client
    # NOTE: Replace 'YOUR_API_KEY' with your actual key if not using env variables
    api_key = os.environ.get("GEMINI_API_KEY") 
    client = genai.Client(api_key=api_key)

    # 1. Construct a prompt that explicitly explains the timing
    prompt_text = "Generate a voiceover for a fitness advertisement. You must strictly adhere to the following timing constraints and pacing:\n\n"
    
    for seg in segments:
        duration = seg['end_time'] - seg['start_time']
        prompt_text += f"- [{seg['start_time']}s to {seg['end_time']}s] (Duration: {duration}s): {seg['script']}\n"

    prompt_text += "\nInstructions:\n"
    prompt_text += "1. Strictly follow the timestamps provided for each line.\n"
    prompt_text += "2. Adjust your speaking rate (speed up or slow down) to fit the text exactly within the specific duration.\n"
    prompt_text += "3. Where the script says '(Pause)', ensure there is silence for that duration.\n"
    prompt_text += "4. Maintain an energetic, motivating tone throughout."

    print("Sending prompt to Gemini...")
    
    # 2. Generate Content
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=prompt_text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Enceladus'
                    )
                )
            )
        )
    )

    # 3. Save File
    if response.candidates and response.candidates[0].content.parts[0].inline_data:
        pcm_data = response.candidates[0].content.parts[0].inline_data.data
        save_wav(out_file, pcm_data)
        print(f"Audio saved successfully to {out_file}")
    else:
        print("Error: No audio data returned.")

# ----------------------
# Example usage:
# ----------------------

segments = [
    {'start_time': 0.0, 'end_time': 4.0, 'script': 'Every journey is unique. Every goal is personal.'},
    {'start_time': 4.0, 'end_time': 6.0, 'script': 'With a plan built just for you.'},
    {'start_time': 6.0, 'end_time': 10.0, 'script': 'Follow guided workouts that fit your life, wherever you are.'},
    {'start_time': 10.0, 'end_time': 14.0, 'script': 'Push your limits. Smash your goals.'},
    {'start_time': 14.0, 'end_time': 16.0, 'script': 'And celebrate every single victory.'},
    {'start_time': 16.0, 'end_time': 20.0, 'script': 'Find your strength, and find your community.'},
    {'start_time': 20.0, 'end_time': 24.0, 'script': 'Fuel your body right, and get the support that keeps you going.'},
    {'start_time': 24.0, 'end_time': 28.0, 'script': 'This is more than fitness. This is your transformation.'},
    {'start_time': 28.0, 'end_time': 30.0, 'script': '(Pause)'},
    {'start_time': 30.0, 'end_time': 32.0, 'script': 'Elevate Your Fitness. Download now.'}
]

# Ensure directory exists
os.makedirs("audios", exist_ok=True)

generate_voice_from_segments(segments, "audios/fitness_ad.wav")