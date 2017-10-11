"""
Data Access Layer abstracts database accesses by exposing a RESTful API
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({
            'up': True  # the server is up
        })
    else:
        # echo whatever is posted for now
        if request.json is not None:
            return jsonify(request.json)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
