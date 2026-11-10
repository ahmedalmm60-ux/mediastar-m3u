```python
import os
import urllib.parse
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# =========================================================
# محرك تحويل روابط التورنت/Magnet إلى HTTP Stream للرسيفر
# =========================================================
def get_streamable_url(item, host_base):
    raw_url = item.get("url", "")
    
    # إذا كان الرابط هو Magnet link أو ملف torrent
    if raw_url.startswith("magnet:") or raw_url.endswith(".torrent"):
        encoded_torrent = urllib.parse.quote(raw_url, safe='')
        return f"{host_base}/play_torrent?url={encoded_torrent}"
            
    return raw_url

# =========================================================
# قاعدة بيانات الميديا (قنوات، أفلام، مسلسلات)
# =========================================================
CHANNELS_DATABASE = [
    {
        "title": "قناة تجريبية 1",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "group": "Live Channels",
        "logo": ""
    }
]

MOVIES_DATABASE = [
    {
        "title": "فيلم تجريبي تورنت (Magnet)",
        # ضع رابط الـ Magnet المباشر هنا
        "url": "magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10&dn=Sintel",
        "group": "Movies",
        "logo": ""
    }
]

SERIES_DATABASE = [
    {
        "title": "مسلسل تجريبي - الحلقة الأولى",
        "url": "https://www.w3schools.com/html/html5.mp4",
        "group": "Series",
        "logo": ""
    }
]

# =========================================================
# مسارات تطبيق Flask
# =========================================================
@app.route('/')
def home():
    return "MediaStar Apollo5 M3U & Torrent Generator is Running Successfully!"

@app.route('/playlist.m3u')
def generate_m3u():
    host_base = request.host_url.rstrip('/')
    m3u_content = "#EXTM3U x-tvg-url=\"\"\n\n"
    
    # دمج كافة الأقسام
    all_media = CHANNELS_DATABASE + MOVIES_DATABASE + SERIES_DATABASE
    
    for item in all_media:
        logo = item.get("logo", "")
        group = item.get("group", "General")
        title = item.get("title", "Untitled")
        
        # تجهيز الرابط المناسب للبث
        stream_url = get_streamable_url(item, host_base)
            
        m3u_content += f'#EXTINF:-1 tvg-name="{title}" tvg-logo="{logo}" group-title="{group}",{title}\n'
        m3u_content += f'{stream_url}\n\n'
        
    return Response(m3u_content, mimetype='audio/x-mpegurl')

@app.route('/play_torrent')
def play_torrent():
    torrent_url = request.args.get('url')
    if not torrent_url:
        return "Missing torrent URL", 400
        
    clean_url = urllib.parse.unquote(torrent_url)
    
    # تحويل رابط التورنت إلى رابط بث مباشر HTTP
    target_stream = f"https://api.torrentstream.to/download?torrent={urllib.parse.quote(clean_url)}"
    return redirect(target_stream)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
```
