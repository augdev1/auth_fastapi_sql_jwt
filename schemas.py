from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TwoFactorLogin(BaseModel):
    temp_token: str
    code: str

class LogCreate(BaseModel):
    action: str

class TOTPVerify(BaseModel):
    code: str

class TOTPSetupResponse(BaseModel):
    secret: str
    qr_code_base64: str
    otpauth_url: str
