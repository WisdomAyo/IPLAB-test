# IPLABS YouTube Video Downloader

This application downloads videos and their associated metadata from YouTube channel: https://www.youtube.com/@vk-streaming3526, excluding shorts.

## Features

- Extracts video metadata from YouTube channels
- Filters out shorts to download only regular videos
- Downloads videos in the best available quality
- Saves associated metadata including descriptions and thumbnails
- Verifies downloaded content for completeness
- Generates comprehensive reports

## Requirements

- Python 3.6+
- yt-dlp
- requests
- beautifulsoup4
- python-dateutil

## Installation

```bash
# Clone or extract the application
# Install dependencies
pip install yt-dlp requests beautifulsoup4 python-dateutil
```

## Usage

```bash
# Run the main script with default channel
python main.py

# Or specify a different channel URL
python main.py https://www.youtube.com/channel/YOUR_CHANNEL_ID
```

## Directory Structure

```
IPLABS test/
├── main.py               # Main application script
├── channel_info.py       # Channel access script
├── extract_metadata.py   # Metadata extraction script
├── download_videos.py    # Video downloading script
├── verify_downloads.py   # Download verification script
├── create_summary.py     # Report generation script
├── metadata/             # Raw and processed metadata
├── downloads/            # Downloaded videos and verification
└── reports/              # Generated reports
```

## Output

The application creates the following outputs:

1. **metadata/** - Contains raw and processed channel metadata
2. **downloads/videos/** - Contains downloaded videos and their metadata
3. **reports/** - Contains summary reports and verification details

For more details, please take a look at the summary report in the reports directory. #Wisdev
