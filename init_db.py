# init_db.py
import sqlite3

# データベースファイルに接続（無ければ作成されます）
conn = sqlite3.connect('database.db')
c = conn.cursor()

# postsテーブルを作成
c.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("✅ database.db が作成されました。")
