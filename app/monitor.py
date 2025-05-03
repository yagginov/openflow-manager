import requests

class OpenFlowMonitor:
    def __init__(self, controller_url, username, password):
        self.controller_url = controller_url
        self.auth = (username, password)

    def get_flow_stats(self):
        url = f"{self.controller_url}/restconf/operational/opendaylight-inventory:nodes/"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch flow stats: {response.status_code}")

    def get_port_stats(self, node_id):
        url = f"{self.controller_url}/restconf/operational/opendaylight-inventory:nodes/node/{node_id}/node-connector/"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch port stats: {response.status_code}")