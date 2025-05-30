from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from app.monitor import OpenFlowMonitor
from app.controller import OpenFlowController
from app.graph_utils import prepare_graph_data
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = 'yagginov-secret-key'

monitor = OpenFlowMonitor()
controller = OpenFlowController()

def get_topology_and_graph(monitor):
    topology_details = monitor.get_full_topology()
    graph_data = prepare_graph_data(topology_details)
    return topology_details, graph_data

@app.route("/")
def index():
    try:
        topology_details, graph_data = get_topology_and_graph(monitor)
        return render_template("index.html", topology=topology_details, graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

@app.route('/flows')
def flows():
    try:
        topology_details, graph_data = get_topology_and_graph(monitor)

        flows = monitor.get_flows()
        return render_template(
            "flows.html", 
            graph_data=json.dumps(graph_data),
            title="Active Flows", 
            headers=flows.columns.tolist(), 
            data=flows.values.tolist()
            )
    except Exception as e:
        return str(e), 500
    
STATISTICS_MAP = {
    "flow-stat": (monitor.get_flow_statistics, "Flow Statistics"),
    "flow-table-stat": (monitor.get_flow_table_statistics, "Flow Table Statistics"),
    "aggregate-flow-stat": (monitor.get_aggregate_flow_statistics, "Aggregate Flow Statistics"),
    "ports-stat": (monitor.get_ports_statistics, "Ports Statistics"),
}

@app.route("/statistics/<stat_type>")
def statistics(stat_type):
    try:
        topology_details, graph_data = get_topology_and_graph(monitor)
        stat_func, title = STATISTICS_MAP.get(stat_type, (None, None))
        if stat_func is None:
            return "Unknown statistics type", 404
        stat_table = stat_func()
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
    try:
        controller.delete_flow(node_id, table_id, flow_id)
        flash('Flow deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting flow: {e}', 'danger')
    return redirect(url_for('flows'))




@app.route('/flows/edit/<node_id>/<table_id>/<flow_id>', methods=['GET', 'POST'])
def edit_flow(node_id, table_id, flow_id):
    if request.method == 'POST':
        try:
            print(f"node_id: {node_id}\ntable_id: {table_id}\nflow_id: {flow_id}")

            # Використовуємо build_flow_entry з контролера
            flow_entry = controller.build_flow_entry(request.form)
            print(flow_entry)

            controller.create_flow(node_id, flow_entry["flow"][0]["table_id"], flow_entry["flow"][0]["id"], flow_entry)
            flash('Flow updated successfully', 'success')
            return redirect(url_for('flows'))

        except Exception as e:
            print(e)
            
            flow_info = extract_flow_info(request.form)

            topology_details, graph_data = get_topology_and_graph(monitor)
            return render_template(
                "edit_flow.html", 
                topology_details=topology_details, 
                graph_data=graph_data,
                flow_info=flow_info, 
                json_info={})
        
    else:
        flow_info = monitor.get_flow_info(node_id, table_id, flow_id)
        json_flow_info = monitor.get_json_flow_info(node_id, table_id, flow_id)
        if flow_info is None:
            flash('Flow not found', 'danger')
            print("Problem with flow")
            return redirect(url_for('flows'))
        
        topology_details, graph_data = get_topology_and_graph(monitor)
        return render_template(
            "edit_flow.html", 
            topology_details=topology_details, 
            graph_data=graph_data,
            flow_info=flow_info, 
            json_info=json_flow_info)

@app.route('/flows/create', methods=['GET', 'POST'])
def create_flow():
    if request.method == 'POST':
        try:
            # Створюємо flow_entry з форми
            flow_entry = controller.build_flow_entry(request.form)
            node_id = request.form.get("node_id")
            table_id = flow_entry["flow"][0]["table_id"]
            flow_id = flow_entry["flow"][0]["id"]
            controller.create_flow(node_id, table_id, flow_id, flow_entry)
            flash('Flow created successfully', 'success')
            return redirect(url_for('flows'))
        except Exception as e:
            print(e)
            flow_info = extract_flow_info(request.form)
            topology_details, graph_data = get_topology_and_graph(monitor)
            return render_template(
                "edit_flow.html", 
                topology_details=topology_details, 
                graph_data=graph_data,
                flow_info=flow_info, 
                json_info={})
    else:
        # Порожні дані для нової форми
        flow_info = {
            "id": "",
            "priority": "",
            "table_id": "",
            "match_in_port": "",
            "match_eth_type": "",
            "match_ipv4_src": "",
            "match_ipv4_dst": "",
            "match_ipv6_src": "",
            "match_ipv6_dst": "",
            "match_tcp_src": "",
            "match_tcp_dst": "",
            "match_udp_src": "",
            "match_udp_dst": "",
            "match_eth_src": "",
            "match_eth_dst": "",
            "match_vlan_id": "",
            "match_ip_proto": "",
            "action_output": "",
            "action_drop": False,
            "action_set_ipv4_src": "",
            "action_set_ipv4_dst": "",
            "action_set_eth_src": "",
            "action_set_eth_dst": "",
            "action_set_vlan_id": "",
            "action_push_vlan": False,
            "action_pop_vlan": False,
            "action_set_queue": "",
            "node_id": ""
        }
        topology_details, graph_data = get_topology_and_graph(monitor)
        return render_template(
            "edit_flow.html", 
            topology_details=topology_details, 
            graph_data=graph_data,
            flow_info=flow_info, 
            json_info={})

def extract_flow_info(form):
    return {
        "id": form.get("id", ""),
        "priority": form.get("priority", ""),
        "table_id": form.get("table_id", ""),
        "match_in_port": form.get("match_in_port", ""),
        "match_eth_type": form.get("match_eth_type", ""),
        "match_ipv4_src": form.get("match_ipv4_src", ""),
        "match_ipv4_dst": form.get("match_ipv4_dst", ""),
        "match_ipv6_src": form.get("match_ipv6_src", ""),
        "match_ipv6_dst": form.get("match_ipv6_dst", ""),
        "match_tcp_src": form.get("match_tcp_src", ""),
        "match_tcp_dst": form.get("match_tcp_dst", ""),
        "match_udp_src": form.get("match_udp_src", ""),
        "match_udp_dst": form.get("match_udp_dst", ""),
        "match_eth_src": form.get("match_eth_src", ""),
        "match_eth_dst": form.get("match_eth_dst", ""),
        "match_vlan_id": form.get("match_vlan_id", ""),
        "match_ip_proto": form.get("match_ip_proto", ""),
        "action_output": form.get("action_output", ""),
        "action_drop": "action_drop" in form,
        "action_set_ipv4_src": form.get("action_set_ipv4_src", ""),
        "action_set_ipv4_dst": form.get("action_set_ipv4_dst", ""),
        "action_set_eth_src": form.get("action_set_eth_src", ""),
        "action_set_eth_dst": form.get("action_set_eth_dst", ""),
        "action_set_vlan_id": form.get("action_set_vlan_id", ""),
        "action_push_vlan": "action_push_vlan" in form,
        "action_pop_vlan": "action_pop_vlan" in form,
        "action_set_queue": form.get("action_set_queue", ""),
        "node_id": form.get("node_id", "")
    }

if __name__ == "__main__":
    app.run(debug=True)