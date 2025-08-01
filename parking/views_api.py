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


class ParkingApi:
    def receive_car_data(request, rcv_schema):
        if type(rcv_schema) != "dict":
            rcv_schema = rcv_schema.dict()
        print(rcv_schema)
        datalog = ParkingRequestLog.objects.create(
            method=request.method, query_raw=request.body,
            originate_from_ip=visitor_ip_address(request))

        cardName = None,
        data_respo={}

        if 'cardName' in rcv_schema.keys():
            cardName = rcv_schema['cardName']
            print('cardName')
            print(cardName)
            if not cardName:
                datalog.our_response_raw = 'Validation Error: cardName must not be empty or None'
                datalog.save()
                raise HttpError(400, 'Validation Error: cardName must not be empty or None')


            return data_respo
        else:
            datalog.our_response_raw = 'Failed with '+str(dataKyc.latestError)
            datalog.save()
            raise HttpError(400, 'Failed with '+str(dataKyc.latestError))

