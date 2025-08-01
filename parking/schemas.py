from smartpolicy.models import *
from sqlite3 import Date
from ninja.orm import create_schema
from ninja import Schema
from typing import List

class CollateralSchema(Schema):
    collateralTypeId: str
    value:float = 0.0
    description:  str = ""

class GuarantorSchema(Schema):
    guarantorTypeId: str
    firstname:str
    lastname:str



class CARDReceiveKYCDataSchema(Schema):
    loanAmount: float = 0.0 or None
    nationalId: str
    firstName: str
    middleName: str = "" or None
    surName: str
    mobileNumber: str
    d_o_b: Date
    gender: str
    street_or_village: str = "" or None
    employment_status: str = "" or None
    district: str = "" or None
    region: str = "" or None
    is_maried: bool=False
    spouseName:str = "" or None
    spouseMobile: str = "" or None
    loanPurpose: str = "" or None
    loanTenure: int
    cardClientId: str
    cardLoanId: str
    loanProductId:int
    collateral:List[CollateralSchema] = [] or None
    guarantors: List[GuarantorSchema] = [] or None
    action: str = "add" or None





class CARDCheckBalanceSchema(Schema):

    cardLoanId: str

class CBSLoanSchema(Schema):

    cbsLoanId: str
