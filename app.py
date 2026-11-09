from flask import Flask, jsonify, Response, request

app = Flask(__name__)

# بيانات الدخول الوهمية الخاصة بنظام أكستريم
SERVER_CONFIG = {
    "username": "admin",
    "password": "123",
    "server_url": "https://mediastar-m3u.onrender.com"
}

# قاعدة البيانات مصنفة حسب الأقسام
CHANNELS_DATABASE = [
    {
        "stream_id": 1,
        "name": "قناة تجريبية 1",
        "stream_type": "live",
        "stream_icon": "",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "category_id": "1",
        "category_name": "Live Channels"
    }
]

MOVIES_DATABASE = [
    {
        "stream_id": 2,
        "name": "فيلم تجريبي 1",
        "stream_type": "movie",
        "stream_icon": "",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "category_id": "2",
        "category_name": "Movies"
    }
]

SERIES_DATABASE = [
    {
        "stream_id": 3,
        "name": "مسلسل تجريبي - الحلقة الأولى",
        "stream_type": "series",
        "stream_icon": "",
        "url": "https://www.w3schools.com/html/html5.mp4",
        "category_id": "3",
        "category_name": "Series"
    }
]

@app.route('/')
def home():
    return "MediaStar Xtream Codes Server is Running Successfully!"

# نقطة التحقق وتسجيل الدخول (player_api.php)
@app.route('/player_api.php')
def player_api():
    username = request.args.get('username')
    password = request.args.get('password')
    action = request.args.get('action')

    # التحقق من بيانات الدخول
    if username != SERVER_CONFIG['username'] or password != SERVER_CONFIG['password']:
        return jsonify({"user_info": {"auth": 0}, "server_info": {"status": "Invalid"}}), 401

    # إذا طلب التطبيق الأقسام (Categories)
    if action == "get_live_categories":
        return jsonify([{"category_id": "1", "category_name": "Live Channels"}])
    elif action == "get_vod_categories":
        return jsonify([{"category_id": "2", "category_name": "Movies"}])
    elif action == "get_series_categories":
        return jsonify([{"category_id": "3", "category_name": "Series"}])

    # إذا طلب القنوات أو الأفلام
    elif action == "get_live_streams":
        return jsonify(CHANNELS_DATABASE)
    elif action == "get_vod_streams":
        return jsonify(MOVIES_DATABASE)
    elif action == "get_series":
        # تنسيق مبسط للمسلسلات في أكستريم
        return jsonify([{
            "series_id": 3,
            "name": "مسلسل تجريبي",
            "cover": "",
            "category_id": "3"
        }])

    # المعلومات الافتراضية عند تسجيل الدخول الناجح
    user_data = {
        "user_info": {
            "username": username,
            "password": password,
            "auth": 1,
            "status": "Active",
            "exp_date": "2147483647",
            "is_trial": "0",
            "active_cons": "1",
            "max_connections": "10"
        },
        "server_info": {
            "url": SERVER_CONFIG['server_url'],
            "port": "443",
            "https_port": "443",
            "server_protocol": "https",
            "time_now": "2026-06-06 00:00:00",
            "timestamp_now": 1780000000
        }
    }
    return jsonify(user_data)

# نقطة توليد ملف M3U عبر بيانات أكستريم (get.php)
@app.route('/get.php')
def get_playlist():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username != SERVER_CONFIG['username'] or password != SERVER_CONFIG['password']:
        return "Unauthorized", 401

    m3u_content = "#EXTM3U\n"
    all_media = CHANNELS_DATABASE + MOVIES_DATABASE + SERIES_DATABASE
    
    for item in all_media:
        m3u_content += f"#EXTINF:-1 tvg-name=\"{item['name']}\" group-title=\"{item['category_name']}\",{item['name']}\n"
        m3u_content += f"{item['url']}\n"
        
    return Response(m3u_content, mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
