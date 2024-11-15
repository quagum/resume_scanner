from fastapi.testclient import TestClient
from ..main import app, tmp_database
import bcrypt

client = TestClient(app)

def test_register_success():
    tmp_database.clear()
    
    payload = {
        "email": "test@example.com",
        "password": "securePassword123",
        "username": "testuser"
    }
    
    response = client.post("/api/register", json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "User registered"}
    
    # Verify password is hashed
    entry = (payload["email"], payload["username"])
    assert entry in tmp_database
    assert bcrypt.checkpw(payload["password"].encode('utf-8'), tmp_database[entry])

def test_register_duplicate():
    tmp_database.clear()

    payload = {
        "email": "duplicate@example.com",
        "password": "password123",
        "username": "duplicateuser"
    }
    tmp_database[(payload["email"], payload["username"])] = bcrypt.hashpw(payload["password"].encode('utf-8'), bcrypt.gensalt())

    # Attempt to register the same entry
    response = client.post("/api/register", json=payload)
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
