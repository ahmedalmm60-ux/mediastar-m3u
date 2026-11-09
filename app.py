from flask import Flask, jsonify, Response, request

app = Flask(__name__)

# بيانات الدخول الخاصة بك
SERVER_CONFIG = {
    "username": "Mahmood",
    "password": "Mahmood102001",
    "server_url": "mediastar-m3u.onrender.com"
}

# 1. القنوات المباشرة
CHANNELS_DATABASE = [
    {
        "num": 1,
        "stream_id": 1,
        "name": "قناة تجريبية 1",
        "stream_type": "live",
        "stream_icon": "",
        "epg_channel_id": "",
        "added": "1700000000",
        "category_id": "1",
        "custom_sid": "",
        "tv_archive": 0,
        "direct_source": "",
        "tv_archive_duration": 0
    }
]

# 2. الأفلام
MOVIES_DATABASE = [
    {
        "num": 1,
        "stream_id": 2,
        "name": "فيلم تجريبي 1",
        "stream_type": "movie",
        "stream_icon": "",
        "rating": "5.0",
        "rating_kinopoisk": "0",
        "added": "1700000000",
        "category_id": "2",
        "container_extension": "mp4"
    }
]

# 3. المسلسلات
SERIES_DATABASE = [
    {
        "num": 1,
        "series_id": 3,
        "name": "مسلسل تجريبي",
        "cover": "",
        "plot": "مسلسل تجريبي للتأكد من توافق الرسيفر",
        "cast": "Mahmood",
        "director": "Mahmood",
        "genre": "Drama",
        "releaseDate": "2026",
        "rating": "5.0",
        "category_id": "3"
    }
]

SERIES_EPISODES = {
    "3": [
        {
            "id": 301,
            "episode_num": 1,
            "title": "الحلقة الأولى",
            "container_extension": "mp4",
            "info": {}
        }
    ]
}

@app.route('/')
def home():
    return "MediaStar Xtream Codes Compatible Server is Active!"

# نقطة الاتصال والمصادقة الأساسية لرسيفرات أكستريم
@app.route('/player_api.php')
def player_api():
    username = request.args.get('username')
    password = request.args.get('password')
    action = request.args.get('action')

    # التحقق من بيانات الدخول
    if username != SERVER_CONFIG['username'] or password != SERVER_CONFIG['password']:
        return jsonify({
            "user_info": {"auth": 0, "status": "Expired"},
            "server_info": {"status": "Invalid"}
        }), 200

    # الأقسام المعتمدة للقوائم الثلاثة (Live, VOD, Series)
    if action == "get_live_categories":
        return jsonify([{"category_id": "1", "category_name": "Live Channels", "parent_id": 0}])
    elif action == "get_vod_categories":
        return jsonify([{"category_id": "2", "category_name": "Movies", "parent_id": 0}])
    elif action == "get_series_categories":
        return jsonify([{"category_id": "3", "category_name": "Series", "parent_id": 0}])

    # جلب قوائم المحتوى
    elif action == "get_live_streams":
        return jsonify(CHANNELS_DATABASE)
    elif action == "get_vod_streams":
        return jsonify(MOVIES_DATABASE)
    elif action == "get_series":
        return jsonify(SERIES_DATABASE)
    elif action == "get_series_info":
        info = {
            "seasons": [{"season_number": 1, "name": "الموسم الاول", "episode_count": 1}],
            "episodes": SERIES_EPISODES,
            "info": {
                "name": "مسلسل تجريبي",
                "cover": "",
                "plot": "وصف المسلسل التجريبي"
            }
        }
        return jsonify(info)

    # الاستجابة لعملية تسجيل الدخول الناجح من الرسيفر
    return jsonify({
        "user_info": {
            "username": username,
            "password": password,
            "auth": 1,
            "status": "Active",
            "exp_date": "2147483647",
            "is_trial": "0",
            "active_cons": "1",
            "max_connections": "10",
            "allowed_output_formats": ["m3u8", "ts", "rtmp"]
        },
        "server_info": {
            "url": SERVER_CONFIG['server_url'],
            "port": "443",
            "https_port": "443",
            "server_protocol": "https",
            "rtmp_port": "8080",
            "timezone": "UTC",
            "timestamp_now": 1780000000,
            "time_now": "2026-06-06 00:00:00"
        }
    })

# نقاط تشغيل البث المباشر
@app.route('/live/<username>/<password>/<int:stream_id>.ts')
@app.route('/live/<username>/<password>/<int:stream_id>')
def stream_live(username, password, stream_id):
    if username != SERVER_CONFIG['username'] or password != SERVER_CONFIG['password']:
        return "Unauthorized", 401
    return Response("Redirect", status=302, headers={"Location": "https://www.w3schools.com/html/mov_bbb.mp4"})

# نقاط تشغيل الأفلام
@app.route('/movie/<username>/<password>/<int:stream_id>.<ext>')
@app.route('/movie/<username>/<password>/<int:stream_id>')
def stream_movie(username, password, stream_id, ext="mp4"):
    if username != SERVER_CONFIG['username'] or password != SERVER_CONFIG['password']:
        return "Unauthorized", 401
    return Response("Redirect", status=302, headers={"Location": "https://www.w3schools.com/html/mov_bbb.mp4"})

# نقاط تشغيل المسلسلات
@app.route('/series/<username>/<password>/<int:episode_id>.<ext>')
@app.route('/series/<username>/<password>/<int:episode_id>')
def stream_series(username, password, episode_id, ext="mp4"):
    if username != SERVER_CONFIG['username'] or password != SERVER_CONFIG['password']:
        return "Unauthorized", 401
    return Response("Redirect", status=302, headers={"Location": "https://www.w3schools.com/html/html5.mp4"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
