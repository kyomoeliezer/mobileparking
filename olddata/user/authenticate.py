from ninja import Router
from .auth_token import *
from user import schemas
from typing import List

api = Router()


@api.post("/login", response=schemas.Token)
def login(request, loginSchema: schemas.UserAuthenticate):
    print(request.body)
    return Auth.authenticate_user(request, loginSchema)


@api.post("/login-confirm-devide-id", response=schemas.TokenWithDevice)
def login_confirm_devide_id(request, loginSchema: schemas.UserAuthenticate2):
    print(request.body)
    return Auth.authenticate_user_with_deviceId(request, loginSchema)


@api.post("/authenticate", response=schemas.UserSchema)
def authenticate(request, token: str):
    return Auth.authenticate_request(request, token)
