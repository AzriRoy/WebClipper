from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os
import uuid
import re

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

FFMPEG_PATH = r"C:\Users\azriel cerezo\OneDrive\Documents\FFmpeg\ffmpeg-9.0.1-essentials_build\ffmpeg-9.0.1-essentials_build\bin"

CLIPS_FOLDER = "clips"

os.makedirs(CLIPS_FOLDER, exist_ok=True)


class ClipRequest(BaseModel):
    url: str
    start: str
    end: str
    quality: str = "best"


def timestamp_to_seconds(timestamp):
    parts = timestamp.split(":")

    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds

    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds

    raise ValueError("Invalid timestamp")


def validate_timestamp(timestamp):
    pattern = r"^\d{2}:\d{2}:\d{2}$"

    if not re.match(pattern, timestamp):
        return False

    try:
        hours, minutes, seconds = map(int, timestamp.split(":"))

        if minutes > 59 or seconds > 59:
            return False

        if hours > 99:
            return False

        return True

    except ValueError:
        return False


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.post("/clip")
def create_clip(request: ClipRequest):

    if not request.url.strip():
        return {
            "success": False,
            "error": "Please enter a video URL."
        }

    if not validate_timestamp(request.start):
        return {
            "success": False,
            "error": "Invalid start timestamp."
        }

    if not validate_timestamp(request.end):
        return {
            "success": False,
            "error": "Invalid end timestamp."
        }

    start_seconds = timestamp_to_seconds(request.start)
    end_seconds = timestamp_to_seconds(request.end)

    if start_seconds >= end_seconds:
        return {
            "success": False,
            "error": "End time must be after start time."
        }

    clip_id = str(uuid.uuid4())

    output_file = os.path.join(
        CLIPS_FOLDER,
        f"{clip_id}.mp4"
    )

    if request.quality == "best":
        format_selector = "bv*+ba/b"

    elif request.quality == "1080":
        format_selector = "bv*[height<=1080]+ba/b"

    elif request.quality == "720":
        format_selector = "bv*[height<=720]+ba/b"

    elif request.quality == "480":
        format_selector = "bv*[height<=480]+ba/b"

    else:
        format_selector = "bv*+ba/b"

    try:

        command = [
            "yt-dlp",

            "--ffmpeg-location",
            FFMPEG_PATH,

            "--download-sections",
            f"*{request.start}-{request.end}",

            "--force-keyframes-at-cuts",

            "-f",
            format_selector,

            "--merge-output-format",
            "mp4",

            "-o",
            output_file,

            request.url
        ]

        subprocess.run(
            command,
            check=True
        )

        if not os.path.exists(output_file):
            return {
                "success": False,
                "error": "The clip was not created."
            }

        return {
            "success": True,
            "file": f"/video/{clip_id}",
            "download": f"/download/{clip_id}",
            "filename": (
                f"clip_{request.start.replace(':', '-')}"
                f"_to_{request.end.replace(':', '-')}.mp4"
            )
        }

    except subprocess.CalledProcessError as error:

        return {
            "success": False,
            "error": f"Video processing failed. Error code: {error.returncode}"
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


@app.get("/video/{clip_id}")
def stream_clip(clip_id: str):

    file_path = os.path.join(
        CLIPS_FOLDER,
        f"{clip_id}.mp4"
    )

    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": "Clip not found."
        }

    return FileResponse(
        file_path,
        media_type="video/mp4"
    )


@app.get("/download/{clip_id}")
def download_clip(clip_id: str):

    file_path = os.path.join(
        CLIPS_FOLDER,
        f"{clip_id}.mp4"
    )

    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": "Clip not found."
        }

    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename="clip.mp4"
    )


@app.delete("/clear-clips")
def clear_clips():

    deleted = 0

    for filename in os.listdir(CLIPS_FOLDER):

        file_path = os.path.join(
            CLIPS_FOLDER,
            filename
        )

        if os.path.isfile(file_path):

            try:
                os.remove(file_path)
                deleted += 1

            except Exception:
                pass

    return {
        "success": True,
        "deleted": deleted
    }