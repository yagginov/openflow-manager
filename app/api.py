from flask import Blueprint, jsonify
from app.monitor import OpenFlowMonitor

api = Blueprint("api", __name__)
monitor = OpenFlowMonitor()

@api.route("/api/topology", methods=["GET"])
def get_topology():
    """Отримати інформацію про топологію мережі через API."""
    try:
        topology_details = monitor.get_topology()
        return jsonify(topology_details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500