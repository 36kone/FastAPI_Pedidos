from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KET = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACESS_TOKEN_EXPIRE_MINUTES'))

app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

from order_routes import order_router
from auth_routes import auth_router

app.include_router(order_router)
app.include_router(auth_router)
