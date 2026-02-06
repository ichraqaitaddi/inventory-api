from flask import Flask, jsonify

app = Flask(__name__)

# Notre "base de données" temporaire [cite: 47, 48]
servers = [
    {"id": 1, "hostname": "web-prod-01", "ip": "10.0.0.1", "status": "up"},
    {"id": 2, "hostname": "db-prod-01", "ip": "10.0.0.2", "status": "down"}
]

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    # C'est ici qu'on répond au premier endpoint [cite: 39, 40]
    return jsonify({"status": "OK", "version": "1.0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/api/v1/servers', methods=['GET'])
def get_servers():
    # On prépare le dictionnaire avec la liste et le compte
    response = {
        "servers": servers,
        "count": len(servers)
    }
    # On transforme le tout en JSON
    return jsonify(response)

@app.route('/api/v1/servers/<int:server_id>', methods=['GET'])
def get_server(server_id):
    # On parcourt la liste pour trouver le bon ID
    for server in servers:
        if server["id"] == server_id:
            return jsonify(server)

    # Si on arrive ici, c'est que l'ID n'existe pas
    return jsonify({"error": "Server not found"}), 404
