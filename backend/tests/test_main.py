from fastapi.testclient import TestClient
from ..database.models import User
from ..main import app, get_db
from unittest.mock import MagicMock
import pytest
import os
import jwt
import bcrypt
"""
Setup and helper
"""
client = TestClient(app)

mock_session = MagicMock()
def override_get_db():
    try:
        yield mock_session
    finally:
        pass
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def mock_db_session():
    return mock_session

register_payload_1 = {
    "email": "test@example.com",
    "password": "securePassword123",
    "username": "testuser"
}

"""
Tests
"""
def test_register_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.post("/api/register", json=register_payload_1)
    assert response.status_code == 201
    assert response.json() == {"message": "User registered"}

def test_register_duplicate(mock_db_session):
    existing_user = User(email="test@example.com", username="testuser", hashed_password="hashedpassword123")
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_user
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

def test_login_success(mock_db_session):
    mock_password = "hashedpassword123"
    mock_hashed_password = bcrypt.hashpw(mock_password.encode('utf-8'), bcrypt.gensalt())
    existing_user = User(email="test@example.com", username="testuser", hashed_password=mock_hashed_password)
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_user
    mock_db_session.users[existing_user.email].hashed_password = existing_user.hashed_password
    login_payload = {
            "email": "test@example.com",
            "password": "hashedpassword123"
    }
    response = client.post("/api/login", json=login_payload)
    secret = os.getenv('secret')
    algorithm = os.getenv('algorithm')
    assert response.status_code == 200
    data = response.json()
    generated_token = data["token"]
    decoded_token = jwt.decode(generated_token, secret, algorithms=[algorithm])
    assert decoded_token["email"] == login_payload["email"]

def test_login_fail(mock_db_session):
    mock_password = "hashedpassword123"
    mock_hashed_password = bcrypt.hashpw(mock_password.encode('utf-8'), bcrypt.gensalt())
    existing_user = User(email="test@example.com", username="testuser", hashed_password=mock_hashed_password)
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_user
    mock_db_session.users[existing_user.email].hashed_password = existing_user.hashed_password
    login_payload = {
            "email": "test@example.com",
            "password": "superWrongPassword123",
    }
    response = client.post("/api/login", json=login_payload)
    
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Email or password is not recognized"

def test_login_nonexistent_user(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    payload = {
        "email": "nonexistent@example.com", 
        "password": register_payload_1["password"]
    }
    response = client.post("/api/login", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Email or password is not recognized"