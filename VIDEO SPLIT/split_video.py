import math
import os
from moviepy import VideoFileClip

def split_video():
    video_path = input("Enter video file path: ").strip().strip('"\'')

    if not os.path.exists(video_path):
        print(f"Error: File '{video_path}' not found!")
        return

    output_dir, full_filename = os.path.split(video_path)
    filename, _ = os.path.splitext(full_filename)

    # 4.40 minutes = 4 * 60 + 40 = 280 seconds
    chunk_duration = 4 * 60 + 40 

    try:
        # Load clip to get total duration
        with VideoFileClip(video_path) as video:
            total_duration = video.duration
            total_parts = math.ceil(total_duration / chunk_duration)
            print(f"\nProcessing '{full_filename}' ({total_duration:.2f} seconds)...")
            print(f"Total Parts to create: {total_parts}\n")

        # Process each part individually to prevent file locks
        for i in range(total_parts):
            start_time = i * chunk_duration
            end_time = min((i + 1) * chunk_duration, total_duration)
            output_filename = f"{filename}_part_{i + 1}.mp4"
            output_path = os.path.join(output_dir, output_filename)

            print(f"Exporting Part {i + 1}/{total_parts}: {output_filename}...")
            
            with VideoFileClip(video_path) as current_video:
                if hasattr(current_video, "subclipped"):
                    subclip = current_video.subclipped(start_time, end_time)
                else:
                    subclip = current_video.subclip(start_time, end_time)
                
                subclip.write_videofile(
                    output_path, 
                    codec="libx264", 
                    audio_codec="aac",
                    preset="ultrafast",
                    logger=None  # Cleans up console output
                )
                subclip.close()

        print(f"\nSuccess! Created all {total_parts} part(s) in MP4 format.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    split_video()