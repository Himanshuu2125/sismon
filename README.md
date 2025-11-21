# Media Generation Pipeline

This project takes a single user prompt and turns it into a complete video with images or video clips, narration text, and generated voice. The goal is to have a simple end‑to‑end flow where one prompt produces a structured final output without any manual work in between.

## Overview

The pipeline works in a straightforward way. We begin with one prompt from the user. That prompt is expanded into smaller visual prompts using Gemini text models. The same model is also used to create a narration script that matches those segments. Once the segments and narration are ready, the system generates the actual visuals for every segment using Gemini image and video models. After all visuals are prepared, everything is lined up according to a timeline so each clip plays in the correct order with the correct duration.

MoviePy is used to stitch all the media together, apply simple motion effects to images, and handle any resizing needed for portrait or landscape orientation. MoviePy relies on FFmpeg internally for all encoding and final video export. After the video structure is ready, narration text is added as on‑screen text. The narration itself is converted into audio using Gemini TTS. Librosa and SoundFile are used to clean and adjust the audio so it syncs properly with the video. Finally, the audio and video are merged and exported as an MP4 file.

## Architecture Breakdown

### 1. Prompt Handling

The system receives a single prompt from the user. This is the starting point for everything.

### 2. Prompt Expansion

Gemini text models break the main prompt into smaller visual segments. Each segment describes what should be shown.

### 3. Script Generation

Gemini produces narration lines that match each visual segment. The narration is structured so it can be displayed as text and spoken as audio.

### 4. Media Generation

For each segment, Gemini generates either an image or a video. The output is saved inside the `public/images` or `public/videos` folders.

### 5. Segment Mapping

The generated media and narration lines are matched together. This produces a usable timeline describing which clip plays when.

### 6. Video Assembly

MoviePy is used to combine all clips into a single video. FFmpeg is used internally during the export process. Simple pan or zoom effects can be applied to images.

### 7. Text Overlay

Narration lines are placed on top of the video as subtitles.

### 8. Voice Generation and Processing

The narration is turned into speech using Gemini TTS. Librosa and SoundFile help clean the audio and adjust it to the correct timing.

### 9. Final Export

MoviePy and FFmpeg merge the audio with the video and output the final MP4 file into the `public/outputs` directory.


## Technologies Used

* Gemini text models for prompt breakdown and script generation
* Gemini image and video models for media creation
* Gemini TTS for voice generation
* MoviePy for video handling and composition
* FFmpeg for encoding and exporting videos
* Librosa and SoundFile for processing and cleaning audio

## Running the Pipeline

1. Set your Gemini API key in the environment.
2. Provide a prompt.
3. Run the main pipeline script.
4. The final output will appear in `public/outputs`.

Example:

```
python main.py
```

## Notes

* MoviePy calls FFmpeg automatically during export.
* All intermediate files are saved so the pipeline can be inspected if anything needs debugging.
