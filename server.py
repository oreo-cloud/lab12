from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import time
from datetime import datetime
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """
    返回前端頁面
    """
    return render_template('index.html')

if __name__ == '__main__':
    # 啟動 Flask-SocketIO 伺服器
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)