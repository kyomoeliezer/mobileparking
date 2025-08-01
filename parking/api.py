from user.auth_token import GlobalAuth
from .views_api import *
from ninja import Router
from parking import schemas
from typing import List


api = Router(auth=GlobalAuth())


@api.post("/data")
def card_receive_data(request, card: schemas.CARDReceiveKYCDataSchema):
    return CardKycAPi.receive_card_data(request, card)


@api.post("/check-status")#, response=List[schemas.GetSmartPolicySchema])
def check_status(request,card: schemas.CARDCheckBalanceSchema):
    return CardKycAPi.check_status(request,card)

@api.get("/guarantors/templates")#, response=List[schemas.GetSmartPolicySchema])
def guarantors_templates(request):
    return CardKycAPi.get_guarantor_types(request)

@api.get("/collateral/templates")#, response=List[schemas.GetSmartPolicySchema])
def collateral_templates(request):
    return CardKycAPi.get_collateral_types(request)
@api.get("/list-loanproducts")#, response=List[schemas.GetSmartPolicySchema])
def get_loan_products(request):
    return CardKycAPi.get_get_loan_products(request)
