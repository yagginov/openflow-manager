from flask import Flask, render_template, request, jsonify
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController
import json

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

def prepare_graph_data(topology_details):
    nodes = []
    edges = []

    for node in topology_details["nodes"]["node"]:
        # Додаємо вузол для свіча
        nodes.append({
            "id": node["id"],
            "label": node["id"],
            "title": f"Hardware: {node.get('flow-node-inventory:hardware', 'N/A')}<br>IP: {node.get('flow-node-inventory:ip-address', 'N/A')}",
            "group": "switch"  # Група для стилізації
        })

        # Обробляємо порти
        for connector in node.get("node-connector", []):
            # Додаємо вузли для комп'ютерів, підключених до порту
            for address in connector.get("address-tracker:addresses", []):
                computer_id = f"{node['id']}-{address['mac']}"  # Унікальний ID для комп'ютера
                nodes.append({
                    "id": computer_id,
                    "label": address["ip"],
                    "title": f"MAC: {address['mac']}<br>IP: {address['ip']}",
                    "group": "computer"  # Група для стилізації
                })

                # Додаємо зв'язок між свічем і комп'ютером
                edges.append({
                    "from": node["id"],
                    "to": computer_id,
                    "label": f"Port: {connector.get('flow-node-inventory:name', 'N/A')}"
                })

    return {"nodes": nodes, "edges": edges}

@app.route("/")
def index():
    try:
        topology_details = monitor.get_topology()
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
        # Assuming you have a controller to handle adding flows
        controller.add_flow(data["node_id"], data["flow_id"], data["match"], data["actions"])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()