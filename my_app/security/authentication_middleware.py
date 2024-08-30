from typing import TYPE_CHECKING, cast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from my_app.db.models import User
from my_app.security.jwt import decode_jwt_token

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

API_KEY_HEADER = "X-API-KEY"

class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        # Skip authentication for the registration and login routes
        if connection.url.path in ["/register", "/login"]:
            return AuthenticationResult(user=None, auth=None)

        auth_header = connection.headers.get(API_KEY_HEADER)
        if not auth_header:
            raise NotAuthorizedException()

        token = decode_jwt_token(encoded_token=auth_header)
        engine = cast("AsyncEngine", connection.app.state.db_engine)
        
        async with AsyncSession(engine) as session:
            result = await session.execute(select(User).where(User.id == token.sub))
            user = result.scalars().first()
        
        if not user:
            raise NotAuthorizedException()
        
        return AuthenticationResult(user=user, auth=token)
