# import requests
# # from flask import request
# # from google import genai
# # from google.genai import types
# # from PIL import Image
# # from io import BytesIO
# import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # api_key = os.getenv("GEMINI_API_KEY")

# # client = genai.Client(api_key=api_key)

# # def generate_video_from_prompt(prompt, segment_number, duration_seconds, output_dir="output"):
# #     """
# #     Generate a video from a prompt
    
# #     Args:
# #         prompt: Text prompt for video generation
# #         segment_number: Segment number for naming
# #         duration_seconds: Duration of the video (should be 4 seconds)
# #         output_dir: Directory to save the video
        
# #     Returns:
# #         Path to the saved video file
# #     """
# #     print(f"\n{'='*80}")
# #     print(f"Generating VIDEO for Segment {segment_number} ({duration_seconds}s)")
# #     print(f"{'='*80}")
# #     print(f"Prompt: {prompt[:100]}...")
    
# #     try:
# #         # Note: Replace with actual video generation API when available
# #         # This is a placeholder for the video generation logic
# #         response = client.models.generate_videos(
# #             model='veo-2.0',  # Replace with actual video model name
# #             prompt=prompt,
# #             config=types.GenerateVideosConfig(
# #                 duration_seconds=duration_seconds,
# #                 number_of_videos=1,
# #             )
# #         )
        
# #         # # Create output directory if it doesn't exist
# #         # os.makedirs(output_dir, exist_ok=True)
        
# #         # Save the generated video
# #         filename = f"{segment_number}.mp4"
# #         filepath = os.path.join(output_dir, filename)
        
# #         # Save video (adjust based on actual API response structure)
# #         with open(filepath, 'wb') as f:
# #             f.write(response.video_data)  # Adjust based on API
        
# #         print(f"✓ Video saved: {filepath}")
# #         return filepath
        
# #     except Exception as e:
# #         print(f"✗ Error generating video: {str(e)}")
# #         print("Note: Video generation API may not be available yet.")
# #         return None
# def download_file(url, filename):
#     """Download file from URL and save locally"""
#     response = requests.get(url, stream=True)
#     response.raise_for_status()
    
#     # os.makedirs('downloads', exist_ok=True)
#     filepath = os.path.join('public/media', filename)

    
#     with open(filepath, 'wb') as f:
#         for chunk in response.iter_content(chunk_size=8192):
#             f.write(chunk)

# def generate_video_from_prompt(prompt, segment_number, duration_seconds, output_dir="public/media"):
#     """
#     Generate a video from a prompt
    
#     Args:
#         prompt: Text prompt for video generation
#         segment_number: Segment number for naming
#         duration_seconds: Duration of the video (should be 4 seconds)
#         output_dir: Directory to save the video
        
#     Returns:
#         Path to the saved video file
#     """
#     print(f"\n{'='*80}")
#     print(f"Generating VIDEO for Segment {segment_number} ({duration_seconds}s)")
#     print(f"{'='*80}")
#     print(f"Prompt: {prompt[:100]}...")
    
#     try:
#         url = "https://api.kie.ai/api/v1/runway/generate"

#         payload = {
#             "prompt": prompt,
#             "model": "runway-duration-5-generate",
#             "callBackUrl": "https://api.example.com/callback",
#             "duration":duration_seconds,
#             "quality": "720p"
#         }
#         headers = {
#             "Authorization": "Bearer 00ac5c400d3f43c6628cbb7fb15fcec6",
#             "Content-Type": "application/json"
#         }

#         response = requests.post(url, json=payload, headers=headers)


#         # print(response.json())
#         data=response.json()
#         callback_data = data.get('data', {})
#         video_url = callback_data.get('video_url')
#         if video_url:
#             try:
#                 video_filename = f"{segment_number}.mp4"
#                 download_file(video_url, video_filename)
#                 print(f"Video downloaded as {video_filename}")
#             except Exception as e:
#                 print(f"Video download failed: {e}")
#         # Note: Replace with actual video generation API when available
#         # This is a placeholder for the video generation logic
#         # response = client.models.generate_videos(
#         #     model='veo-2.0',  # Replace with actual video model name
#         #     prompt=prompt,
#         #     config=types.GenerateVideosConfig(
#         #         duration_seconds=duration_seconds,
#         #         number_of_videos=1,
#         #     )
#         # )
        
#         # # Create output directory if it doesn't exist
#         # os.makedirs(output_dir, exist_ok=True)
        
#         # Save the generated video
#         # filename = f"{segment_number}.mp4"
#         # filepath = os.path.join(output_dir, filename)
        
#         # # Save video (adjust based on actual API response structure)
#         # with open(filepath, 'wb') as f:
#         #     f.write(response.video_data)  # Adjust based on API
        
#         # print(f"✓ Video saved: {filepath}")
#         # return filepath
        
#     except Exception as e:
#         print(f"✗ Error generating video: {str(e)}")
#         print("Note: Video generation API may not be available yet.")
#         return None

import requests
import os
import time  # For polling delays

def download_file(url, filename, output_dir="public/media"):
    """Download file from URL and save locally"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    print(f"Downloading video from {url} to {filepath}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✓ Video saved: {filepath}")
    return filepath

def generate_video_from_prompt(prompt, segment_number, duration_seconds=5, aspect_ratio="9:16", output_dir="public/media"):
    """
    Generate a video from a prompt using Kie.ai Runway API (async with polling).
    
    Args:
        prompt: Text prompt for video generation
        segment_number: Segment number for naming
        duration_seconds: Duration of the video (5 or 10 seconds only)
        aspect_ratio: Video aspect ratio (e.g., "16:9", "9:16"). Default: "16:9"
        output_dir: Directory to save the video
        
    Returns:
        Path to the saved video file, or None on failure
    """
    print(f"\n{'='*80}")
    print(f"Generating VIDEO for Segment {segment_number} ({duration_seconds}s)")
    print(f"{'='*80}")
    print(f"Prompt: {prompt[:100]}...")
    
    try:
        url = "https://api.kie.ai/api/v1/runway/generate"

        payload = {
            "prompt": prompt,
            "model": "runway-duration-5-generate",  # Adjust if needed for 10s
            "callBackUrl": "https://api.example.com/callback",
            "duration": duration_seconds,
            "quality": "720p",
            "aspectRatio": aspect_ratio,
            "waterMark": ""  # Set to "" for no watermark, or e.g., "your-brand"
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('KIE_API_KEY')}",
            "Content-Type": "application/json"
        }

        # Start the generation job
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        api_data = response.json()
        
        if api_data.get("code") != 200:
            print(f"✗ API error starting job: {api_data.get('msg', 'Unknown error')}")
            return None
        
        task_id = api_data.get("data", {}).get("taskId")
        if not task_id:
            print("✗ No taskId returned from API.")
            return None
        
        print(f"✓ Job started with taskId: {task_id}")
        print("Polling for completion...")

        # Poll for status
        status_url = f"https://api.kie.ai/api/v1/runway/record-detail?taskId={task_id}"
        max_polls = 60  # ~5-10 min max wait; adjust as needed
        poll_interval = 10  # seconds between polls
        
        for attempt in range(max_polls):
            status_response = requests.get(status_url, headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            if status_data.get("code") != 200:
                print(f"✗ Status check failed: {status_data.get('msg', 'Unknown error')}")
                return None
            
            state = status_data.get("data", {}).get("state")
            print(f"Poll {attempt + 1}/{max_polls}: State = {state}")
            
            if state == "success":
                video_info = status_data.get("data", {}).get("videoInfo", {})
                video_url = video_info.get("videoUrl")
                if video_url:
                    video_filename = f"{segment_number}.mp4"
                    return download_file(video_url, video_filename, output_dir)
                else:
                    print("✗ No videoUrl in successful response.")
                    return None
            elif state in ["failed", "error"]:
                error_msg = status_data.get("data", {}).get("errorMsg", "Unknown error")
                print(f"✗ Job failed: {error_msg}")
                return None
            
            # Still processing; wait and retry
            if attempt < max_polls - 1:
                time.sleep(poll_interval)
        
        print("✗ Timeout: Job took too long to complete.")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Network/API error: {str(e)}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return None