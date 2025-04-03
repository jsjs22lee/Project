from flask import Flask, jsonify
from scheduler import get_best_node

app = Flask(__name__)

@app.route("/best-node")
def best_node():
    try:
        node = get_best_node()
        return jsonify({"node": node})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)