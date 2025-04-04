
"""
Script to download videos and their metadata from the YouTube channel
"""

import json
import os
import subprocess
import sys
from datetime import datetime

def download_videos():
    """
    Download videos and their metadata using yt-dlp
    """
    print("Starting video downloads...")
    
    # Create output directory for videos
    videos_dir = os.path.abspath("downloads/videos")
    os.makedirs(videos_dir, exist_ok=True)
    
    # Read the videos metadata
    try:
        with open("metadata/videos_metadata.json", "r") as f:
            videos = json.load(f)
        
        print(f"Found {len(videos)} videos to download")
        
        # Download each video
        for i, video in enumerate(videos, 1):
            video_id = video.get('id')
            video_title = video.get('title')
            video_url = video.get('webpage_url')
            
            if not video_id or not video_url:
                print(f"Skipping video {i} due to missing ID or URL")
                continue
            
            print(f"Downloading video {i}/{len(videos)}: {video_title} (ID: {video_id})")
            
            # Create video-specific directory
            video_dir = os.path.join(videos_dir, video_id)
            os.makedirs(video_dir, exist_ok=True)
            
            # Save video metadata
            with open(os.path.join(video_dir, "metadata.json"), "w") as f:
                json.dump(video, f, indent=2)
            
            # Download video using yt-dlp
            cmd = [
                "yt-dlp",
                "-f", "best",  # Best quality
                "-o", os.path.join(video_dir, "%(title)s.%(ext)s"),
                "--write-description",
                "--write-info-json",
                "--write-thumbnail",
                video_url
            ]
            
            try:
                subprocess.run(cmd, check=True)
                print(f"Successfully downloaded video: {video_title}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading video {video_title}: {e}")
        
        print(f"Video download process completed")
        return True
    except Exception as e:
        print(f"Error during video download process: {e}")
        return False

if __name__ == "__main__":
    print(f"Starting video download process at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = download_videos()
    if success:
        print("Successfully downloaded videos and metadata")
    else:
        print("Failed to download videos and metadata")
        sys.exit(1)
