from flask import Flask, Response

app = Flask(__name__)

# قاعدة بيانات مقسمة إلى أقسام: قنوات، أفلام، ومسلسلات
CHANNELS_DATABASE = [
    {
        "title": "قناة تجريبية 1",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "group": "Live Channels"
    }
]

MOVIES_DATABASE = [
    {
        "title": "فيلم تجريبي 1",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "group": "Movies"
    }
]

SERIES_DATABASE = [
    {
        "title": "مسلسل تجريبي - الحلقة الأولى",
        "url": "https://www.w3schools.com/html/html5.mp4",
        "group": "Series"
    }
]

@app.route('/')
def home():
    return "MediaStar Apollo5 M3U Generator is Running Successfully!"

@app.route('/playlist.m3u')
def generate_m3u():
    # وسم البداية الإلزامي لملفات M3U لتتطابق مع معايير التطبيقات مثل Apollo5
    m3u_content = "#EXTM3U\n"
    
    # دمج جميع الأقسام في القائمة بترتيب منظم
    all_media = CHANNELS_DATABASE + MOVIES_DATABASE + SERIES_DATABASE
    
    for item in all_media:
        # إضافة خصائص الـ M3U مع تحديد اسم القسم (group-title) لكي يصنفها Apollo5 تلقائياً
        m3u_content += f"#EXTINF:-1 tvg-name=\"{item['title']}\" group-title=\"{item['group']}\",{item['title']}\n"
        m3u_content += f"{item['url']}\n"
        
    return Response(m3u_content, mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
