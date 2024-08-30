from datetime import datetime, timedelta
from uuid import UUID
from jose import JWTError, jwt
from pydantic import UUID4, BaseModel
from litestar.exceptions import NotAuthorizedException
from my_app.config import settings

DEFAULT_TIME_DELTA = timedelta(days=1)
ALGORITHM = "HS256"

class Token(BaseModel):
    exp: datetime
    iat: datetime
    sub: str

def decode_jwt_token(encoded_token: str) -> Token:
    try:
        
        payload = jwt.decode(encoded_token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        
        
        if 'sub' in payload:
            payload['sub'] = UUID(payload['sub'])
        
        
        return Token(**payload)
    except JWTError as e:
        raise NotAuthorizedException("Invalid token") from e
    except ValueError as e:
        
        raise NotAuthorizedException("Invalid token payload") from e

def encode_jwt_token(user_id: UUID, expiration: timedelta = DEFAULT_TIME_DELTA) -> str:
    token = Token(
        exp=datetime.utcnow() + expiration,
        iat=datetime.utcnow(),
        sub=str(user_id)  
    )
    return jwt.encode(token.dict(), settings.JWT_SECRET, algorithm=ALGORITHM)