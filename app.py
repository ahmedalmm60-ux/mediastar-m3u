from flask import Flask, Response

app = Flask(__name__)

MOVIES_DATABASE = [
    {
        "title": "فيلم تجريبي 1 (720p)",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    },
    {
        "title": "فيلم تجريبي 2 (720p)",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
    }
]

@app.route('/')
def home():
    return "MediaStar M3U Generator is Running Successfully!"

@app.route('/playlist.m3u')
def generate_m3u():
    m3u_content = "#EXTM3U\n"
    for item in MOVIES_DATABASE:
        m3u_content += f"#EXTINF:-1 tvg-name=\"{item['title']}\" group-title=\"Movies\",{item['title']}\n"
        m3u_content += f"{item['url']}\n"
    return Response(m3u_content, mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
