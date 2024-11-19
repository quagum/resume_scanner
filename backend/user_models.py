from pydantic import BaseModel

class User:
  def __init__(self, email, username, hashed_password):
    self.email = email
    self.username = username
    self.hashed_password = hashed_password
  
class BaseUserPayload(BaseModel):
    email: str
    password: str

class RegisterPayload(BaseUserPayload):
    username: str

class LoginPayload(BaseUserPayload):
    pass
