from app.services import concatenate_media,add_multiple_texts

# Example usage
if __name__ == "__main__":
    media_list = [
    ('images/img4.jpeg', 2, 'zoom_in', 1.2),          # Strong opening – zoom in on gym scene
    ('videos/v4.mp4', 0, 2),                         # Dynamic workout clip
    ('images/img5.jpeg', 2, 'left', 1.15),            # Pan left across equipment/athletes
    ('videos/v5.mp4', 0, 2),                         # High-energy training moment
    ('images/img6.jpeg', 2, 'up', 1.1),               # Pan upward for a powerful finish
]
    
    concatenate_media(media_list, orientation='portrait')
    texts = [
    ("Push\nYour\nLimits", 0, 2),
    ("Train\nHarder", 2, 4),
    ("Feel\nStronger", 4, 6),
    ("Become\nUnstoppable", 6, 8),
    ("Your\nFitness\nJourney\nStarts\nNow", 8, 10)
]

    add_multiple_texts(
        video_path="outputs/output.mp4",
        output_path="outputs/output_with_texts.mp4",
        texts=texts,
        font_size=80,
        color=(255,255,255,255),
        stroke_color="black",
        stroke_width=3,
        margin=(50, 100),
    )