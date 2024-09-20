from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from config import Config
import asyncio

app = Flask(__name__)
socketio = SocketIO(app)
config = Config()

@app.route('/')
def index():
    return render_template('index.html', config=config.to_dict())

@app.route('/update_config', methods=['POST'])
def update_config():
    data = request.json
    config.update_from_dict(data)
    return jsonify({"status": "success"})

@app.route('/get_config', methods=['GET'])
def get_config():
    return jsonify(config.to_dict())

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    socketio.start_background_task(target=scraping_task)
    return jsonify({"status": "Scraping başlatıldı"})

def scraping_task():
    socketio.emit('scraping_progress', {'progress': 0})
    # ... scraping işlemi ...
    socketio.emit('scraping_progress', {'progress': 100})

if __name__ == '__main__':
    socketio.run(app, debug=True)