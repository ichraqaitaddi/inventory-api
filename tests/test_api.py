import pytest
from app.main import app

@pytest.fixture
def client():
    # On crée un client de test Flask
    return app.test_client()

def test_health_check(client):
    # On appelle la route
    response = client.get('/api/v1/health')
    # On vérifie que le code de statut est 200
    assert response.status_code == 200
    # On vérifie le contenu du JSON
    assert response.get_json() == {"status": "OK", "version": "1.0"}

def test_get_server_not_found(client):
    # On demande un ID qui n'existe pas (ex: 999)
    response = client.get('/api/v1/servers/999')

    # On vérifie que le code est 404
    assert response.status_code == 404

    # On vérifie le message d'erreur
    assert response.get_json()["error"] == "Server not found"

def test_get_all_servers(client):
    response = client.get('/api/v1/servers')
    assert response.status_code == 200
    data = response.get_json()
    assert "servers" in data
    assert data["count"] == 2


def test_get_single_server(client):
    # On cible l'ID 1 qui existe dans notre liste
    response = client.get('/api/v1/servers/1')
    assert response.status_code == 200

    data = response.get_json()
    # On vérifie que c'est bien le bon serveur
    assert data["id"] == 1
    assert data["hostname"] == "web-prod-01"