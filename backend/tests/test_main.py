from fastapi.testclient import TestClient
from ..main import app, tmp_database
import bcrypt
import os
import jwt

"""
SETUP AND HELPERS
"""
client = TestClient(app)

register_payload_1 = {
        "email": "test@example.com",
        "password": "securePassword123",
        "username": "testuser"
    }

def clear_and_register_account(payload):
    tmp_database.clear()
    client.post("/api/register", json=payload)    

"""
TESTS
"""

def test_register_success():
    tmp_database.clear()
    
    response = client.post("/api/register", json=register_payload_1)
    assert response.status_code == 201
    assert response.json() == {"message": "User registered"}
    
    # Verify password is hashed
    email = register_payload_1["email"]
    assert email in tmp_database
    assert bcrypt.checkpw(register_payload_1["password"].encode('utf-8'), tmp_database[email].hashed_password)

def test_register_duplicate():
    clear_and_register_account(register_payload_1)
    
    # Attempt to register the same entry
    client.post("/api/register", json=register_payload_1)
    response = client.post("/api/register", json=register_payload_1)
    assert response.status_code == 400
    assert response.json() == {"error": "Username or email already registered"}

def test_register_missing_field():
    payload = {
        "email": "incomplete@example.com",
        "password": "pass123"
        # Missing "username" field
    }
    
    response = client.post("/api/register", json=payload)
    assert response.status_code == 422  # Unprocessable Entity for validation error

def test_login_success():
    clear_and_register_account(register_payload_1)

    login_payload = {
            "email": register_payload_1["email"],
            "password": register_payload_1["password"],
    }
    response = client.post("/api/login", json=login_payload)
    
    secret = os.getenv('secret')
    algorithm = os.getenv('algorithm')

    assert response.status_code == 200
    data = response.json()
    generated_token = data["token"]
    decoded_token = jwt.decode(generated_token, secret, algorithms=[algorithm])
    assert decoded_token["email"] == login_payload["email"]

def test_login_fail():
    clear_and_register_account(register_payload_1)

    login_payload = {
            "email": register_payload_1["email"],
            "password": "superWrongPassword123",
    }
    response = client.post("/api/login", json=login_payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Email or password is not recognized"

def test_login_nonexistent_user():

    payload = {
        "email": "nonexistent@example.com", 
        "password": register_payload_1["password"]
    }
    response = client.post("/api/login", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Email or password is not recognized"