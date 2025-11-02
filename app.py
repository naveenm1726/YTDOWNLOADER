from flask import Flask, render_template, request, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = "secret123"  # needed for flash messages

# Create 'downloads' folder if not exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')

    if not url:
        flash("Please enter a valid YouTube URL.", "error")
        return redirect(url_for('index'))

    try:
        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join("downloads", '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        flash("✅ Download started successfully! Check 'downloads' folder.", "success")

    except Exception as e:
        flash(f"❌ Error: {str(e)}", "error")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
