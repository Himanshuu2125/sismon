from google import genai
from google.genai import types
import wave
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly
from fractions import Fraction
import os

def save_wav(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM data as WAV file"""
    print("inside save_wav")
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def build_transcript(segments):
    """Convert timestamped segments to plain transcript string"""
    print("inside build_transcript")
    return " ".join(seg["script"] for seg in segments)

def adjust_audio_to_duration(input_file, output_file, target_duration):
    """Adjust audio duration using high-quality polyphase resampling"""
    print(f"Adjusting audio duration to {target_duration}s")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Load audio
    y, sr = librosa.load(input_file, sr=None)
    current_duration = len(y) / sr
    
    print(f"Current duration: {current_duration:.2f}s")
    
    # If duration is close enough, skip adjustment
    if abs(current_duration - target_duration) < 0.5:
        print(f"Duration already close to target ({current_duration:.2f}s ≈ {target_duration:.2f}s)")
        sf.write(output_file, y, sr)
        return current_duration
    
    # Calculate speed factor
    speed_factor = current_duration / target_duration
    print(f"Adjusting: {current_duration:.2f}s → {target_duration:.2f}s (speed factor: {speed_factor:.2f}x)")
    
    # Use polyphase resampling for better quality
    # Convert speed_factor to rational numbers
    frac = Fraction(speed_factor).limit_denominator(1000)
    print(f"Using rational approximation: {frac.numerator}/{frac.denominator}")
    
    # Resample with high quality
    y_fast = resample_poly(y, frac.denominator, frac.numerator)
    
    # Adjust to exact target duration by trimming or padding
    target_samples = int(target_duration * sr)
    current_samples = len(y_fast)
    
    if current_samples > target_samples:
        # Trim excess samples
        y_fast = y_fast[:target_samples]
        print(f"Trimmed {current_samples - target_samples} samples")
    elif current_samples < target_samples:
        # Pad with silence
        padding = target_samples - current_samples
        y_fast = np.pad(y_fast, (0, padding), mode='constant')
        print(f"Padded {padding} samples")
    
    # Save adjusted audio
    sf.write(output_file, y_fast, sr)
    
    final_duration = len(y_fast) / sr
    print(f"✓ Audio adjusted successfully to {final_duration:.2f}s")
    
    return final_duration

def generate_voice_from_segments(segments, out_file="output.wav", adjust_timing=True):
    """Generate voice using Google TTS and optionally adjust timing"""
    print("inside generate_voice_from_segments")
    
    # Build transcript
    transcript = "Read the following script with an energetic, motivating tone: "
    transcript += build_transcript(segments)

    print("Calling Google TTS API...")
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
    
    # Create temp file for initial audio
    out_dir = os.path.dirname(out_file) or "."
    out_basename = os.path.basename(out_file)
    temp_file = os.path.join(out_dir, "temp_" + out_basename)
    
    save_wav(temp_file, pcm_data)
    print(f"Initial audio saved to {temp_file}")
    
    # Adjust timing if requested
    if adjust_timing and segments:
        target_duration = segments[-1]["end_time"]
        print(f"\nTarget duration from segments: {target_duration}s")
        adjust_audio_to_duration(temp_file, out_file, target_duration)
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"Removed temporary file: {temp_file}")
    else:
        # Just move temp file to output file
        import shutil
        shutil.move(temp_file, out_file)
        print(f"Moved {temp_file} to {out_file}")
    
    print(f"✓ Final audio saved to {out_file}")