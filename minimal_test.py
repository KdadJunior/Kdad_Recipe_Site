#!/usr/bin/env python3
"""
Minimal test to check Flask app
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_route():
    return jsonify({"status": "working"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
