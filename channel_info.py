"""
Script to access YouTube channel and extract video information
"""

import json
import os
import subprocess
import sys
from datetime import datetime

CHANNEL_URL = "https://www.youtube.com/@vk-streaming3526"

def get_channel_info():
    """
    Get basic information about the YouTube channel
    """
    print(f"Accessing channel: {CHANNEL_URL}")
    
    # Use yt-dlp to get channel info
    cmd = [
        "yt-dlp", 
        "--dump-json",
        "--flat-playlist",
        CHANNEL_URL
    ]
    
    try:
        # Create output directory for metadata
        os.makedirs("metadata", exist_ok=True)
        
        # Run the command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Save raw channel info
        with open("metadata/channel_raw_info.json", "w") as f:
            f.write(result.stdout)
            
        print(f"Channel information saved to metadata/channel_raw_info.json")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error accessing channel: {e}")
        print(f"Error output: {e.stderr}")
        return False

if __name__ == "__main__":
    print(f"Starting channel access at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = get_channel_info()
    if success:
        print("Successfully accessed channel information")
    else:
        print("Failed to access channel information")
        sys.exit(1)
