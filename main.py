
"""
Main script for  YouTube IPLABS Video Downloader application
"""

import argparse
import os
import sys
import subprocess
from datetime import datetime

def main():
    """
    Main function to run the YouTube Video Downloader application
    """
    parser = argparse.ArgumentParser(description='Download videos from a YouTube channel, excluding shorts.')
    parser.add_argument('channel_url', nargs='?', default="https://www.youtube.com/@vk-streaming3526",
                        help='YouTube channel URL (default: https://www.youtube.com/@vk-streaming3526)')
    args = parser.parse_args()
    
    channel_url = args.channel_url
    
    print(f"YouTube Video Downloader")
    print(f"=======================")
    print(f"Starting download process for channel: {channel_url}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Access the YouTube channel
    print("Step 1: Accessing YouTube channel...")
    result = run_script("channel_info.py")
    if not result:
        print("Failed to access YouTube channel. Exiting.")
        sys.exit(1)
    print()
    
    # Step 2: Extract video metadata
    print("Step 2: Extracting video metadata...")
    result = run_script("extract_metadata.py")
    if not result:
        print("Failed to extract video metadata. Exiting.")
        sys.exit(1)
    print()
    
    # Step 3: Download videos and metadata
    print("Step 3: Downloading videos and metadata...")
    result = run_script("download_videos.py")
    if not result:
        print("Failed to download videos. Exiting.")
        sys.exit(1)
    print()
    
    # Step 4: Verify downloads
    print("Step 4: Verifying downloads...")
    result = run_script("verify_downloads.py")
    if not result:
        print("Warning: Some videos failed verification.")
    print()
    
    # Step 5: Create summary report
    print("Step 5: Creating summary report...")
    result = run_script("create_summary.py")
    if not result:
        print("Failed to create summary report.")
    print()
    
    print(f"Download process completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results are available in the following directories:")
    print(f"  - Downloaded videos: {os.path.abspath('downloads/videos')}")
    print(f"  - Reports: {os.path.abspath('reports')}")
    print()
    print("Thank you for using IPLABS YouTube Video Downloader!")

def run_script(script_name):
    """
    Run a Python script and return True if successful, False otherwise
    """
    try:
        subprocess.run(["python", script_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    main()
