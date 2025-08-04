import datetime
from django.shortcuts import render, HttpResponse
from http.client import HTTPException
from ninja.errors import HttpError
from django.utils.decorators import method_decorator
from user.decorators import *
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView
from django.shortcuts import redirect,reverse,resolve_url,render,HttpResponse
from django.contrib.auth.models import Group
from django.db.models import Q,Count,F,Max,ProtectedError
from django.db.models import ProtectedError,Count,F,Q,Case,When,Value,FloatField,Sum
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login,logout # ,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib import messages
from parking.models import *
from parking.forms import *
from zoneinfo import ZoneInfo

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




class ParkingApi:
    def go_car_data(request, rcv_schema):
        if type(rcv_schema) != "dict":
            rcv_schema = rcv_schema.dict()
        print(rcv_schema)
        datalog = ParkingRequestLog.objects.create(
            method=request.method, query_raw=request.body,
            originate_from_ip=visitor_ip_address(request))

        cardName = None,
        data_respo={}
        action='in'
        vehicleNo=None

        if 'vehicleNo' in rcv_schema.keys():
            vehicleNo = rcv_schema['vehicleNo'].strip()
            print('vehicleNo')
            print(vehicleNo)
            if not vehicleNo:
                datalog.our_response_raw = 'Validation Error: vehicleNo must not be empty or None'
                datalog.save()
                raise HttpError(400, 'Validation Error: vehicleNo must not be empty or None')


        if 'action' in rcv_schema.keys():
            action = rcv_schema['action'].strip()
            if not action:
                action='in'


        if 'in' in action:
            if not Parking.objects.filter(Q(cardName__iexact=vehicleNo)&Q(Q(status__isnull=True)|~Q(status__iexact='paid'))).exists():
                parkdata=Parking.objects.create(
                    cardName=vehicleNo
                )
                return {
                    'parked_at': str(parkdata.created_on),
                    'parking_id': str(parkdata.id),
                    'billingStatus': str(parkdata.id),
                    'billingAmount': str(parkdata.id),
                    'billingAt': str(parkdata.id),
                    'billingPaymentStatus': str(parkdata.id),

                }
            else:
                parkdata=Parking.objects.filter(Q(cardName__iexact=vehicleNo)&Q(Q(status__isnull=True)|~Q(status__iexact='paid'))).first()
                return {
                    'parked_at':str(parkdata.created_on),
                    'parking_id' : str(parkdata.id),
                    'billingStatus' : str(parkdata.id),
                    'billingAmount': str(parkdata.id),
                    'billingAt': str(parkdata.id),
                    'billingPaymentStatus': str(parkdata.id),

                }



        else:
            datalog.our_response_raw = 'Failed please insert  the correct car number'
            datalog.save()
            raise HttpError(400, ' '+str('Failed please insert  the correct car number'))

