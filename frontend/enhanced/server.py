#!/usr/bin/env python3
from flask import Flask, send_from_directory, jsonify, make_response
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.after_request
def add_header(response):
    """Add cache-control headers to prevent CSS/JS caching issues"""
    if response.content_type and ('text/css' in response.content_type or 
                                  'javascript' in response.content_type or
                                  'text/html' in response.content_type):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

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
