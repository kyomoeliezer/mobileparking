from django import template
from django.contrib.auth.models import Group
from django.db.models import Q

from parking.models import Payment,TimeSettings
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
        if Payment.objects.filter(parkingbill__parking_id=parkId).first():
            return Payment.objects.filter(parkingbill__parking_id=parkId).first().created_on
    return None

@register.simple_tag
def time_setting_exists():
    if TimeSettings.objects.filter(hours__isnull=False).exists():
        return True
    return False
@register.simple_tag
def time_setting_exist_more():
    if TimeSettings.objects.filter(hours__isnull=False).count() > 1:
        return True
    return False



