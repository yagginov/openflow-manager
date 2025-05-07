from flask import Flask, render_template, request, jsonify
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController

app = Flask(__name__)

monitor = OpenFlowMonitor()
controller = OpenFlowController("http://localhost:8181", "admin", "admin")

@app.route("/")
def index():
    try:
        stats = monitor.get_flow_stats()
        return render_template("index.html", stats=stats)
    except Exception as e:
        return str(e), 500

@app.route("/add_flow", methods=["POST"])
def add_flow():
    data = request.json
    try:
        controller.add_flow(data["node_id"], data["flow_id"], data["match"], data["actions"])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()