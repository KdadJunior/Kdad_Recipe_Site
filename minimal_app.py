#!/usr/bin/env python3
"""
Minimal Flask app to test the issue
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/clear', methods=['GET'])
def clear_db():
    return jsonify({"status": 1})

@app.route('/create_user', methods=['POST'])
def create_user():
    return jsonify({"status": 1, "pass_hash": "test"})

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"status": 1, "jwt": "test_jwt"})

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    return jsonify({"status": 1, "recipe_id": 1})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
