from flask import Flask, render_template, request, jsonify
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController
from app.port_utils import sort_ports_by_name
from app.graph_utils import prepare_graph_data
import json
import pandas as pd

app = Flask(__name__)

monitor = OpenFlowMonitor()
controller = OpenFlowController("http://localhost:8181", "admin", "admin")

@app.route("/")
def index():
    try:
        topology_details = monitor.get_full_topology()  
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
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("statistics.html", graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

@app.route("/network-management")
def network_management():
    try:
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("network_management.html", graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500
    
@app.route("/statistics/flow-stat")
def statistics_flow_stat():
    try:
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)

        stat_table = monitor.get_flow_statistics()
        return render_template(
            "base_statistics.html", 
            graph_data=json.dumps(graph_data),
            title="Flow Statistics",
            headers = stat_table.columns.tolist(),
            data = stat_table.values.tolist()
            )
    except Exception as e:
        return str(e), 500

@app.route("/statistics/flow-table-stat")
def statistics_flow_table_stat():
    try:
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)

        stat_table = monitor.get_flow_table_statistics()
        return render_template(
            "base_statistics.html", 
            graph_data=json.dumps(graph_data),
            title="Flow Table Statistics",
            headers = stat_table.columns.tolist(),
            data = stat_table.values.tolist()
            )
    except Exception as e:
        return str(e), 500

@app.route("/statistics/aggregate-flow-stat")
def statistics_aggregate_flow_stat():
    try:
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)

        stat_table = monitor.get_aggregate_flow_statistics()
        return render_template(
            "base_statistics.html", 
            graph_data=json.dumps(graph_data),
            title="Aggregate Flow Statistics",
            headers = stat_table.columns.tolist(),
            data = stat_table.values.tolist()
            )
    except Exception as e:
        return str(e), 500

@app.route("/statistics/ports-stat")
def statistics_ports_stat():
    try:
        topology_details = monitor.get_full_topology()  
        
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)

        stat_table = monitor.get_ports_statistics()
        return render_template(
            "base_statistics.html", 
            graph_data=json.dumps(graph_data),
            title="Ports Statistics",
            headers = stat_table.columns.tolist(),
            data = stat_table.values.tolist()
            )
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run()