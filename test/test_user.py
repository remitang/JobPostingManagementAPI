import pytest
from fastapi.testclient import TestClient
from app.main import app 
import requests

client = TestClient(app)

BASE_URL = "http://127.0.0.1:8000"


def test_register_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "id" in response.json(), "Response JSON does not contain 'id'"
    assert "email" in response.json(), "Response JSON does not contain 'email'"


def test_register_same_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    json_response = response.json()
    print(json_response)
    assert json_response["detail"] == "Email already registered"


def test_login_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = requests.post(f"{BASE_URL}/users/login", json=user_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "access" in response.json(), "Response JSON does not contain 'access_token'"
    assert "token_type" in response.json(), "Response JSON does not contain 'token_type'"


def test_login_user_me():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = requests.post(f"{BASE_URL}/users/login", json=user_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    access_token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "id" in response.json(), "Response JSON does not contain 'id'"
    assert "role" in response.json(), "Response JSON does not contain 'role'"
    assert "address" in response.json(), "Response JSON does not contain 'address'"
    assert "cv" in response.json(), "Response JSON does not contain 'cv'"
    assert "name" in response.json(), "Response JSON does not contain 'name'"
    assert "email" in response.json(), "Response JSON does not contain 'email'"
    assert "telephone" in response.json(), "Response JSON does not contain 'telephone'"
    assert "creation_date" in response.json(), "Response JSON does not contain 'creation_date'"

def test_delete_user():

    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = requests.post(f"{BASE_URL}/users/login", json=user_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    access_token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "id" in response.json(), "Response JSON does not contain 'id'"
    user_id = response.json()["id"]

    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code == 204, f"Expected status code 204, got {response.status_code}"

    