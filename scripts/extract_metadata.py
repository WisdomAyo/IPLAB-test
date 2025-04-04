#!/usr/bin/env python3
"""
Script to extract and process video metadata from the YouTube channel
"""

import json
import os
import sys
from datetime import datetime

def extract_metadata():
    """
    Extract and process video metadata from the raw channel information
    """
    print("Extracting video metadata...")
    
    # Create output directory for processed metadata
    os.makedirs("metadata/videos", exist_ok=True)
    os.makedirs("metadata/shorts", exist_ok=True)
    
    # Read the raw channel info
    try:
        with open("metadata/channel_raw_info.json", "r") as f:
            lines = f.readlines()
        
        # Process each line (each line is a JSON object)
        videos = []
        shorts = []
        
        for line in lines:
            if not line.strip():
                continue
                
            data = json.loads(line)
            
            # Determine if it's a video or a short
            if "shorts" in data.get("webpage_url", "").lower():
                shorts.append(data)
            else:
                videos.append(data)
        
        # Save processed metadata
        with open("metadata/videos_metadata.json", "w") as f:
            json.dump(videos, f, indent=2)
            
        with open("metadata/shorts_metadata.json", "w") as f:
            json.dump(shorts, f, indent=2)
            
        # Create a summary file with key information
        create_summary(videos, shorts)
        
        print(f"Found {len(videos)} videos and {len(shorts)} shorts")
        print(f"Metadata extracted and saved to metadata/videos_metadata.json and metadata/shorts_metadata.json")
        
        return True
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return False

def create_summary(videos, shorts):
    """
    Create a summary file with key information about videos and shorts
    """
    with open("metadata/summary.txt", "w") as f:
        f.write(f"Channel: VK-STREAMING (@vk-streaming3526)\n")
        f.write(f"Extraction date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"Total videos: {len(videos)}\n")
        f.write(f"Total shorts: {len(shorts)}\n\n")
        
        f.write("=== VIDEOS ===\n")
        for i, video in enumerate(videos, 1):
            f.write(f"{i}. {video.get('title', 'Unknown Title')} (ID: {video.get('id', 'Unknown ID')})\n")
            f.write(f"   Duration: {video.get('duration_string', 'Unknown')}\n")
            f.write(f"   URL: {video.get('webpage_url', 'Unknown URL')}\n")
            f.write(f"   Views: {video.get('view_count', 'Unknown')}\n")
            f.write(f"   Description: {video.get('description', 'No description')}\n\n")
        
        f.write("=== SHORTS ===\n")
        for i, short in enumerate(shorts, 1):
            f.write(f"{i}. {short.get('title', 'Unknown Title')} (ID: {short.get('id', 'Unknown ID')})\n")
            f.write(f"   URL: {short.get('webpage_url', 'Unknown URL')}\n")
            f.write(f"   Views: {short.get('view_count', 'Unknown')}\n\n")

if __name__ == "__main__":
    print(f"Starting metadata extraction at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = extract_metadata()
    if success:
        print("Successfully extracted video metadata")
    else:
        print("Failed to extract video metadata")
        sys.exit(1)
