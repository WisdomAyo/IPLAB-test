import os
import json
import time
import argparse

import pytube
from pytube import Channel, exceptions


class YouTubeChannelDownloader:
    """
    A simpler, more reliable YouTube channel downloader using pytube's Channel class.
    """
    
    def __init__(self, channel_url, output_dir="downloads", skip_shorts=True, delay=1.5):
        """
        Initialize the YouTube channel downloader.
        
        Args:
            channel_url (str): URL of the YouTube channel
            output_dir (str): Directory to save downloaded videos and metadata
            skip_shorts (bool): Whether to skip YouTube Shorts
            delay (float): Delay between requests to avoid rate limiting
        """
        self.channel_url = channel_url
        self.output_dir = output_dir
        self.skip_shorts = skip_shorts
        self.delay = delay
        self.video_dir = os.path.join(output_dir, "videos")
        self.metadata_dir = os.path.join(output_dir, "metadata")
        
        # Create necessary directories
        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        print(f"Initialized downloader for channel: {channel_url}")
        print(f"Output directory: {os.path.abspath(output_dir)}")
    
    def get_video_list(self):
        """
        Get a list of all videos from the channel using pytube's Channel class.
        
        Returns:
            list: List of video URLs
        """
        print(f"Fetching video list from channel...")
        try:
            # Use pytube's Channel class which handles the dynamic loading
            channel = Channel(self.channel_url)
            
            # Get all video URLs
            video_urls = list(channel.video_urls)
            print(f"Found {len(video_urls)} total videos")
            
            # If we're skipping shorts, filter them out
            if self.skip_shorts:
                # We'll need to check each video after downloading metadata
                filtered_urls = video_urls
                print(f"Will check for shorts during download process")
            else:
                filtered_urls = video_urls
            
            return filtered_urls
            
        except Exception as e:
            print(f"Error fetching video list: {str(e)}")
            return []
    
    def is_short(self, video):
        """
        Check if a video is a YouTube Short.
        
        Args:
            video (pytube.YouTube): A pytube YouTube object
            
        Returns:
            bool: True if the video is a short, False otherwise
        """
        # Method 1: Check duration (Shorts are typically under 60 seconds)
        if video.length < 60:
            # Method 2: Check video dimensions (Shorts are vertical)
            streams = video.streams.filter(progressive=True, file_extension='mp4')
            for stream in streams:
                if hasattr(stream, 'resolution'):
                    # Try to extract height and width
                    try:
                        res = stream.resolution
                        if res:
                            width, height = map(int, res.split('x'))
                            # Vertical video (height > width) is likely a Short
                            if height > width:
                                return True
                    except:
                        pass
        
        # Method 3: Check URL for shorts path
        if '/shorts/' in video.watch_url:
            return True
            
        return False
    
    def download_video(self, video_url):
        """
        Download a single video and its metadata.
        
        Args:
            video_url (str): URL of the video to download
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        try:
            # Create a YouTube object
            yt = pytube.YouTube(video_url)
            
            video_id = yt.video_id
            title = yt.title
            
            print(f"\nProcessing: {title} ({video_id})")
            
            # Check if it's a short and we're skipping shorts
            if self.skip_shorts and self.is_short(yt):
                print(f"Skipping YouTube Short: {title}")
                return False
            
            # Check if already downloaded
            video_filename = f"{video_id}.mp4"
            metadata_filename = f"{video_id}.json"
            video_path = os.path.join(self.video_dir, video_filename)
            metadata_path = os.path.join(self.metadata_dir, metadata_filename)
            
            if os.path.exists(video_path) and os.path.exists(metadata_path):
                print(f"Video and metadata already exist. Skipping.")
                return True
            
            # Prepare metadata
            video_data = {
                'video_id': video_id,
                'title': title,
                'url': video_url,
                'description': yt.description,
                'author': yt.author,
                'publish_date': str(yt.publish_date) if yt.publish_date else 'Unknown',
                'length': yt.length,
                'views': yt.views,
                'keywords': yt.keywords,
                'channel_id': yt.channel_id,
                'channel_url': yt.channel_url,
            }
            
            # Save metadata
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(video_data, f, indent=4, ensure_ascii=False)
            
            # Download the video (highest resolution)
            print(f"Downloading video...")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
            if not stream:
                print(f"No suitable stream found for {video_id}. Trying audio only.")
                stream = yt.streams.filter(only_audio=True).first()
                
            if stream:
                stream.download(output_path=self.video_dir, filename=video_filename)
                print(f"Successfully downloaded: {title}")
                return True
            else:
                print(f"No streams available for {video_id}")
                return False
                
        except exceptions.VideoUnavailable:
            print(f"Video {video_url} is unavailable, skipping.")
            return False
        except Exception as e:
            print(f"Error downloading {video_url}: {str(e)}")
            return False
    
    def download_all_videos(self):
        """
        Download all videos from the channel.
        
        Returns:
            tuple: (success_count, total_count)
        """
        video_urls = self.get_video_list()
        
        if not video_urls:
            print("No videos found to download.")
            return 0, 0
        
        success_count = 0
        total_count = len(video_urls)
        
        for i, video_url in enumerate(video_urls):
            print(f"\nProcessing video {i+1}/{total_count}")
            
            if self.download_video(video_url):
                success_count += 1
            
            # Add delay between downloads to avoid rate limiting
            if i < total_count - 1:
                print(f"Waiting {self.delay} seconds before next download...")
                time.sleep(self.delay)
        
        print(f"\nDownload complete! Successfully downloaded {success_count}/{total_count} videos.")
        print(f"Videos saved to: {os.path.abspath(self.video_dir)}")
        print(f"Metadata saved to: {os.path.abspath(self.metadata_dir)}")
        
        return success_count, total_count


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Download videos from a YouTube channel')
    parser.add_argument('channel_url', help='YouTube channel URL')
    parser.add_argument('--output', '-o', default='downloads', help='Output directory for downloads')
    parser.add_argument('--include-shorts', action='store_true', help='Include YouTube Shorts in download')
    parser.add_argument('--delay', '-d', type=float, default=1.5, help='Delay between video downloads (in seconds)')
    
    args = parser.parse_args()
    
    try:
        downloader = YouTubeChannelDownloader(
            channel_url=args.channel_url,
            output_dir=args.output,
            skip_shorts=not args.include_shorts,
            delay=args.delay
        )
        
        downloader.download_all_videos()
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())