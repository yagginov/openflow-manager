import requests
import json

# Load configuration from config.json
with open("app/config.json", "r") as config_file:
    config = json.load(config_file)

BASE_URL = config["BASE_URL"]
HEADERS = config["HEADERS"]

def get_topology_details():
    """Retrieve OpenFlow topology details."""
    url = f"{BASE_URL}/restconf/operational/opendaylight-inventory:nodes/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()

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

def get_port_description(node_id, port_id):
    """Retrieve port description and statistics."""
    url = f"{BASE_URL}/rests/data/opendaylight-inventory:nodes/node={node_id}/node-connector={port_id}?content=nonconfig"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_flow_table_statistics(node_id, table_id):
    """Retrieve flow table and aggregated statistics."""
    url = f"{BASE_URL}/rests/data/opendaylight-inventory:nodes/node={node_id}/table={table_id}?content=nonconfig"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_flow_statistics(node_id, table_id, flow_id):
    """Retrieve individual flow statistics."""
    url = f"{BASE_URL}/rests/data/opendaylight-inventory:nodes/node={node_id}/table={table_id}/flow={flow_id}?content=nonconfig"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_group_statistics(node_id, group_id):
    """Retrieve group description and statistics."""
    url = f"{BASE_URL}/rests/data/opendaylight-inventory:nodes/node={node_id}/group={group_id}?content=nonconfig"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_meter_statistics(node_id, meter_id):
    """Retrieve meter description and statistics."""
    url = f"{BASE_URL}/rests/data/opendaylight-inventory:nodes/node={node_id}/meter={meter_id}?content=nonconfig"
    response = requests.get(url, headers=HEADERS)
    return response.json()