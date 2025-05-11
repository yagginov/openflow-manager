def prepare_graph_data(topology_details):
    """
    Готує дані для графа на основі деталей топології.
    """
    nodes = []
    edges = []
    unique_links = set()  # Множина для унікальних зв'язків
    unique_ports = {}

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

                if node.get("flow-node-inventory:name", 'N/A') != "N/A":
                    unique_ports[node['id']] = node.get("flow-node-inventory:name", 'N/A')

                # Додаємо зв'язок між свічем і комп'ютером
                edges.append({
                    "from": node["id"],
                    "to": computer_id,
                    "label": f"{connector.get('flow-node-inventory:name', 'N/A')}"
                })

    # Додаємо зв'язки між вузлами
    for link in topology_details.get("links", []):
        print(link, end='\n\n')
        # Формуємо унікальний ключ для зв'язку
        link_key = tuple(sorted([
            (link["source"]["source-node"], link["source"].get("source-tp", "N/A")),
            (link["destination"]["dest-node"], link["destination"].get("dest-tp", "N/A"))
        ]))

        if link_key not in unique_links:
            unique_links.add(link_key)  # Додаємо ключ до множини
            edges.append({
                "from": link["source"]["source-node"],
                "to": link["destination"]["dest-node"],
                "label": f"Port: {unique_ports.get(link['source']['source-tp'], 'N/A')} -> {unique_ports.get(link['destination']['dest-tp'], 'N/A')}"
            })

    return {"nodes": nodes, "edges": edges}