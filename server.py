from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import time
from datetime import datetime
import sqlite3
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

post_url = 'http://192.168.XXX.XXX:5000/'

conn = sqlite3.connect('game.db', check_same_thread=False)
cursor = conn.cursor()

def store_to_db(score: int):
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

@app.route('/')
def index():
    """
    返回前端頁面
    """
    return render_template('index.html')
  
@app.route('/history')
def history():
    """
    返回 history.html 頁面
    """
    return render_template('history.html')
  
@app.route('/get_score', methods=['POST'])
def get_score():
    data = request.json
    score = data.get('score')
    store_to_db(score)
    return jsonify({"status": f"success {score}"})

@app.route('/send_score', methods=['POST'])
def send_score():
    data = request.json
    class_name = data.get('class')
    group = data.get('group')
    try:
        cursor.execute('SELECT * FROM dino ORDER BY score DESC LIMIT 1')
        data = cursor.fetchall()
        if len(data) == 0:
            # 資料庫內沒內容
            return jsonify({"status": "fail", "score": -1})
        print(data)
    except Exception as e:
        print(e)
        # 沒有資料庫
        return jsonify({"status": "fail", "score": -2})
    
    response = requests.post(post_url, json={"class": class_name, "group": group, "score": data[0][1]})
    
    if response.status_code != 200:
        # post發送失敗
        return jsonify({"status": "fail", "score": -3})
    
    return jsonify({"status": "success", "score": data[0][1]})

@app.route('/get_score_data', methods=['GET'])
def get_score_data():
    cursor.execute('SELECT * FROM dino ORDER BY id ASC')
    data = cursor.fetchall()
    return jsonify(data)

if __name__ == '__main__':
    # 啟動 Flask-SocketIO 伺服器
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)