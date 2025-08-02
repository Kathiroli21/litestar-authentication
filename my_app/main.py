from litestar import Litestar
from litestar.middleware.base import DefineMiddleware
from my_app.security.authentication_middleware import JWTAuthenticationMiddleware
from my_app.routes.auth_routes import register, login

auth_middleware = DefineMiddleware(JWTAuthenticationMiddleware, exclude=["/register", "/login"])

app = Litestar(route_handlers=[register, login], middleware=[auth_middleware])

