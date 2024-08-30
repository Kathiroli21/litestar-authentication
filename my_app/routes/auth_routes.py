from litestar import post, Request, Response
from litestar.exceptions import ValidationException, NotAuthorizedException,InternalServerException
from pydantic import BaseModel
from sqlalchemy.future import select
from my_app.db.models import User
from my_app.db.session import get_session
from my_app.security.jwt import encode_jwt_token
from ..security.password import hash_password, verify_password
import logging


logger = logging.getLogger(__name__)

class UserCreate(BaseModel):
    username: str
    password: str
@post("/register")
async def register(data: UserCreate, request: Request) -> Response:
    try:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.username == data.username))
            existing_user = result.scalars().first()
            if existing_user:
                raise ValidationException(detail="Username already taken")
            
            user = User(username=data.username, hashed_password=hash_password(data.password))
            session.add(user)
            await session.commit()

        return Response({"message": "User created successfully"}, media_type="application/json")

    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise InternalServerException(status_code=500, detail="Internal Server Error")


@post("/login")
async def login(data: UserCreate, request: Request) -> Response:
    try:
        async with get_session() as session:
            logger.info(f"Attempting login for user: {data.username}")
            result = await session.execute(select(User).where(User.username == data.username))
            user = result.scalars().first()
            
            if not user:
                logger.warning(f"Login attempt failed: Username not found ({data.username})")
                raise NotAuthorizedException("Invalid credentials")

            if not verify_password(data.password, user.hashed_password):
                logger.warning(f"Login attempt failed: Incorrect password for username ({data.username})")
                raise NotAuthorizedException("Invalid credentials")
            
            token = encode_jwt_token(user_id=str(user.id))  
            logger.debug(f"Generated token: {token}")  

            user_id_str = str(user.id)
            response_data = {
                "token": token,
                "user_id": user_id_str
            }
            logger.debug(f"Response data: {response_data}")  

            logger.info(f"Login successful for user: {data.username}")
            return Response(content=response_data, media_type="application/json")
    
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise InternalServerException(status_code=500, detail="Internal Server Error")