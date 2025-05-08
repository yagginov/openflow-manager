from flask import Flask, render_template, request, jsonify
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController

app = Flask(__name__)

monitor = OpenFlowMonitor()
controller = OpenFlowController("http://localhost:8181", "admin", "admin")

def sort_ports_by_name(ports):
    import re
    # Сортуємо порти за числовою частиною імені
    def extract_number(port_name):
        match = re.search(r'\d+', port_name)
        return int(match.group()) if match else float('inf')  # Якщо немає числа, ставимо "безкінечність"
    
    return sorted(ports, key=lambda port: extract_number(port.get("flow-node-inventory:name", "")))

@app.route("/")
def index():
    try:
        topology_details = monitor.get_topology()
        # Сортуємо порти для кожного вузла
        for node in topology_details["nodes"]["node"]:
            node["node-connector"] = sort_ports_by_name(node["node-connector"])
        return render_template("index.html", topology=topology_details)
    except Exception as e:
        return str(e), 500

@app.route("/add_flow", methods=["POST"])
def add_flow():
    data = request.json
    try:
        # Assuming you have a controller to handle adding flows
        controller.add_flow(data["node_id"], data["flow_id"], data["match"], data["actions"])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()