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

# 一覧（GET）＋ 保険でPOSTも受ける（/ に POST してもOKにする）
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return upload()  # 誤って / にPOSTしても動く
    
    # 投稿削除
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT filename FROM posts WHERE id=?", (post_id,))
    row = c.fetchone()
    if row:
        filename = row[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)   # 画像ファイル削除
        c.execute("DELETE FROM posts WHERE id=?", (post_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))


    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, filename, comment FROM posts ORDER BY id DESC LIMIT ? OFFSET ?',
              (PER_PAGE + 1, offset))  # 次ページ判定のため +1 件
    rows = c.fetchall()
    conn.close()

    has_next = len(rows) > PER_PAGE
    images = rows[:PER_PAGE]  # templateでは image[1]=filename, image[2]=comment を参照

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
