#!/usr/bin/env python3
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'enhanced-frontend',
        'backend_url': 'http://localhost:8000'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=False)

