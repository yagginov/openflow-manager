import requests
import json
from app.opendaylight_client import create_flow as odl_create_flow, delete_flow as odl_delete_flow

# Load configuration from config.json (як у monitor.py)
with open("app/config.json", "r") as config_file:
    config = json.load(config_file)

BASE_URL = config["BASE_URL"]
HEADERS = config["HEADERS"]

class OpenFlowController:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def build_flow_entry(self, form):
        """Створює flow_entry з даних форми."""
        # --- MATCH ---
        match = {}
        in_port = form.get("match_in_port")
        if in_port:
            match["in-port"] = in_port

        eth_type = form.get("match_eth_type")
        if eth_type:
            match["ethernet-match"] = {
                "ethernet-type": {
                    "type": int(eth_type)
                }
            }

        ipv4_src = form.get("match_ipv4_src")
        if ipv4_src:
            match["ipv4-source"] = ipv4_src

        ipv4_dst = form.get("match_ipv4_dst")
        if ipv4_dst:
            match["ipv4-destination"] = ipv4_dst

        # --- ACTIONS ---
        actions = []

        output_port = form.get("action_output")
        if output_port:
            actions.append({
                "output-action": {
                    "output-node-connector": output_port,
                    "max-length": 65535
                },
                "order": len(actions)
            })

        if form.get("action_drop"):
            actions.append({
                "drop-action": {},
                "order": len(actions)
            })

        set_ipv4_src = form.get("action_set_ipv4_src")
        if set_ipv4_src:
            actions.append({
                "set-field": {
                    "ipv4-source": set_ipv4_src
                },
                "order": len(actions)
            })

        flow_id = form.get("id")
        priority = int(form.get("priority"))
        table_id = int(form.get("table_id"))

        instructions = {
            "instruction": [
                {
                    "order": 0,
                    "apply-actions": {
                        "action": actions
                    }
                }
            ]
        }

        flow_entry = {
            "flow": [
                {
                    "id": flow_id,
                    "table_id": table_id,
                    "priority": priority,
                    "match": match,
                    "instructions": instructions
                }
            ]
        }
        return flow_entry

    def create_flow(self, node_id, table_id, flow_id, flow_data):
        return odl_create_flow(node_id, table_id, flow_id, flow_data)

    def delete_flow(self, node_id, table_id, flow_id):
        return odl_delete_flow(node_id, table_id, flow_id)