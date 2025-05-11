from flask import Flask, render_template, request, jsonify
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController
from app.port_utils import sort_ports_by_name
from app.graph_utils import prepare_graph_data
import json

app = Flask(__name__)

monitor = OpenFlowMonitor()
controller = OpenFlowController("http://localhost:8181", "admin", "admin")

@app.route("/")
def index():
    try:
        topology_details = monitor.get_full_topology()  # Використовуємо новий метод
        # Сортуємо порти для кожного вузла
        for node in topology_details["nodes"]["node"]:
            node["node-connector"] = sort_ports_by_name(node["node-connector"])
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("index.html", topology=topology_details, graph_data=json.dumps(graph_data))
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

@app.route("/statistics")
def statistics():
    try:
        topology_details = monitor.get_full_topology()  # Використовуємо новий метод
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("statistics.html", graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

@app.route("/network-management")
def network_management():
    try:
        topology_details = monitor.get_full_topology()  # Використовуємо новий метод
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("network_management.html", graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run()