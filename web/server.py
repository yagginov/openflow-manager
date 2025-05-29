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

@app.route("/")
def index():
    try:
        topology_details = monitor.get_full_topology()          
        # Підготовка даних для графа
        graph_data = prepare_graph_data(topology_details)
        return render_template("index.html", topology=topology_details, graph_data=json.dumps(graph_data))
    except Exception as e:
        return str(e), 500

@app.route('/flows')
def flows():
    try:
        topology_details = monitor.get_full_topology()
        graph_data = prepare_graph_data(topology_details)

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
    try:
        controller.delete_flow(node_id, table_id, flow_id)
        flash('Flow deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting flow: {e}', 'danger')
    return redirect(url_for('flows'))

@app.route('/flows/edit/<node_id>/<table_id>/<flow_id>', methods=['GET', 'POST'])
def edit_flow(node_id, table_id, flow_id):
    if request.method == 'POST':
        # Збираємо flow entry з форми
        try:
            flow_entry = {
                "id": request.form.get("id"),
                "priority": int(request.form.get("priority")),
                "table_id": int(request.form.get("table_id")),
                "match": json.loads(request.form.get("match")),
                "instructions": json.loads(request.form.get("instructions")),
                # Додайте інші поля за потреби
            }
            controller.update_flow(node_id, table_id, flow_id, flow_entry)
            flash('Flow updated successfully', 'success')
            return redirect(url_for('flows'))
        except Exception as e:
            flash(f'Error updating flow: {e}', 'danger')
            # Повертаємо форму з введеними даними
            return render_template("edit_flow.html", flow_info=request.form)
    else:
        flow_info = monitor.get_flow_info(node_id, table_id, flow_id)
        if flow_info is None:
            flash('Flow not found', 'danger')
            return redirect(url_for('flows'))
        return render_template("edit_flow.html", flow_info=flow_info)

if __name__ == "__main__":
    app.run()