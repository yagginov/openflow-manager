import requests
import json

# Load configuration from config.json
with open("app/config.json", "r") as config_file:
    config = json.load(config_file)

BASE_URL = config["BASE_URL"]
HEADERS = config["HEADERS"]

def get_topology_details():
    """Retrieve operational OpenFlow topology details."""
    url = f"{BASE_URL}/restconf/operational/opendaylight-inventory:nodes/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()

def get_config_topology_details():
    """Retrieve configuration OpenFlow topology details."""
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()

def get_config_flow_info(node_id, table_id, flow_id):
    """Get flow configuration for a specific node, table, and flow."""
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()

def get_flow_ids(node_id, table_id):
    """Get all flow IDs from a specific node and table."""
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    data = response.json()
    flows = data.get("flow-node-inventory:table", [])[0].get("flow", [])
    return [flow["id"] for flow in flows]

def get_topology_links():
    """Retrieve links between nodes in the topology."""
    url = f"{BASE_URL}/restconf/operational/network-topology:network-topology/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()

def get_node_inventory(node_id):
    """Retrieve inventory data of a connected node."""
    url = f"{BASE_URL}/rests/data/opendaylight-inventory:nodes/node={node_id}?content=nonconfig"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def create_flow(node_id, table_id, flow_id, flow_data):
    """
    Create a new flow on the specified node, table, and flow_id.
    flow_data should be a dictionary matching the OpenFlow structure.
    """
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
    response = requests.put(url, json=flow_data, headers=HEADERS)
    if response.status_code in [200, 201]:
        if response.text and response.text.strip():
            return response.json()
        else:
            return True
    else:
        raise Exception(f"Failed to create flow: {response.status_code} {response.text}")

def delete_flow(node_id, table_id, flow_id):
    """
    Delete a flow from the specified node, table, and flow_id.
    """
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code in [200, 204]:
        return True
    else:
        raise Exception(f"Failed to delete flow: {response.status_code} {response.text}")