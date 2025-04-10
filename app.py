from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3  

app = Flask(__name__)  
CORS(app)

def init_db():  
    conn = sqlite3.connect('snippets.db')  
    c = conn.cursor()  
    c.execute('''CREATE TABLE IF NOT EXISTS snippets  
                 (id INTEGER PRIMARY KEY, title TEXT, language TEXT, code TEXT)''')  
    conn.commit()  
    conn.close()

init_db()  

@app.route('/snippets', methods=['GET'])  
def get_snippets():  
    conn = sqlite3.connect('snippets.db')  
    c = conn.cursor()  
    c.execute("SELECT * FROM snippets")  
    snippets = [{"id": row[0], "title": row[1], "language": row[2], "code": row[3]} for row in c.fetchall()]  
    conn.close()
    return jsonify(snippets)  

@app.route('/snippets', methods=['POST'])  
def add_snippet():  
    data = request.json  
    conn = sqlite3.connect('snippets.db')  
    c = conn.cursor()  
    c.execute("INSERT INTO snippets (title, language, code) VALUES (?, ?, ?)",  
              (data['title'], data['language'], data['code']))  
    conn.commit()  
    conn.close()
    return jsonify({"status": "success"})  

@app.route('/stats', methods=['GET'])
def snippet_stats():
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute("SELECT language, COUNT(*) FROM snippets GROUP BY language")
    stats = c.fetchall()
    conn.close()
    return jsonify(stats)

if __name__ == '__main__':  
    app.run(debug=True)