from app.opendaylight_client import (
    get_flow_table_statistics,
    get_port_description,
    get_topology_details,
    get_topology_links,  # Import the new function
)

class OpenFlowMonitor:
    def __init__(self):
        pass  # Конфігурація вже завантажується в opendaylight_client

    def get_flow_stats(self, node_id=1, table_id=1):
        """Отримати статистику потоків для конкретного вузла та таблиці."""
        try:
            return get_flow_table_statistics(node_id, table_id)
        except Exception as e:
            raise Exception(f"Failed to fetch flow stats: {e}")

    def get_port_stats(self, node_id, port_id):
        """Отримати статистику портів для конкретного вузла та порту."""
        try:
            return get_port_description(node_id, port_id)
        except Exception as e:
            raise Exception(f"Failed to fetch port stats: {e}")

    def get_topology(self):
        """Отримати інформацію про топологію мережі."""
        try:
            return get_topology_details()
        except Exception as e:
            raise Exception(f"Failed to fetch topology details: {e}")

    def get_full_topology(self):
        """Отримати повну інформацію про топологію мережі, включаючи зв'язки."""
        try:
            topology_details = get_topology_details()
            topology_links = get_topology_links()
            topology_details["links"] = topology_links.get("network-topology", {}).get("topology", [])[0].get("link", [])
            return topology_details
        except Exception as e:
            raise Exception(f"Failed to fetch full topology: {e}")