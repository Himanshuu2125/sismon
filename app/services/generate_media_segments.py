import random

def process_media_segments(visual_segments, script_segments):
    """
    Combines visual segments and script segments into the final lists for video generation.
    Handles 'clubbed' video files (e.g., 25.mp4 containing segments 2 and 5).
    """
    media_list = []
    texts = []

    # --- PRE-PROCESSING: Map Video Segments ---
    # 1. Extract all segment numbers that are videos, in order.
    video_indices = []
    for seg in visual_segments:
        # Handle object vs dict access safely
        s_type = seg['type'] if isinstance(seg, dict) else seg.type
        s_num = seg['segment_number'] if isinstance(seg, dict) else seg.segment_number
        
        if s_type == "video":
            video_indices.append(s_num)

    # 2. Create a lookup map for video file details
    # Key: segment_number, Value: {'file': path, 'start': float, 'end': float}
    video_map = {}
    
    # Iterate through indices in pairs (step=2)
    for i in range(0, len(video_indices), 2):
        first_seg = video_indices[i]
        
        # Check if there is a pair (handle odd number of videos gracefully)
        if i + 1 < len(video_indices):
            second_seg = video_indices[i+1]
            # Filename combines both IDs (e.g., "25.mp4")
            filename = f"public/media/{first_seg}{second_seg}.mp4"
            
            # First segment gets first half (0s to 4s)
            video_map[first_seg] = {'file': filename, 'start': 0, 'end': 4}
            
            # Second segment gets second half (4s to 8s)
            video_map[second_seg] = {'file': filename, 'start': 4, 'end': 8}
        else:
            # Fallback for an orphan video (last one if odd count)
            # Assuming it's saved as a single number or still combined format? 
            # Here saving as single number to be safe, taking first 4 seconds.
            filename = f"public/media/{first_seg}.mp4"
            video_map[first_seg] = {'file': filename, 'start': 0, 'end': 4}

    # --- 1. Build media_list (Visuals) ---
    for segment in visual_segments:
        s_type = segment['type'] if isinstance(segment, dict) else segment.type
        s_num = segment['segment_number'] if isinstance(segment, dict) else segment.segment_number
        s_duration = segment['duration_seconds'] if isinstance(segment, dict) else segment.duration_seconds

        if s_type == "image":
            # Format: (Filename, Duration, Effect, Zoom_Amount)
            filename = f"public/media/{s_num}.png"
            zoom_amount = round(random.uniform(1.1, 1.5), 2)
            media_list.append((filename, s_duration, 'zoom_in', zoom_amount))
            
        elif s_type == "video":
            # Retrieve pre-calculated file info
            if s_num in video_map:
                v_info = video_map[s_num]
                
                # Format: (Filename, Start_Time, End_Time)
                # This now matches your request: (file, 0, 4) or (file, 4, 8)
                media_list.append((v_info['file'], v_info['start'], v_info['end']))

    # --- 2. Build texts (Script/Overlay) ---
    for item in script_segments:
        script_text = item['script'] if isinstance(item, dict) else item.script
        start_time = item['start_time'] if isinstance(item, dict) else item.start_time
        end_time = item['end_time'] if isinstance(item, dict) else item.end_time
        
        # Format: (Text Content, Start_Time, End_Time)
        texts.append((script_text, start_time, end_time))

    return media_list, texts