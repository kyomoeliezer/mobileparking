from parking.models import *
from sqlite3 import Date
from ninja.orm import create_schema
from ninja import Schema
from typing import List


class CarParkRequestSchema(Schema):
    vehicleNo: str = '' or None


