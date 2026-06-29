from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from src.middleware.auth_middleware import verify_token

client = TestClient(app)

# Función simulada que devuelve los datos del token JWT decodificado
def override_verify_token():
    return {
        "id": "admin-id-123",
        "role": "admin",
        "mustChangePassword": False
    }

@patch('src.modules.users.users_router.users_service')
def test_get_subjects_como_admin(mock_users_service):
    # Sobrescribimos la dependencia original con nuestro mock de token
    app.dependency_overrides[verify_token] = override_verify_token
    
    # Simulamos la lista de materias devuelta por el servicio
    mock_users_service.get_subjects.return_value = [
        {"id": "1", "name": "Matemáticas", "code": "MAT-101"},
        {"id": "2", "name": "Español", "code": "ESP-101"}
    ]
    
    # Hacemos la petición GET protegida
    response = client.get("/api/v1/users/subjects", headers={"Authorization": "Bearer token-falso"})
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Matemáticas"
    
    # Limpiamos las dependencias sobrescritas para no afectar otros tests
    app.dependency_overrides.clear()

    # new push