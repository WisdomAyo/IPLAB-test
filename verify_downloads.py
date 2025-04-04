#!/usr/bin/env python3
"""
Script to organize and verify the downloaded videos and metadata
"""

import json
import os
import sys
from datetime import datetime

def organize_and_verify():
    """
    Organize and verify the downloaded videos and metadata
    """
    print("Organizing and verifying downloads...")
    
    # Define paths
    videos_dir = os.path.abspath("downloads/videos")
    
    # Check if videos directory exists
    if not os.path.exists(videos_dir):
        print(f"Error: Videos directory {videos_dir} does not exist")
        return False
    
    # Read the videos metadata
    try:
        with open("metadata/videos_metadata.json", "r") as f:
            expected_videos = json.load(f)
        
        print(f"Expected {len(expected_videos)} videos")
        
        # Get list of downloaded video directories
        video_dirs = [d for d in os.listdir(videos_dir) if os.path.isdir(os.path.join(videos_dir, d))]
        print(f"Found {len(video_dirs)} video directories")
        
        # Verify each video
        verification_results = []
        for video in expected_videos:
            video_id = video.get('id')
            video_title = video.get('title')
            
            result = {
                "id": video_id,
                "title": video_title,
                "verified": False,
                "issues": []
            }
            
            # Check if video directory exists
            video_dir = os.path.join(videos_dir, video_id)
            if not os.path.exists(video_dir):
                result["issues"].append(f"Video directory not found")
                verification_results.append(result)
                continue
            
            # Check for video file
            video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
            if not video_files:
                result["issues"].append(f"No video file found")
            else:
                result["video_file"] = video_files[0]
            
            # Check for metadata files
            if not os.path.exists(os.path.join(video_dir, "metadata.json")):
                result["issues"].append(f"metadata.json not found")
            
            if not any(f.endswith('.info.json') for f in os.listdir(video_dir)):
                result["issues"].append(f"info.json not found")
            
            if not any(f.endswith('.description') for f in os.listdir(video_dir)):
                result["issues"].append(f"description file not found")
            
            if not any(f.endswith('.webp') for f in os.listdir(video_dir)):
                result["issues"].append(f"thumbnail not found")
            
            # Mark as verified if no issues
            if not result["issues"]:
                result["verified"] = True
            
            verification_results.append(result)
        
        # Save verification results
        with open("downloads/verification_results.json", "w") as f:
            json.dump(verification_results, f, indent=2)
        
        # Create a human-readable verification report
        create_verification_report(verification_results)
        
        # Check overall verification status
        verified_count = sum(1 for r in verification_results if r["verified"])
        print(f"Verified {verified_count} out of {len(expected_videos)} videos")
        
        if verified_count == len(expected_videos):
            print("All videos successfully verified")
            return True
        else:
            print(f"Warning: {len(expected_videos) - verified_count} videos failed verification")
            return False
    
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

def create_verification_report(verification_results):
    """
    Create a human-readable verification report
    """
    with open("downloads/verification_report.txt", "w") as f:
        f.write(f"Video Download Verification Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        verified_count = sum(1 for r in verification_results if r["verified"])
        f.write(f"Summary: {verified_count} out of {len(verification_results)} videos verified\n\n")
        
        f.write("=== VERIFICATION DETAILS ===\n")
        for result in verification_results:
            f.write(f"\nVideo: {result['title']} (ID: {result['id']})\n")
            f.write(f"Status: {'✓ Verified' if result['verified'] else '✗ Failed'}\n")
            
            if "video_file" in result:
                f.write(f"Video file: {result['video_file']}\n")
            
            if result["issues"]:
                f.write("Issues:\n")
                for issue in result["issues"]:
                    f.write(f"  - {issue}\n")

if __name__ == "__main__":
    print(f"Starting organization and verification at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = organize_and_verify()
    if success:
        print("Successfully organized and verified downloads")
    else:
        print("Verification completed with issues")
        sys.exit(1)
