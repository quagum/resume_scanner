from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import bcrypt

app = FastAPI()

tmp_database = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Payload model 
class RegisterPayload(BaseModel):
    email: str
    password: str
    username: str

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
    id = (email, username)
    if id not in tmp_database:
        password = payload.password
        bytes = password.encode('utf-8') 
        salt = bcrypt.gensalt() 
        hashed_password = bcrypt.hashpw(bytes, salt) 
        tmp_database[id] = hashed_password
        response.status_code = status.HTTP_201_CREATED
        return {"message": "User registered"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Username or email already registered"}