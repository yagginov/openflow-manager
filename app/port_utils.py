import re

def sort_ports_by_name(ports):
    """
    Сортує порти за числовою частиною імені.
    """
    def extract_number(port_name):
        match = re.search(r'\d+', port_name)
        return int(match.group()) if match else float('inf')  # Якщо немає числа, ставимо "безкінечність"
    
    return sorted(ports, key=lambda port: extract_number(port.get("flow-node-inventory:name", "")))