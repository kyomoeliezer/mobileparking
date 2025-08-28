from django import template
from django.contrib.auth.models import Group
from django.db.models import Q

from parking.models import Payment
from parking.models import ParkingBill
register = template.Library()

@register.simple_tag
def disparted_at(parkId):
     if ParkingBill.objects.filter(parking_id=parkId).exists():
         return ParkingBill.objects.filter(parking_id=parkId).first().created_on
     return ''

@register.simple_tag
def paid_parking(parkId):
    if ParkingBill.objects.filter(parking_id=parkId).exists():
        return Payment.objects.filter(parkingbill__parking_id=parkId).first().created_on
    return None

