from user.models import  User
from ninja.orm import create_schema
from ninja import Schema

UserSchema = create_schema(User)
CreateUserSchema = create_schema(
    User, exclude=["id", "date_joined", "last_login", "groups", "user_permissions"]
)

UpdateUserSchema = create_schema(
    User, exclude=["date_joined", "last_login", "groups", "user_permissions"]
)


class Token(Schema):

    role: str
    access_token: str
    token_type: str
    user_details: object


class TokenWithDevice(Schema):
    can_work_offline:bool
    can_view_dashboard: bool
    is_use_controlled_transport:bool
    must_use_scale_capturing:bool
    can_view_buyers_report:bool
    isDeviceAuthirized: bool
    can_do_analysis:bool
    role: str
    access_token: str
    token_type: str
    user_details: object


class AuthToken(Schema):
    access_token: str


class TokenData(Schema):
    username: str = None


class UserAuthenticate(Schema):
    username: str
    password: str

class UserAuthenticate2(Schema):
    username: str
    password: str
    deviceId: str = None
    deviceModel:str = None
