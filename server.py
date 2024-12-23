from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import time
from datetime import datetime
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def store_to_db(score: int):
    conn = sqlite3.connect('game.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS dino (
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      score INTEGER, 
                      time TEXT
                    ) 
                   ''')
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 當前時間
    cursor.execute('INSERT INTO dino (score, time) VALUES (?, ?)', (score, current_time))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """
    返回前端頁面
    """
    return render_template('index.html')
  
@app.route('/get_score', methods=['POST'])
def get_score():
    data = request.json
    score = data.get('score')
    store_to_db(score)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # 啟動 Flask-SocketIO 伺服器
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)