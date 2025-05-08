def prepare_graph_data(topology_details):
    """
    Готує дані для графа на основі деталей топології.
    """
    nodes = []
    edges = []

    for node in topology_details["nodes"]["node"]:
        # Додаємо вузол для свіча
        nodes.append({
            "id": node["id"],
            "label": node["id"],
            "title": f"Hardware: {node.get('flow-node-inventory:hardware', 'N/A')}<br>IP: {node.get('flow-node-inventory:ip-address', 'N/A')}",
            "group": "switch"  # Група для стилізації
        })

        # Обробляємо порти
        for connector in node.get("node-connector", []):
            # Додаємо вузли для комп'ютерів, підключених до порту
            for address in connector.get("address-tracker:addresses", []):
                computer_id = f"{node['id']}-{address['mac']}"  # Унікальний ID для комп'ютера
                nodes.append({
                    "id": computer_id,
                    "label": address["ip"],
                    "title": f"MAC: {address['mac']}<br>IP: {address['ip']}",
                    "group": "computer"  # Група для стилізації
                })

                # Додаємо зв'язок між свічем і комп'ютером
                edges.append({
                    "from": node["id"],
                    "to": computer_id,
                    "label": f"{connector.get('flow-node-inventory:name', 'N/A')}"
                })

    return {"nodes": nodes, "edges": edges}