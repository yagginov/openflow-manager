import requests

class OpenFlowController:
    def __init__(self, controller_url, username, password):
        self.controller_url = controller_url
        self.auth = (username, password)

    def add_flow(self, node_id, flow_id, match, actions):
        url = f"{self.controller_url}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/0/flow/{flow_id}"
        flow_data = {
            "flow": [
                {
                    "id": flow_id,
                    "match": match,
                    "instructions": {
                        "instruction": [
                            {
                                "order": 0,
                                "apply-actions": {
                                    "action": actions
                                }
                            }
                        ]
                    },
                    "priority": 500,
                    "table_id": 0
                }
            ]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, json=flow_data, headers=headers, auth=self.auth)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Failed to add flow: {response.status_code}")

    def delete_flow(self, node_id, flow_id):
        url = f"{self.controller_url}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/0/flow/{flow_id}"
        response = requests.delete(url, auth=self.auth)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Failed to delete flow: {response.status_code}")