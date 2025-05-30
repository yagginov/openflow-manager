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

        ipv6_src = form.get("match_ipv6_src")
        if ipv6_src:
            match["ipv6-source"] = ipv6_src

        ipv6_dst = form.get("match_ipv6_dst")
        if ipv6_dst:
            match["ipv6-destination"] = ipv6_dst

        tcp_src = form.get("match_tcp_src")
        if tcp_src:
            match.setdefault("tcp-source-port", int(tcp_src))

        tcp_dst = form.get("match_tcp_dst")
        if tcp_dst:
            match.setdefault("tcp-destination-port", int(tcp_dst))

        udp_src = form.get("match_udp_src")
        if udp_src:
            match.setdefault("udp-source-port", int(udp_src))

        udp_dst = form.get("match_udp_dst")
        if udp_dst:
            match.setdefault("udp-destination-port", int(udp_dst))

        eth_src = form.get("match_eth_src")
        if eth_src:
            match.setdefault("ethernet-match", {}).setdefault("ethernet-source", {})["address"] = eth_src

        eth_dst = form.get("match_eth_dst")
        if eth_dst:
            match.setdefault("ethernet-match", {}).setdefault("ethernet-destination", {})["address"] = eth_dst

        vlan_id = form.get("match_vlan_id")
        if vlan_id:
            match.setdefault("vlan-match", {})["vlan-id"] = {
                "vlan-id": int(vlan_id),
                "vlan-id-present": True
            }

        ip_proto = form.get("match_ip_proto")
        if ip_proto:
            match["ip-match"] = {"ip-protocol": int(ip_proto)}

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

        set_ipv4_dst = form.get("action_set_ipv4_dst")
        if set_ipv4_dst:
            actions.append({
                "set-field": {
                    "ipv4-destination": set_ipv4_dst
                },
                "order": len(actions)
            })

        set_eth_src = form.get("action_set_eth_src")
        if set_eth_src:
            actions.append({
                "set-field": {
                    "eth-source": set_eth_src
                },
                "order": len(actions)
            })

        set_eth_dst = form.get("action_set_eth_dst")
        if set_eth_dst:
            actions.append({
                "set-field": {
                    "eth-destination": set_eth_dst
                },
                "order": len(actions)
            })

        set_vlan_id = form.get("action_set_vlan_id")
        if set_vlan_id:
            actions.append({
                "set-field": {
                    "vlan-match": {
                        "vlan-id": {
                            "vlan-id": int(set_vlan_id),
                            "vlan-id-present": True
                        }
                    }
                },
                "order": len(actions)
            })

        if form.get("action_push_vlan"):
            actions.append({
                "push-vlan-action": {
                    "ethernet-type": 33024  # 0x8100
                },
                "order": len(actions)
            })

        if form.get("action_pop_vlan"):
            actions.append({
                "pop-vlan-action": {},
                "order": len(actions)
            })

        set_queue = form.get("action_set_queue")
        if set_queue:
            actions.append({
                "set-queue-action": {
                    "queue-id": int(set_queue)
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