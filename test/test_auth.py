from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 1. prueba de inicio de session exitoso

@patch('src.modules.auth.auth_router.auth_service')
def test_login_success(mock_auth_service):
    #somulamos la respuesta exitosa del servicio
    mock_auth_service.login.return_value = {
        "token": "token-falso-jwt",
        "mustChangePassword": False,
        "role": "admin",
        "first_name": "Usuario",
        "last_name": "Prueba"
    }
    # simulamos la peticion de login
    payload = {
        "id_number": "admin",
        "password": "admin1234"
    }

    # hacemos la peticion al endpoint de login
    response = client.post("/api/v1/auth/login", json=payload)

    # validamos que nos devuelva la informacion que ocupamos
    assert response.status_code == 200
    assert response.json()["token"] == "token-falso-jwt"
    mock_auth_service.login.assert_called_once_with("admin", "admin1234")

    # 2. Prueba de inicio de sesión fallido
@patch('src.modules.auth.auth_router.auth_service')
def test_login_fallido(mock_auth_service):
    # Simulamos que el servicio lanza un error de credenciales
    mock_auth_service.login.side_effect = ValueError("Invalid credentials")
    
    payload = {
        "id_number": "admin",
        "password": "passwordIncorrecto"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"