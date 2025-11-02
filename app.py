from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import re

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def clean_filename(title):
    """Clean invalid filename characters."""
    return re.sub(r'[\\/*?:"<>|]', "", title)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    try:
        url = request.form["url"].strip()
        format_choice = request.form["format"]

        # ✅ Normalize Shorts or youtu.be URLs
        if "shorts/" in url:
            match = re.search(r"shorts/([^?&/]+)", url)
            if match:
                url = f"https://www.youtube.com/watch?v={match.group(1)}"
        elif "youtu.be/" in url:
            match = re.search(r"youtu\.be/([^?&/]+)", url)
            if match:
                url = f"https://www.youtube.com/watch?v={match.group(1)}"

        # Remove tracking parameters like ?si=
        url = re.sub(r"(\?|\&)(si|pp|ab_channel)=[^&]+", "", url)

        # Choose yt_dlp download options
        if format_choice == "audio":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
        else:
            ydl_opts = {
                "format": "mp4/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            }

        # Download video/audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Rename extension for MP3
        if format_choice == "audio":
            filename = os.path.splitext(filename)[0] + ".mp3"
            return send_file(filename, as_attachment=True, mimetype="audio/mpeg")
        else:
            return send_file(filename, as_attachment=True, mimetype="video/mp4")

    except Exception as e:
        return f"❌ Error: {str(e)}", 400


if __name__ == "__main__":
    app.run(debug=True)
