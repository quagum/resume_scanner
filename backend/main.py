from fastapi import FastAPI, Response, status, UploadFile, Depends
#from pydantic import BaseModel
import os 
import io 
import bcrypt
import jwt
import datetime
from database import models
from user_models import RegisterPayload, LoginPayload

resume_file_content = io.BytesIO()

app = FastAPI()

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/register")
async def register(payload: RegisterPayload, response: Response, db: Session = Depends(get_db)):
    """
      Register account from the given payload.
      
      Args:
        payload (RegisterPayload): The payload containing email, password, username
        response (Response): The FastAPI Response object for setting the status code
        db (Session): A database connection?
      Returns:
        dict: A JSON response with a status message.
      """
    email = payload.email
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return {"error": "Username or email already registered"}
    else:
      username = payload.username
      password = payload.password
      bytes = password.encode('utf-8') 
      salt = bcrypt.gensalt() 
      hashed_password = bcrypt.hashpw(bytes, salt) 
      user = models.User(email=email, username=username, hashed_password=hashed_password)
      db.add(user)
      db.commit()
      response.status_code = status.HTTP_201_CREATED
      return {"message": "User registered"}
  
@app.post("/api/login")
async def login(payload: LoginPayload, response: Response, db: Session = Depends(get_db)):
    """
      Register account from the given payload.
      
      Args:
        payload (LoginPayload): The payload containing email, password
        response (Response): The FastAPI Response object for setting the status code

      Returns:
        dict: A JSON response with token if succesful otherwise a status message.
      """
    email = payload.email
    password = payload.password
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user and bcrypt.checkpw(password.encode('utf-8'), db.users[email].hashed_password):
      secret = os.getenv('secret')
      algorithm = os.getenv('algorithm')
      payload = {
          "email" : email,
          "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
      }
      jwt_token = jwt.encode(payload, secret, algorithm)
      response.status_code = status.HTTP_200_OK
      return {"token": jwt_token}
    else:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return {"error": "Email or password is not recognized"}

@app.post("/api/resume-upload")
async def resume_upload(file: UploadFile, response: Response):
    max_file_size = 2 * 1024 * 1024 * 1024
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type in allowed_types:
      file_size = 0
      chunk_size = 1024 * 1024
      while chunk := await file.read(chunk_size):
          resume_file_content.write(chunk)
          file_size += len(chunk)
          if file_size > max_file_size:
              response.status_code = status.HTTP_400_BAD_REQUEST
              return {
                  "error": "File size exceeds the 2GB limit.",
                  "status": "error"
              }
      resume_file_content.seek(0)
      response.status_code = status.HTTP_200_OK
      return {
          "message": "Resume uploaded successfully.",
          "status": "success"
        }
    else:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return {
        "error": "Invalid file type. Only PDF files are allowed.",
        "status": "error"
        }
      
@app.post("/api/job-description")
async def job_description_upload(payload: JobDescriptionPayload, response: Response):
  job_description = payload.job_description
  job_description.strip()
  max_char_count = 5000
  if len(job_description) <= max_char_count:
    response.status_code = status.HTTP_200_OK
    return {
      "message": "Job description submitted successfully.",
      "status": "success"
    }
  else:
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {
      "error": "Job description exceeds character limit.",
      "status": "error"
    }

