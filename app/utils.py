import json

def get_topology_and_graph(monitor, prepare_graph_data):
    topology_details = monitor.get_full_topology()
    graph_data = prepare_graph_data(topology_details)
    return topology_details, graph_data

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

def parse_actions_from_flow(flow):
    """Розбирає actions з flow-entry у прості поля для форми."""
    actions = {}
    try:
        instructions = flow.get("instructions", {}).get("instruction", [])
        if instructions:
            actions_list = instructions[0].get("apply-actions", {}).get("action", [])
            for act in actions_list:
                if "output-action" in act:
                    actions["action_output"] = act["output-action"].get("output-node-connector", "")
                if "drop-action" in act:
                    actions["action_drop"] = True
                if "set-field" in act:
                    sf = act["set-field"]
                    if "ipv4-source" in sf:
                        actions["action_set_ipv4_src"] = sf["ipv4-source"]
                    if "ipv4-destination" in sf:
                        actions["action_set_ipv4_dst"] = sf["ipv4-destination"]
                    if "eth-source" in sf:
                        actions["action_set_eth_src"] = sf["eth-source"]
                    if "eth-destination" in sf:
                        actions["action_set_eth_dst"] = sf["eth-destination"]
                    if "vlan-match" in sf and "vlan-id" in sf["vlan-match"]:
                        actions["action_set_vlan_id"] = sf["vlan-match"]["vlan-id"]["vlan-id"]
                if "push-vlan-action" in act:
                    actions["action_push_vlan"] = True
                if "pop-vlan-action" in act:
                    actions["action_pop_vlan"] = True
                if "set-queue-action" in act:
                    actions["action_set_queue"] = act["set-queue-action"].get("queue-id", "")
    except Exception as e:
        print("Error parsing actions:", e)
    return actions