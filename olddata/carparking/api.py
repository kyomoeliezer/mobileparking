from ninja import NinjaAPI, Form

# from auths.auth_token import Authenticate
from ninja.security import HttpBearer
from user.api import api as auth_apis
from parking.api import api as park_apis
from user.authenticate import api as auth_apis2


api = NinjaAPI(
    title="CAPTURE API",
    docs_url="/docs",
)
api.add_router("user", auth_apis, tags=["Authentication APIs"])
api.add_router("auth", auth_apis2, tags=["Authentication APIs"])
api.add_router("parking", park_apis, tags=["Parking APIs"])


