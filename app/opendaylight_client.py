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

def get_config_topology_details():
    """Retrieve OpenFlow topology details."""
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()


def get_config_flow_info(node_id, table_id, flow_id):
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}/"
    print(f"url for api: {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    return response.json()


def get_flow_ids(node_id, table_id):
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
    Створити новий flow на вказаному вузлі, таблиці та з flow_id.
    flow_data — це словник з усіма параметрами flow (відповідає структурі OpenFlow).
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
    Видалити flow з вказаного вузла, таблиці та flow_id.
    """
    url = f"{BASE_URL}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code in [200, 204]:
        return True
    else:
        raise Exception(f"Failed to delete flow: {response.status_code} {response.text}")