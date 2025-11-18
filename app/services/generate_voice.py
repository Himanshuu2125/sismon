from google import genai
from google.genai import types
import wave


def save_wav(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


# Build SSML where timestamps force strict pacing
def build_timestamp_strict_ssml(segments):
    ssml = "<speak>\n"

    for seg in segments:
        duration = seg["end_time"] - seg["start_time"]
        text = ""
        text += "\nInstructions:\n"
        text += "1. Strictly follow the timestamps provided for each line.\n"
        text += "2. Adjust your speaking rate (speed up or slow down) to fit the text exactly within the specific duration.\n"
        text += "3. Maintain an energetic, motivating tone throughout."
        text += seg["script"]

        ssml += f"  <p>{text}</p>\n"

    ssml += "</speak>"
    return ssml


def generate_voice_from_segments(segments, out_file="timed_output.wav"):
    ssml = build_timestamp_strict_ssml(segments)

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=ssml,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Kore'
                    )
                )
            )
        )
    )

    pcm_data = response.candidates[0].content.parts[0].inline_data.data

    save_wav(out_file, pcm_data)
    print(f"Strict-timed audio saved to {out_file}")


from google import genai
from google.genai import types
import wave

# Save PCM data to WAV
def save_wav(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


# Convert timestamped segments → plain transcript string
def build_transcript(segments):
    return " ".join(seg["script"] for seg in segments)


# Generate voice using Google TTS
def generate_voice_from_segments(segments, out_file="output.wav"):
    # Build transcript
    transcript = ""
    transcript += "\nInstructions:\n"
    transcript += "1. Strictly follow the timestamps provided for each line.\n"
    transcript += "2. Adjust your speaking rate (speed up or slow down) to fit the text exactly within the specific duration.\n"
    transcript += "3. Maintain an energetic, motivating tone throughout."
    transcript += build_transcript(segments)

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=transcript,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Kore'
                    )
                )
            )
        )
    )

    pcm_data = response.candidates[0].content.parts[0].inline_data.data

    save_wav(out_file, pcm_data)
    print(f"Audio saved to {out_file}")



