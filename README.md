# 🎬 Video Clipper

A web-based video clipping tool that allows users to create clips from supported online videos by specifying a start and end timestamp.

The project uses **FastAPI, yt-dlp, FFmpeg, HTML, CSS, and JavaScript**.

## ✨ Features

* 📎 Paste a video URL
* ⏱️ Select a specific start and end timestamp
* 🎞️ Create clips without downloading the entire video first
* 🎥 Preview the generated clip in the browser
* ⬇️ Download the finished clip
* 🖥️ Quality selection
* 🧹 Clear generated clips from the clips folder
* 🔊 Automatically handle separate video and audio streams
* 🌐 Support for many sites compatible with yt-dlp

## 🌐 Supported Websites

The application uses **yt-dlp** for media extraction, so it can work with many supported video platforms.

Examples include:

* YouTube
* Vimeo
* TikTok
* Twitch
* Bilibili
* Instagram
* Facebook
* Reddit
* Twitter/X
* And many others

Support depends on the individual website and its current implementation. Websites can change their video delivery systems, which may cause previously working URLs to stop working.

For the current list of yt-dlp extractors, see the official supported-sites list.

## 🛠️ Technologies

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI

### Video Processing

* yt-dlp
* FFmpeg

### Planned AI Features

* Automatic transcription
* Find interesting moments
* Search videos by topic
* Automatic clip suggestions
* Automatic captions
* AI-generated clip titles

## 📁 Project Structure

```text
video-clipper/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── clips/
    └── generated clips
```

## ⚙️ Requirements

* Python 3.11+
* FFmpeg
* yt-dlp
* FastAPI
* Uvicorn

## 🚀 Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd video-clipper
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

Download and install a Windows FFmpeg build and make sure the application knows where `ffmpeg.exe` is located.

### 4. Start the server

```bash
uvicorn app:app --reload
```

### 5. Open the application

Open:

```text
http://127.0.0.1:8000
```

## 🎯 How to Use

1. Paste a supported video URL.
2. Enter the start timestamp.
3. Enter the end timestamp.
4. Select the desired quality.
5. Click **Create Clip**.
6. Wait for processing to finish.
7. Preview the generated clip.
8. Download the clip if you're satisfied with it.

### Timestamp Format

Timestamps use:

```text
HH:MM:SS
```

For example:

```text
00:01:30
```

means:

```text
1 minute and 30 seconds
```

## 🤖 Future AI Features

The long-term goal is to turn this from a basic timestamp clipper into an **AI-assisted clipping tool**.

Possible features include:

```text
Long Video
     ↓
Transcription
     ↓
AI Analysis
     ↓
Interesting Moments
     ↓
Suggested Clips
     ↓
Preview
     ↓
Export
```

Users could eventually enter prompts such as:

> Find the most interesting moments where the speaker talks about artificial intelligence.

The AI could return timestamp ranges and automatically create the clips.

## ⚠️ Disclaimer

This project is intended for educational and personal use.

Users are responsible for ensuring that they have the necessary rights or permission to download, process, and redistribute videos.

The application does not bypass DRM or other access controls.

## 📌 Project Status

### Current

* [x] Web interface
* [x] URL input
* [x] Timestamp selection
* [x] Video clipping
* [x] Quality selection
* [x] Browser preview
* [x] Clip download
* [x] Clear clips
* [x] FFmpeg integration
* [x] yt-dlp integration

### Planned

* [ ] Video metadata preview
* [ ] Interactive timeline
* [ ] Multiple clips
* [ ] Clip queue
* [ ] Automatic subtitles
* [ ] AI transcription
* [ ] AI clip detection
* [ ] AI-generated titles
* [ ] Vertical 9:16 export
* [ ] Automatic Shorts/Reels formatting
* [ ] Cloud deployment

## 📄 License

Standard MIT License
