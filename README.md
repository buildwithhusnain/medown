# Media Downloader

A robust black and white GUI media downloader that supports multiple platforms including YouTube, Facebook, Instagram, Twitter/X, and many more.

## Features

- Clean black and white interface
- Support for 1000+ websites via yt-dlp
- Built-in proxy support for restricted access
- Quality selection (best, 720p, 480p, 360p, worst)
- Real-time download progress
- Automatic dependency installation

## Supported Platforms

- YouTube
- Facebook
- Instagram
- Twitter/X
- TikTok
- Vimeo
- Dailymotion
- And 1000+ more sites

## Installation

1. Ensure Python 3.7+ is installed
2. Run the application:
   ```
   python media_downloader.py
   ```
   Or double-click `run.bat` on Windows

3. The app will automatically install yt-dlp if needed

## Usage

1. Paste the media URL in the input field
2. Select download location (defaults to Downloads folder)
3. Choose quality preference
4. Click Download
5. Monitor progress in the status window

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- yt-dlp (auto-installed)

## Notes

- The tool uses free proxies to bypass platform restrictions
- Downloads are saved with original titles
- Supports video and audio formats
- Works with playlists and single videos