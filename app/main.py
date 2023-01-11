from fastapi import Depends, FastAPI

from app.config.database import Base, engine
from app.middleware.error_handler import ErrorHandler
from app.middleware.jwt_bearer import JWTBearer
from app.routers.auth import auth_route
from app.routers.menu import menu_route
from app.routers.module import module_route
from app.routers.role import role_route
from app.routers.user import user_route
from app.routers.web import web_route


app = FastAPI()
app.title = 'Hipodromo Chile Single Sign-On'
app.version = '1.0.0'
app.description = 'API in charge of managing the SSO of Hipodromo Chile'

# Add Middleware
#app.add_middleware(ErrorHandler)


# Add routers
app.include_router(auth_route)
app.include_router(menu_route)
app.include_router(module_route)
app.include_router(role_route)
app.include_router(user_route)
app.include_router(web_route)
'''app.include_router(menu_route, dependencies=[Depends(JWTBearer())])
app.include_router(module_route, dependencies=[Depends(JWTBearer())])
app.include_router(role_route, dependencies=[Depends(JWTBearer())])
app.include_router(user_route, dependencies=[Depends(JWTBearer())])
app.include_router(web_route, dependencies=[Depends(JWTBearer())])'''


# When the app start, all the tables are created.
@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)
    # init_data()
