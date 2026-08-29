import math
import os
import subprocess

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
        # Get video duration using ffprobe
        cmd_duration = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ]
        
        total_duration = float(subprocess.check_output(cmd_duration).strip())
        total_parts = math.ceil(total_duration / chunk_duration)

        print(f"\nProcessing '{full_filename}' ({total_duration:.2f} seconds)...")
        print(f"Total Parts to create: {total_parts}\n")

        for i in range(total_parts):
            start_time = i * chunk_duration
            output_filename = f"{i + 1}_part_{filename}.mp4"
            output_path = os.path.join(output_dir, output_filename)

            print(f"Exporting Part {i + 1}/{total_parts}: {output_filename}...")

            # Re-encode to standard MP4 (H.264 + AAC) to ensure 100% video playback
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-ss", str(start_time), "-i", video_path,
                "-t", str(chunk_duration), "-c:v", "libx264", "-c:a", "aac",
                "-strict", "experimental", output_path
            ]
            
            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"\nSuccess! All {total_parts} part(s) created perfectly in MP4 format.")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Tip: Make sure FFmpeg is installed and added to PATH.")

if __name__ == "__main__":
    split_video()