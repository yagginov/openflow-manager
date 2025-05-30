# SDN OpenFlow Network Manager

This project is a Python-based web application for managing and monitoring Software-Defined Networking (SDN) environments using the OpenFlow protocol. It provides a user-friendly interface for visualizing network topology, managing OpenFlow rules (flows), and analyzing network statistics in real time.

## Features

- **Network Topology Visualization**  
  Interactive visualization of the SDN network topology, including switches and connected hosts, using vis.js.

- **Flow Management**  
  - View all configured OpenFlow flows in the network.
  - Create new flow entries with detailed match and action fields.
  - Edit existing flows.
  - Delete flows from the network.

- **Statistics and Monitoring**  
  - View real-time flow statistics (bytes, packets, duration).
  - View flow table statistics (active flows, packets looked up/matched).
  - View aggregate statistics for flow tables.
  - View port statistics (bytes, packets, errors, drops, etc.).

- **Custom Flow Entry Builder**  
  Flexible form for specifying match fields (IP, MAC, VLAN, TCP/UDP ports, etc.) and actions (output, drop, set fields, VLAN operations, queue assignment).

- **REST API Integration**  
  Communicates with an OpenDaylight controller via RESTCONF API for all management and monitoring operations.

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, Jinja2, CSS (SCSS), JavaScript (vis.js, DataTables)
- **SDN Controller:** OpenDaylight (RESTCONF API)
- **Other:** pandas (for tabular statistics), requests

## Getting Started

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Configure OpenDaylight connection:**
   Edit [`app/config.json`](app/config.json) with your OpenDaylight controller's URL and credentials.

3. **Run the application:**
   ```
   python -m web.server
   ```

   Or
   ```
   python3 -m web.server
   ```

   Or use Docker Compose:
   ```
   docker-compose up --build
   ```

4. **Access the web UI:**  
   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Project Structure

- `app/` – Core backend logic (OpenDaylight client, monitoring, controller, utilities)
- `web/` – Flask web server, templates, static files
- `docker/` – Dockerfile and entrypoint
- `requirements.txt` – Python dependencies

## Notes

- Requires a running OpenDaylight controller with RESTCONF enabled.
- All flow and statistics operations are performed live via the controller's REST API.

---

© 2025 SDN OpenFlow Network Manager