from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Allows Netlify to talk to this server

@app.route('/', methods=['GET'])
def home():
    return "TikTok API is Running!"

@app.route('/get-video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    # 1. User-Agent Spoofing to look like a real browser
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': user_agent,
        'referer': 'https://www.tiktok.com/',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail'),
                'download_url': info.get('url'),
                'author': info.get('uploader'),
                'success': True
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
