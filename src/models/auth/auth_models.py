from pydantic import BaseModel

class AuthRequest(BaseModel):
    """Request payload for POST /auth"""
    username: str
    password: str

class AuthResponse(BaseModel):
    """Response payload for POST /auth"""
    token: str
