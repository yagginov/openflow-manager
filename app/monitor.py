from app.opendaylight_client import (
    get_topology_details,
    get_topology_links,
    get_config_topology_details,
    get_config_flow_info
)
import pandas as pd

class OpenFlowMonitor:
    def __init__(self):
        pass  # Configuration is loaded in opendaylight_client

    def get_full_topology(self):
        """Get complete network topology information, including links."""
        try:
            topology_details = get_topology_details()
            topology_links = get_topology_links()
            topology_details["links"] = topology_links.get("network-topology", {}).get("topology", [])[0].get("link", [])
            return topology_details
        except Exception as e:
            raise Exception(f"Failed to fetch full topology: {e}")
        
    def get_nodes(self):
        topology_details = self.get_full_topology()
        nodes = topology_details.get("nodes", {}).get("node", {})
        return nodes
    
    def get_config_nodes(self):
        topology_details = get_config_topology_details()
        nodes = topology_details.get("nodes", {}).get("node", {})
        return nodes

    def get_flow_statistics(self):
        """Return statistics for all flows in the network."""
        nodes = self.get_nodes()
        flow_statistics = []

        for node in nodes:
            node_id = node["id"]
            hardware = node["flow-node-inventory:hardware"]

            for table_element in node.get("flow-node-inventory:table", []):
                for stat in table_element.get("flow", []):
                    table_id = stat.get("table_id", -1)
                    flow_id = stat.get("id", "N/A")
                    
                    flow_stat = stat.get("opendaylight-flow-statistics:flow-statistics", {})
                    byte_count = flow_stat.get("byte-count", -1)
                    packet_count = flow_stat.get("packet-count", -1)
                    
                    duration = flow_stat.get("duration", {})
                    duration_nanosecond = duration.get("nanosecond", -1)
                    duration_second = duration.get("second", -1)
                    flow_statistics.append((node_id, hardware, table_id, flow_id, byte_count, packet_count, duration_nanosecond, duration_second))

        columns = [
            "Node ID", "Hardware", "Table ID", "Flow ID", 
            "Byte Count", "Packet Count", "Duration (ns)", "Duration (s)"
        ]
        flow_statistics_df = pd.DataFrame(flow_statistics, columns=columns)
        return flow_statistics_df
    
    def get_flow_table_statistics(self):
        """Return statistics for all flow tables in the network."""
        nodes = self.get_nodes()
        flow_table_statistics = []

        for node in nodes:
            node_id = node["id"]
            hardware = node["flow-node-inventory:hardware"]

            for table_element in node.get("flow-node-inventory:table", []):
                stat = table_element.get("opendaylight-flow-table-statistics:flow-table-statistics", {})
                if len(stat):
                    table_id = table_element.get("id", -1)
                    active_flows = stat.get("active-flows", -1)
                    packets_looked_up = stat.get("packets-looked-up", -1)
                    packets_matched = stat.get("packets-matched", -1)

                    flow_table_statistics.append((node_id, hardware, table_id, active_flows, packets_looked_up, packets_matched))
        
        columns = ["Node ID", "Hardware", "Table ID", "Active Flows", "Packets Looked Up", "Packets Matched"]
        flow_table_statistics_df = pd.DataFrame(flow_table_statistics, columns=columns)
        return flow_table_statistics_df

    def get_aggregate_flow_statistics(self):
        """Return aggregate statistics for all flow tables."""
        nodes = self.get_nodes()
        aggregate_flow_statistics = []

        for node in nodes:
            node_id = node["id"]
            hardware = node["flow-node-inventory:hardware"]

            for table_element in node.get("flow-node-inventory:table", []):
                stat = table_element.get("opendaylight-flow-statistics:aggregate-flow-statistics", {})
                if len(stat):
                    table_id = table_element.get("id", -1)
                    byte_count = stat.get("byte-count", -1)
                    flow_count = stat.get("flow-count", -1)
                    packet_count = stat.get("packet-count", -1)

                    aggregate_flow_statistics.append((node_id, hardware, table_id, byte_count, flow_count, packet_count))
        
        columns = ["Node ID", "Hardware", "Table ID", "Byte Count", "Flow Count", "Packet Count"]
        aggregate_flow_statistics_df = pd.DataFrame(aggregate_flow_statistics, columns=columns)
        return aggregate_flow_statistics_df

    def get_ports_statistics(self):
        """Return statistics for all ports in the network."""
        nodes = self.get_nodes()
        ports_statistics = []

        for node in nodes:
            node_id = node["id"]
            hardware = node["flow-node-inventory:hardware"]

            for port_info in node.get("node-connector", []):
                port_id = port_info.get("id", "N/A")
                port_name = port_info.get("flow-node-inventory:name", "N/A")
                
                stat = port_info.get("opendaylight-port-statistics:flow-capable-node-connector-statistics", {})
                bytes = stat.get("bytes", {})
                bytes_received = bytes.get("received", -1)
                bytes_transmitted = bytes.get("transmitted", -1)

                duration = stat.get("duration", {})
                duration_nanosecond = duration.get("nanosecond", -1)
                duration_second = duration.get("second", -1)

                packets = stat.get("packets", {})
                packets_received = packets.get("received", -1)
                packets_transmitted = packets.get("transmitted", -1)

                collision_count = stat.get("collision-count", -1)
                receieve_crc_error = stat.get("receive-crc-error", -1)
                receieve_drops = stat.get("receive-drops", -1)
                receieve_errors = stat.get("receive-errors", -1)
                receieve_frame_error = stat.get("receive-frame-error", -1)
                receieve_over_run_error = stat.get("receive-over-run-error", -1)
                transmit_drops = stat.get("transmit-drops", -1)
                transmit_errors = stat.get("transmit-errors", -1)

                ports_statistics.append((
                    node_id, hardware, port_id, port_name, bytes_received, bytes_transmitted, collision_count, 
                    duration_nanosecond, duration_second, packets_received, packets_transmitted, receieve_crc_error, 
                    receieve_drops, receieve_errors, receieve_frame_error, receieve_over_run_error, transmit_drops, transmit_errors
                ))
        
        columns = [
            "Node ID", "Hardware", "Port ID", "Port Name", "Bytes Received", "Bytes Transmitted", "Collision Count",
            "Duration (ns)", "Duration (s)", "Packets Received", "Packets Transmitted", "Receive CRC Error",
            "Receive Drops", "Receive Errors", "Receive Frame Error", "Receive Overrun Error", "Transmit Drops", "Transmit Errors"
        ]
        ports_statistics_df = pd.DataFrame(ports_statistics, columns=columns)
        return ports_statistics_df
    

    def get_flows(self):
        """Return all flows from the configuration datastore."""
        nodes = self.get_config_nodes()
        flows_data = []
        for node in nodes:
            node_id = node["id"]
            for table in node.get("flow-node-inventory:table", []):
                table_id = table["id"]
                for flow in table.get("flow", []):
                    flow_id = flow["id"]
                    priority = flow.get("priority", "")
                    flows_data.append([
                        node_id, table_id, flow_id, priority, "", ""
                    ])

        columns = ["Node ID", "Table ID", "Flow ID", "Priority", "Edit", "Delete"]

        flows_df = pd.DataFrame(flows_data, columns=columns)
        return flows_df
    
    def get_flow_info(self, node_id, table_id, flow_id):
        """Return detailed information about a specific flow for form usage."""
        data = get_config_flow_info(node_id, table_id, flow_id)
        
        if not data or "flow-node-inventory:flow" not in data:
            return None

        flow = data["flow-node-inventory:flow"][0]

        flow_info = {
            "id": flow.get("id", ""),
            "priority": flow.get("priority", ""),
            "table_id": flow.get("table_id", ""),

            # Match fields
            "match_in_port": flow.get("match", {}).get("in-port", ""),
            "match_eth_type": flow.get("match", {}).get("ethernet-match", {}).get("ethernet-type", {}).get("type", ""),
            "match_ipv4_src": flow.get("match", {}).get("ipv4-source", ""),
            "match_ipv4_dst": flow.get("match", {}).get("ipv4-destination", ""),

            # Actions
            "action_output": "",
            "action_drop": False,
            "action_set_ipv4_src": ""
        }

        instructions = flow.get("instructions", {}).get("instruction", [])
        for instruction in instructions:
            apply_actions = instruction.get("apply-actions", {}).get("action", [])
            for action in apply_actions:
                if "output-action" in action:
                    flow_info["action_output"] = action["output-action"].get("output-node-connector", "")
                elif "drop-action" in action:
                    flow_info["action_drop"] = True
                elif "set-field" in action:
                    set_field = action["set-field"]
                    if "ipv4-source" in set_field:
                        flow_info["action_set_ipv4_src"] = set_field["ipv4-source"]

        return flow_info

    def get_json_flow_info(self, node_id, table_id, flow_id):
        """Return raw JSON information about a specific flow."""
        return get_config_flow_info(node_id, table_id, flow_id)
