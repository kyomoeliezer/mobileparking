from user.auth_token import GlobalAuth
from .views_api import *
from ninja import Router
from parking import schemas
from typing import List


api = Router(auth=GlobalAuth())


@api.post("/go-car-park")
def car_park_request(request, card: schemas.CarParkRequestSchema):
    return ParkingApi.go_car_data(request, card)

