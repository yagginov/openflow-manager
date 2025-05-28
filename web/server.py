from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController
from app.graph_utils import prepare_graph_data
import json
import pandas as pd

app = Flask(__name__)

monitor = OpenFlowMonitor()
controller = OpenFlowController()

@app.route("/")
def index():
    try:
        topology_details = monitor.get_full_topology()          
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("index.html", topology=topology_details, graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

@app.route("/debug-info")
def debug_info():
    try:
        topology_details = monitor.get_full_topology()          
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("debug_info.html", topology=topology_details, graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

@app.route('/flows')
def flows():
    monitor = OpenFlowMonitor()
    nodes = monitor.get_nodes()
    flows_data = []
    for node in nodes:
        node_id = node["id"]
        for table in node.get("flow-node-inventory:table", []):
            table_id = table["id"]
            for flow in table.get("flow", []):
                flow_id = flow["id"]
                priority = flow.get("priority", "")
                match = flow.get("match", {})
                actions = flow.get("instructions", {})
                flows_data.append([
                    node_id, table_id, flow_id, priority, str(match), str(actions)
                ])
    headers = ["Node ID", "Table ID", "Flow ID", "Priority", "Match", "Actions", "Edit", "Delete"]
    return render_template("flows.html", title="Active Flows", headers=headers, data=flows_data)

@app.route("/network-management")
def network_management():
    try:
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("network_management.html", graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500
    
@app.route("/statistics/<stat_type>")
def statistics(stat_type):
    try:
        topology_details = monitor.get_full_topology()
        graph_data = prepare_graph_data(topology_details)

        # Визначаємо, яку статистику повертати
        if stat_type == "flow-stat":
            stat_table = monitor.get_flow_statistics()
            title = "Flow Statistics"
        elif stat_type == "flow-table-stat":
            stat_table = monitor.get_flow_table_statistics()
            title = "Flow Table Statistics"
        elif stat_type == "aggregate-flow-stat":
            stat_table = monitor.get_aggregate_flow_statistics()
            title = "Aggregate Flow Statistics"
        elif stat_type == "ports-stat":
            stat_table = monitor.get_ports_statistics()
            title = "Ports Statistics"
        else:
            return "Unknown statistics type", 404

        return render_template(
            "base_statistics.html",
            graph_data=json.dumps(graph_data),
            title=title,
            headers=stat_table.columns.tolist(),
            data=stat_table.values.tolist()
        )
    except Exception as e:
        return str(e), 500

@app.route('/flows/delete/<node_id>/<table_id>/<flow_id>', methods=['POST'])
def delete_flow(node_id, table_id, flow_id):
    controller = OpenFlowController()
    try:
        controller.delete_flow(node_id, table_id, flow_id)
        flash('Flow deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting flow: {e}', 'danger')
    return redirect(url_for('flows'))

@app.route('/flows/edit/<node_id>/<table_id>/<flow_id>', methods=['GET', 'POST'])
def edit_flow(node_id, table_id, flow_id):
    # Тут реалізуйте форму для перегляду/редагування flow
    # GET: показати форму з поточними даними flow
    # POST: зберегти зміни через controller.create_flow(...)
    pass

if __name__ == "__main__":
    app.run()