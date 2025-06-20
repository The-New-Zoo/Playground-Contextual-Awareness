from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/data/database.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
        cursor.execute("CREATE TABLE entries (id INTEGER PRIMARY KEY, title TEXT, content TEXT, user_id INTEGER);")
        cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob');")
        cursor.execute("""
            INSERT INTO entries (title, content, user_id) VALUES 
            ('First Post', 'This is the first post.', 1),
            ('Another Post', 'Written by Bob.', 2),
            ('Deep Thoughts', 'Alice has ideas.', 1);
        """)
        conn.commit()
        conn.close()

@app.route('/query', methods=['GET'])
def query():
    sql = request.args.get('sql')
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
