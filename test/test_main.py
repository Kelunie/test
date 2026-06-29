from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)

def test_health():
    # simular una peticion HTTP a la ruta /health
    response = cliente.get("/health")

    # validamos que el estado sea 200 (ok) y la respuesta sea la correcta
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}