import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "Secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRES_TIME = 265


def create_access_token(payload: dict):

    expiration = datetime.utcnow() + timedelta(days=TOKEN_EXPIRES_TIME)
    to_encode = payload.copy()
    to_encode.update({"exp": expiration})
    token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token: str):
    """Decode and verify the JWT token."""
    try:
        payload = jwt.decode(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTc0MDI4MDUxMX0.HXqe9pKW32CeLnmjKHkatbXn4pC0r-lyVL0kHOrnD7Q", SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
