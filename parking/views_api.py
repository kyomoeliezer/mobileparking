import datetime
import os
from django.shortcuts import render, HttpResponse
from http.client import HTTPException
from ninja.errors import HttpError
import base64, binascii
from ninja.files import UploadedFile
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
from carparking.settings import TIME_ZONE
def accuracyData(arr):
    n = len(arr)
    # Initialize maximum element
    max = arr[0]

    # Traverse array elements from second
    # and compare every element with
    # current max
    for i in range(1, n):
        if arr[i]['Confidence'] > max['Confidence']:
            max = arr[i]
    return max
def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def parkNo(no):
    if no < 10:
        return 'PK000'+str(no)
    if no < 100:
        return 'PK00'+str(no)
    if no < 1000:
        return 'PK00'+str(no)
    if no < 10000:
        return 'PK0'+str(no)
    return 'PK'+str(no)



class ParkingApi:
    def car_confirm_plate(request,rcv_schema):
        #def go_car_data(request, rcv_schema):
        if type(rcv_schema) != "dict":
            rcv_schema = rcv_schema.dict()
        print(rcv_schema)
        datalog = ParkingRequestLog.objects.create(
            method=request.method, query_raw=request.body,
            originate_from_ip=visitor_ip_address(request))
        # try:
        image = base64.b64decode(rcv_schema['image'], validate=True)
        file_to_save = "name or path of the file to save,let's say, my_image.png"
        import simplelpr
        import random

        # Initialize the engine
        setup_params = simplelpr.EngineSetupParms()
        engine = simplelpr.SimpleLPR(setup_params)

        # Configure for your country (e.g., UK = 90)
        engine.set_countryWeight(90, 1.0)
        engine.realizeCountryWeights()
        file_to_save = "imagespark/" + str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + str(
            random.randint(200, 300)) + '' + str(rcv_schema['ext'])
        with open(file_to_save, "wb") as f:
            f.write(image)
        # Create a processor
        processor = engine.createProcessor()

        # Analyze an image
        candidates = processor.analyze(file_to_save)
        arrayData = []
        # Print results
        print(candidates);
        for candidate in candidates:
            for match in candidate.matches:
                arrayData.append({
                    'Plate': match.text,
                    'Confidence': match.confidence
                })
                print(f"Plate: {match.text}")
                print(f"Confidence: {match.confidence:.3f}")
        accruracePer = 0
        actual = ''
        if len(arrayData) > 0:
            actual = accuracyData(arrayData)
            print('actual')
            accruracePer = actual['Confidence']
            print(actual['Plate'])
            actual = actual['Plate']
        """
        except binascii.Error as e:
            raise HttpError(401,'Tafadhali chukua vizuri picha ya numba za gari')
        """
        if accruracePer < 0.9:
            raise HttpError(401, 'Tafadhali chukua vizuri picha ya numba za gari, number tu ndo zionekane')

        dir_name = "imagespark/"
        test = os.listdir(dir_name)

        for item in test:
            if not  item.startswith(datetime.datetime.now().strftime("%Y%m%d")):
                os.remove(os.path.join(dir_name, item))
        return {
            'plateNo':actual.replace(" ", "").strip()
        }

    def go_car_data(request, rcv_schema):
        if type(rcv_schema) != "dict":
            rcv_schema = rcv_schema.dict()
        print(rcv_schema)
        datalog = ParkingRequestLog.objects.create(
            method=request.method, query_raw=request.body,
            originate_from_ip=visitor_ip_address(request))

        if 'vehicleNo' in rcv_schema.keys():
            vehicleNo = rcv_schema['vehicleNo'].strip()
            print('vehicleNo')
            print(vehicleNo)
            if not vehicleNo:
                datalog.our_response_raw = 'Validation Error: vehicleNo must not be empty or None'
                datalog.save()
                raise HttpError(400, 'Validation Error: vehicleNo must not be empty or None')


        vehicleNo=vehicleNo.replace(" ", "")
        if 'action' in rcv_schema.keys():
            action = rcv_schema['action'].strip()
            if not action:
                action='in'

        nowTime = datetime.datetime.now()
        print(nowTime)
        no=0
        if 'in' in action:
            if not Parking.objects.filter(Q(cardName__iexact=vehicleNo)&Q(Q(status__isnull=True)|~Q(status__iexact='paid'))&Q(created_on__date=nowTime.date())).exists():
                parkdata=Parking.objects.create(
                    created_on =nowTime,
                    cardName=vehicleNo
                )
                dataf=Parking.objects.first()
                firstData=Parking.objects.filter(no__gt=0).first()
                print(firstData)
                if firstData:
                    no = Parking.objects.filter(no__gt=0).latest('created_on').no
                    print('currentNo'+str(no))
                    no=no+1
                else:
                    no=1
                parkdata.no=no
                parkdata.park_no=parkNo(no)
                parkdata.save()

                bill=ParkingBill.objects.filter(parking=parkdata).first()
                paym=Payment.objects.filter(parkingbill__parking=parkdata).first()
                return {
                    'parked_at': str(parkdata.created_on.strftime('%Y/%m/%d %H:%M:%S')),
                    'parking_id': str(parkdata.id),
                    'carNo': str(parkdata.cardName),
                    'billingStatus': None if not bill else bill.status,
                    'billingAmount': None if not bill else bill.billedAmount,
                    'billingAt': None if not bill else str(bill.created_on.strftime('%Y/%m/%d %H:%M:%S')),
                    'billingPaymentStatus': None if not paym else  'PAID',

                }
            else:
                parkdata=Parking.objects.filter(Q(cardName__iexact=vehicleNo)&Q(Q(status__isnull=True)|~Q(status__iexact='paid'))&Q(created_on__date=nowTime.date())).first()
                bill = ParkingBill.objects.filter(parking=parkdata).first()
                paym = Payment.objects.filter(parkingbill__parking=parkdata).first()
                return {
                    'parked_at': str(parkdata.created_on.strftime('%Y/%m/%d %H:%M:%S') ),
                    'parking_id': str(parkdata.id),
                    'carNo': str(parkdata.cardName),
                    'billingStatus': None if not bill else bill.status,
                    'billingAmount': None if not bill else bill.billedAmount,
                    'billingAt': None if not bill else str(bill.created_on.strftime('%Y/%m/%d %H:%M:%S')),
                    'billingPaymentStatus': None if not paym else 'PAID',

                }
        else:
            nowTime=datetime.datetime.now()
            if  Parking.objects.filter(Q(cardName__iexact=vehicleNo)&Q(Q(status__isnull=True)|~Q(status__iexact='paid'))).exists():
                parkdata = Parking.objects.filter(
                    Q(cardName__iexact=vehicleNo) & Q(Q(status__isnull=True) | ~Q(status__iexact='paid'))).first()
                bill = ParkingBill.objects.filter(parking=parkdata).first()
                paym = Payment.objects.filter(parkingbill__parking=parkdata).first()
                #raise HttpError(400, ' ' + str('Failed please insert  the correct car number'))
                dataFRE= {
                    'parked_at': str(parkdata.created_on.strftime('%Y-%m-%d %H:%M:%S')),
                    'parking_id': str(parkdata.id),
                    'carNo': str(parkdata.cardName),
                    'billingStatus': None if not bill else bill.status,
                    'billingAmount': None if not bill else bill.billedAmount,
                    'billingAt': None if not bill else str(bill.created_on.strftime('%Y-%m-%d %H:%M:%S')),
                    'billingPaymentStatus': None if not paym else 'PAID',

                }
                datalog.our_response_raw =dataFRE
                datalog.save()
                return dataFRE

            elif Parking.objects.filter(Q(cardName__iexact=vehicleNo) & Q(status__iexact='paid') &Q(created_on__date=nowTime.date())).exists():
                parkIpo=Parking.objects.filter(Q(cardName__iexact=vehicleNo) & Q(status__iexact='paid') &Q(created_on__date=nowTime.date())).order_by('-created_on')[0]
                payM=Payment.objects.filter(parkingbill__parking=parkIpo).first()
                bill = ParkingBill.objects.filter(parking=parkIpo).first()
                paym = Payment.objects.filter(parkingbill__parking=parkIpo).first()

                if ((nowTime-payM.created_on).total_seconds()/60) > 30:
                    dataFRE = {
                        'parked_at': str(payM.parkingbill.parking.created_on.strftime('%Y-%m-%d %H:%M:%S')),
                        'parking_id': str(payM.parkingbill.parking.id),
                        'carNo': str(payM.parkingbill.parking.cardName),
                        'billingStatus': None if not payM.parkingbill else payM.parkingbill.status,
                            'billingAmount': None if not payM else payM.paidAmount,
                        'billingAt': None if not bill else str(bill.created_on.strftime('%Y-%m-%d %H:%M:%S')),
                        'billingPaymentStatus':'AMECHELEWA',

                    }
                    datalog.our_response_raw = dataFRE
                    datalog.save()
                    return dataFRE
                else:
                    dataFRE = {
                        'parked_at': str(payM.parkingbill.parking.created_on.strftime('%Y-%m-%d %H:%M:%S')),

                        'parking_id': str(payM.parkingbill.parking),
                        'carNo': str(payM.parkingbill.parking.cardName),
                        'billingStatus': None if not bill else bill.status,
                        'billingAmount': None if not bill else bill.billedAmount,
                        'billingAt': None if not bill else str(bill.created_on.strftime('%Y-%m-%d %H:%M:%S')),
                        'billingPaymentStatus': None if not paym else 'PAID',

                    }
                    datalog.our_response_raw = dataFRE
                    datalog.save()
                    return dataFRE
            else:
                raise HttpError(401,str(vehicleNo)+' haijasajiliwa wakati wa kuingia, or angalia namba vema')

    def go_car2(self,rcv_schema,file2):
        if type(rcv_schema) != "dict":
            rcv_schema = rcv_schema.dict()

        print(rcv_schema)
        print(file2.name)







