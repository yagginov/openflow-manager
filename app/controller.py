import requests
import json

# Load configuration from config.json (як у monitor.py)
with open("app/config.json", "r") as config_file:
    config = json.load(config_file)

BASE_URL = config["BASE_URL"]
HEADERS = config["HEADERS"]

class OpenFlowController:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def create_flow(self, node_id, table_id, flow_id, flow_data):
        """
        Створити новий flow на вказаному вузлі, таблиці та з flow_id.
        flow_data — це словник з усіма параметрами flow (відповідає структурі OpenFlow).
        """
        url = f"{self.base_url}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
        response = requests.put(url, json=flow_data, headers=self.headers)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to create flow: {response.status_code} {response.text}")

    def delete_flow(self, node_id, table_id, flow_id):
        """
        Видалити flow з вказаного вузла, таблиці та flow_id.
        """
        url = f"{self.base_url}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Failed to delete flow: {response.status_code} {response.text}")