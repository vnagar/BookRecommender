from app import app
from flask import jsonify

@app.route('/api')
@app.route('/api/index')
def api_index():
    return jsonify("Hello, World!")
