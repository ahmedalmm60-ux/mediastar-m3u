```python
import os
import urllib.parse
import requests
from flask import Flask, Response, request, redirect

app = Flask(__name__)

# =========================================================
# محرك تحويل روابط التورنت/Magnet إلى HTTP Stream للرسيفر
# =========================================================
def get_streamable_url(raw_url, host_base):
    if raw_url.startswith("magnet:") or raw_url.endswith(".torrent"):
        encoded_torrent = urllib.parse.quote(raw_url, safe='')
        return f"{host_base}/play_torrent?url={encoded_torrent}"
    return raw_url

# =========================================================
# جلب الأفلام التلقائي من API التورنت (YTS)
# =========================================================
def fetch_auto_movies():
    movies = []
    try:
        # جلب قائمة من أحدث/أعلى تقييم للأفلام التورنت
        url = "https://yts.mx/api/v2/list_movies.json?limit=20&sort_by=download_count"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            movie_list = data.get('data', {}).get('movies', [])
            for item in movie_list:
                title = item.get('title_english', item.get('title'))
                year = item.get('year')
                rating = item.get('rating')
                logo = item.get('medium_cover_image', '')
                torrents = item.get('torrents', [])
                
                if torrents:
                    # اختيار أعلى جودة مجهزة (720p أو 1080p)
                    best_torrent = torrents[0]
                    hash_val = best_torrent.get('hash')
                    magnet = f"magnet:?xt=urn:btih:{hash_val}&dn={urllib.parse.quote(title)}"
                    
                    movies.append({
                        "title": f"{title} ({year}) ★ {rating}",
                        "url": magnet,
                        "group": "🎬 Auto Movies (Torrent)",
                        "logo": logo
                    })
    except Exception as e:
        print(f"Error fetching auto movies: {e}")
    return movies

# =========================================================
# جلب المسلسلات التلقائي من API التورنت (EZTV)
# =========================================================
def fetch_auto_series():
    series = []
    try:
        url = "https://eztv.re/api/get-torrents?limit=20"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            torrents = data.get('torrents', [])
            for item in torrents:
                title = item.get('title')
                magnet = item.get('magnet_url')
                logo = item.get('large_screenshot', '')
                
                if magnet and title:
                    series.append({
                        "title": title,
                        "url": magnet,
                        "group": "📺 Auto Series (Torrent)",
                        "logo": logo
                    })
    except Exception as e:
        print(f"Error fetching auto series: {e}")
    return series

# =========================================================
# قاعدة بيانات إضافية يدوية (قنوات مباشرة محددة)
# =========================================================
CUSTOM_CHANNELS = [
    {
        "title": "قناة تجريبية 1",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "group": "Live Channels",
        "logo": ""
    }
]

# =========================================================
# مسارات تطبيق Flask
# =========================================================
@app.route('/')
def home():
    return "MediaStar M3U Auto Torrent Engine is Running!"

@app.route('/playlist.m3u')
def generate_m3u():
    host_base = request.host_url.rstrip('/')
    m3u_content = "#EXTM3U x-tvg-url=\"\"\n\n"
    
    # 1. جلب التورنت التلقائي لأحدث الأفلام والمسلسلات
    auto_movies = fetch_auto_movies()
    auto_series = fetch_auto_series()
    
    # 2. دمج المحتوى التلقائي مع المحتوى اليدوي
    all_media = CUSTOM_CHANNELS + auto_movies + auto_series
    
    for item in all_media:
        logo = item.get("logo", "")
        group = item.get("group", "General")
        title = item.get("title", "Untitled")
        raw_url = item.get("url", "")
        
        # تحويل رابط التورنت تلقائياً
        stream_url = get_streamable_url(raw_url, host_base)
            
        m3u_content += f'#EXTINF:-1 tvg-name="{title}" tvg-logo="{logo}" group-title="{group}",{title}\n'
        m3u_content += f'{stream_url}\n\n'
        
    return Response(m3u_content, mimetype='audio/x-mpegurl')

@app.route('/play_torrent')
def play_torrent():
    torrent_url = request.args.get('url')
    if not torrent_url:
        return "Missing torrent URL", 400
        
    clean_url = urllib.parse.unquote(torrent_url)
    
    # تحويل المغناطيس للبث المباشر عبر البروكسي
    target_stream = f"https://api.torrentstream.to/download?torrent={urllib.parse.quote(clean_url)}"
    return redirect(target_stream)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
```
