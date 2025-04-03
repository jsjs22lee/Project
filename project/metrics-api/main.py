from flask import Flask, jsonify
from scheduler import generate_dynamic_config
import os

app = Flask(__name__)

@app.route("/update")
def update_config():
    config = generate_dynamic_config()
    with open("/traefik/dynamic_conf.yml", "w") as f:
        f.write(config)
    return jsonify({"status": "updated"})
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
