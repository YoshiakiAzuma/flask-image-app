import os
import sqlite3
from flask import Flask, request, redirect, url_for, render_template, send_from_directory

app = Flask(__name__)

# 画像保存フォルダ
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_FILE = 'posts.db'
PER_PAGE = 48  # 1ページ48枚

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    comment TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# ヘルスチェック（Render向け）
@app.route('/healthz', methods=['GET', 'HEAD'])
def healthz():
    return ('ok', 200)

# 一覧（GET/POST/HEAD）
@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    # Renderのヘルスチェック対策：HEADは即200を返す
    if request.method == 'HEAD':
        return ('', 200)

    if request.method == 'POST':
        return upload()  # 誤って / にPOSTしても動く

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 次ページ判定のため +1 件
    c.execute('SELECT id, filename, comment FROM posts ORDER BY id DESC LIMIT ? OFFSET ?',
              (PER_PAGE + 1, offset))
    rows = c.fetchall()
    conn.close()

    has_next = len(rows) > PER_PAGE
    images = rows[:PER_PAGE]  # templateでは image[1]=filename, image[2]=comment

    return render_template('index.html', images=images, page=page, has_next=has_next)

# アップロード（/upload に POST）
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')        # name="file"
    comment = request.form.get('comment', '')

    if file and file.filename:
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO posts (filename, comment) VALUES (?, ?)', (file.filename, comment))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

# 画像配信
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Render対応
if __name__ == '__main__':
    # 本番ではGunicornを推奨だが、まずはこのままでも可
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
