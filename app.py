from flask import Flask, Response

app = Flask(__name__)

MOVIES_DATABASE = [
    {
        "title": "فيديو تجريبي 1",
        "url": "https://www.w3schools.com/html/mov_bbb.mp4"
    },
    {
        "title": "فيديو تجريبي 2",
        "url": "https://www.w3schools.com/html/html5.mp4"
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
