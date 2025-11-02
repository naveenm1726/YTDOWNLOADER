from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        unique_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_DIR, f"{unique_id}.mp4")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'cookiefile': None  # No cookies for public videos
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
