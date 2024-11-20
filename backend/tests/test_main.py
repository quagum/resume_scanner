from fastapi.testclient import TestClient
from ..main import app, tmp_database
import bcrypt
import os
from io import BytesIO
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
    email = register_payload_1["email"]
    assert email in tmp_database
    assert bcrypt.checkpw(register_payload_1["password"].encode('utf-8'), tmp_database[email].hashed_password)

def test_register_duplicate():
    clear_and_register_account(register_payload_1)
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

def test_successful_resume_upload():
    file_content = BytesIO(b"%PDF-1.4 This is a test PDF file.")
    response = client.post(
        "/api/resume-upload",
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Resume uploaded successfully."
    assert response.json()["status"] == "success"

def test_fail_resume_upload_invalid_file_type():
    file_content = BytesIO(b"This is not a valid PDF file.")
    response = client.post(
        "/api/resume-upload",
        files={"file": ("test.txt", file_content, "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid file type. Only PDF files are allowed."
    assert response.json()["status"] == "error"

def test_fail_resume_upload_oversized_file():
    oversized_file = BytesIO(b"A" * (2 * 1024 * 1024 * 1024 + 1))
    response = client.post(
        "/api/resume-upload",
        files={"file": ("large.pdf", oversized_file, "application/pdf")},
    )
    assert response.status_code == 400
    assert response.json()["error"] == "File size exceeds the 2GB limit."
    assert response.json()["status"] == "error"

def test_sucessful_job_description_upload():
    job_description_payload = {
        "job_description": "This is a test job description"
    }
    response = client.post(
        "/api/job-description",
        json=job_description_payload
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Job description submitted successfully."
    assert response.json()["status"] == "success"

def test_fail_job_description_upload_invalid_length():
    job_description_payload = {
        "job_description": "A"*5001
    }
    response = client.post(
        "/api/job-description",
        json=job_description_payload
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Job description exceeds character limit."
    assert response.json()["status"] == "error"