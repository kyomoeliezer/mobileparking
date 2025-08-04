from user.auth_token import GlobalAuth
from .views_api import *
from ninja import Router
from parking import schemas
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

api = Router(auth=GlobalAuth())


@api.post("/go-car-park")
def car_park_request(request, card: schemas.CarParkRequestSchema):
    return ParkingApi.go_car_data(request, card)

@api.post("/go-car-park-file")
def car_park_request2(request,card: schemas.CarParkRequestSchema,file:File[UploadedFile]):
    return ParkingApi.go_car2(request, card,file)

