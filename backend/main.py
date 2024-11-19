from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import os 
import bcrypt
import jwt
import datetime
from backend.user_models import User, RegisterPayload, LoginPayload

app = FastAPI()

tmp_database = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/register")
async def register(payload: RegisterPayload, response: Response):
    """
      Register account from the given payload.
      
      Args:
        payload (RegisterPayload): The payload containing email, password, username
        response (Response): The FastAPI Response object for setting the status code

      Returns:
        dict: A JSON response with a status message.
      """
    email = payload.email
    username = payload.username
    if email not in tmp_database:
        password = payload.password
        bytes = password.encode('utf-8') 
        salt = bcrypt.gensalt() 
        hashed_password = bcrypt.hashpw(bytes, salt) 
        user = User(email, username, hashed_password)
        tmp_database[email] = user
        response.status_code = status.HTTP_201_CREATED
        return {"message": "User registered"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Username or email already registered"}
  
@app.post("/api/login")
async def login(payload: LoginPayload, response: Response):
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
    if email in tmp_database and bcrypt.checkpw(password.encode('utf-8'), tmp_database[email].hashed_password):
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