# =========================
# STEP 1: INSTALL
# =========================
# pip install flask sqlite3

# =========================
# STEP 2: BACKEND (app.py)
# =========================
from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

# Create DB
conn = sqlite3.connect('videos.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    category TEXT
)
''')
conn.commit()

# HTML Frontend
HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>My YouTube Hub</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-6">

<h1 class="text-3xl font-bold mb-4">YouTube Hub</h1>

<input id="url" placeholder="Paste YouTube link" class="border p-2 w-full mb-2" />
<select id="category" class="border p-2 w-full mb-2">
  <option>Machine Learning Podcasts</option>
  <option>Machine Learning Courses</option>
  <option>Universities</option>
  <option>Music</option>
  <option>Business</option>
</select>
<button onclick="addVideo()" class="bg-blue-500 text-white px-4 py-2">Add</button>

<input id="search" placeholder="Search category..." class="border p-2 w-full mt-4" onkeyup="loadVideos()" />

<div id="videos" class="grid grid-cols-3 gap-4 mt-4"></div>

<script>
function getEmbed(url) {
  const id = url.split("v=")[1]?.split("&")[0];
  return `https://www.youtube.com/embed/${id}`;
}

function addVideo() {
  const url = document.getElementById("url").value;
  const category = document.getElementById("category").value;

  fetch('/add', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url, category})
  }).then(() => loadVideos());
}

function loadVideos() {
  const search = document.getElementById("search").value;

  fetch('/videos?search=' + search)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("videos");
      container.innerHTML = "";

      data.forEach(v => {
        container.innerHTML += `
          <div class="bg-white p-2 shadow rounded">
            <iframe src="${getEmbed(v.url)}" class="w-full h-40"></iframe>
            <p class="text-sm mt-2">${v.category}</p>
          </div>
        `;
      });
    });
}

loadVideos();
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/add', methods=['POST'])
def add_video():
    data = request.json
    cursor.execute("INSERT INTO videos (url, category) VALUES (?, ?)", (data['url'], data['category']))
    conn.commit()
    return jsonify({'status': 'ok'})

@app.route('/videos')
def get_videos():
    search = request.args.get('search', '')
    cursor.execute("SELECT url, category FROM videos WHERE category LIKE ?", ('%' + search + '%',))
    rows = cursor.fetchall()
    return jsonify([{'url': r[0], 'category': r[1]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# =========================
# STEP 3: DEPLOY (PUBLIC URL)
# =========================
# Use one of these:
# 1. Render.com (FREE)
# 2. Railway.app
# 3. PythonAnywhere

# Example (Render):
# - Push this file to GitHub
# - Go to render.com → New Web Service
# - Connect repo
# - Build command: pip install flask
# - Start command: python app.py

# You will get a URL like:
# https://your-app.onrender.com
