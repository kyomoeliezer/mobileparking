import datetime

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


class CurrentParkingList(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Parking
    context_object_name = 'lists'
    template_name = 'parking/parking_lists.html'

    def get(self,request,*args, **kwargs):
        context = {}

        context['form']=SeachData

        context['header'] = ' Today Parking [   ' + str(datetime.datetime.now().date())+']'
        context['lists'] = Parking.objects.all().order_by(
            '-created_on')
        #return HttpResponse(context)

        return render(request,self.template_name,context)

    def post(self,request,*args, **kwargs):
        context = {}
        start_date=request.POST.get('fromdate')
        end_date = request.POST.get('todate')
        car = request.POST.get('cardName')
        print('car')
        print(car)
        context['form']=SeachData
        if car:
            context['header'] = str(car)+'  parking as for ' + str(datetime.datetime.now().date())
            context['lists']=Parking.objects.filter(cardName__icontains=car).order_by('-created_on')

        elif start_date:
            context['header'] = 'Parking List from  ' +str(start_date)+' to '+str(end_date)
            context['lists'] = Parking.objects.filter(created_on__gte=start_date,created_on__lte=end_date).order_by('-created_on')
        else:
            context['header'] = ' Today Parking [   ' + str(datetime.datetime.now().date())+']'
            context['lists'] = Parking.objects.filter(created_on__date=datetime.datetime.now().today()).order_by(
                '-created_on')


        return render(request,self.template_name,context)

class NewCarPark(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Parking
    fields = ['cardName']
    header='New Parking'
    success_url = reverse_lazy('parking_lists')
    template_name = 'parking/new_parking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['header'] = self.header
        return context


class ParkingDelete(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')

    def get(self,*args,**kwargs):
        Parking.objects.filter(id=self.kwargs['pk']).delete()
        return redirect(reverse('parking_lists'))


def create_bill(request,parkingId):
    dataParking = Parking.objects.filter(id=parkingId).first()
    if not ParkingBill.objects.filter(parking_id=dataParking.id).exists():
        dataTime = round(
            (datetime.datetime.now(ZoneInfo('Africa/Dar_es_Salaam')) - dataParking.created_on).total_seconds() / 60)
        if TimeSettings.objects.filter(minimumTime__lte=dataTime, maximumTime__gte=dataTime).exists():
            obj = \
            TimeSettings.objects.filter(minimumTime__lte=dataTime, maximumTime__gte=dataTime).order_by('-created_on')[0]
            ParkingBill.objects.create(
                parking=dataParking,
                timespentInMinutes=dataTime,
                billedAmount=obj.chargeAmount
            )
        else:
            messages.warning(request, 'Please the time setting for this is not available ' + str(dataTime))
    else:
        billData = ParkingBill.objects.filter(parking_id=dataParking.id).first()


class GenerateParking(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')

    def get(self,*args,**kwargs):
        dataParking=Parking.objects.filter(id=self.kwargs['pk']).first()
        if not  ParkingBill.objects.filter(parking_id=dataParking.id).exists():
            dataTime=round((datetime.datetime.now(ZoneInfo('Africa/Dar_es_Salaam'))-dataParking.created_on).total_seconds()/60)
            if TimeSettings.objects.filter(minimumTime__lte=dataTime,maximumTime__gte=dataTime).exists():
                obj=TimeSettings.objects.filter(minimumTime__lte=dataTime, maximumTime__gte=dataTime).order_by('-created_on')[0]
                ParkingBill.objects.create(
                    parking=dataParking,
                    timespentInMinutes=dataTime,
                    billedAmount=obj.chargeAmount
                )
            else:
                messages.warning(self.request,'Please the time setting for this is not available '+str(dataTime))
        else:
            billData=ParkingBill.objects.filter(parking_id=dataParking.id).first()


        return redirect(reverse('parking_lists'))

class ParkingBilling (LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = ParkingBill
    context_object_name = 'lists'
    template_name = 'parking/billing_lists.html'

    def get(self,request,*args, **kwargs):
        context = {}

        context['form']=SeachData

        context['header'] = ' Parking Pilling  [   ' + str(datetime.datetime.now().date())+']'
        context['lists'] = ParkingBill.objects.all().order_by(
            '-created_on')
        #return HttpResponse(context)

        return render(request,self.template_name,context)

    def post(self,request,*args, **kwargs):
        context = {}
        start_date=request.POST.get('fromdate')
        end_date = request.POST.get('todate')
        car = request.POST.get('cardName')
        print('car')
        print(car)
        context['form']=SeachData
        if car:
            context['header'] = str(car)+'  billing as for ' + str(datetime.datetime.now().date())
            context['lists']=ParkingBill.objects.filter(parking__cardName__icontains=car).order_by('-created_on')

        elif start_date:
            context['header'] = 'Billing List from  ' +str(start_date)+' to '+str(end_date)
            context['lists'] = ParkingBill.objects.filter(created_on__gte=start_date,created_on__lte=end_date).order_by('-created_on')
        else:
            context['header'] = ' Today Billing [   ' + str(datetime.datetime.now().date())+']'
            context['lists'] = ParkingBill.objects.filter(created_on__date=datetime.datetime.now().today()).order_by(
                '-created_on')


        return render(request,self.template_name,context)

class MakePayment(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Parking
    header='MAKE PAYMENT'
    success_url = reverse_lazy('parking_lists')
    template_name = 'parking/make_payment.html'
    form_class=MakePaymentForm

    def get(self, *args,**kwargs):

        context = {}#
        context['form']=MakePaymentForm
        create_bill(self.request,self.kwargs['pk'])
        billOb=ParkingBill.objects.filter(parking_id=self.kwargs['pk']).first()
        context['bill']=billOb
        context['header'] = self.header
        return render(self.request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        billOb = ParkingBill.objects.filter(parking_id=self.kwargs['pk']).first()
        form = self.form_class(request.POST)
        context={}
        context['form']=form
        if form.is_valid():
            if not  Payment.objects.filter(parkingbill_id=billOb.id).exists():
                pymentOb=Payment.objects.create(
                    parkingbill=billOb,
                    paidAmount=request.POST.get('amount')
                )
                billOb.status='paid'
                billOb.save()
                Parking.objects.filter(id=self.kwargs['pk']).update(
                    status='paid'
                )
                messages.success(self.request,'Payment made '+str(pymentOb.id))
            else:
                pymentOb=Payment.objects.filter(parkingbill_id=billOb.id).first()
                messages.warning(self.request,'Payment was made with '+str(pymentOb.id))
            return redirect(reverse('payment_details',kwargs={'pk':pymentOb.id}))
        return render(self.request,self.template_name,context)


class PaymentDetail(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Parking
    header='Payment Details'
    success_url = reverse_lazy('parking_lists')
    template_name = 'parking/payment_detail.html'
    form_class=MakePaymentForm

    def get(self, *args,**kwargs):

        context = {}#
        context['form']=MakePaymentForm
        context['payment'] = paymentOb= Payment.objects.filter(id=self.kwargs['pk']).first()
        #create_bill(self.request,self.kwargs['pk'])
        billOb=ParkingBill.objects.filter(parking_id=paymentOb.parkingbill.parking_id).first()
        context['bill']=billOb

        context['header'] = self.header
        return render(self.request,self.template_name,context)

class PaymentLists(LoginRequiredMixin,View):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Payment
    context_object_name = 'lists'
    template_name = 'parking/payment_lists.html'

    def get(self,request,*args, **kwargs):
        context = {}

        context['form']=SeachData

        context['header'] = ' Payment lists [   ' + str(datetime.datetime.now().date())+']'
        context['lists'] = listdata=Payment.objects.all().order_by(
            '-created_on')
        context['totalpaid']=listdata.aggregate(sumT=Sum('paidAmount'))['sumT']
        #return HttpResponse(context)
        return render(request,self.template_name,context)

    def post(self,request,*args, **kwargs):
        context = {}
        start_date=request.POST.get('fromdate')
        end_date = request.POST.get('todate')
        car = request.POST.get('cardName')
        print('car')
        print(car)
        context['form']=SeachData
        if car:
            context['header'] = str(car)+'  payments as for ' + str(datetime.datetime.now().date())
            context['lists']=listdata=Payment.objects.filter(parkingbill__parking__cardName__icontains=car).order_by('-created_on')
            context['totalpaid'] = listdata.aggregate(sumT=Sum('paidAmount'))['sumT']
        elif start_date:
            context['header'] = 'Payment List from  ' +str(start_date)+' to '+str(end_date)
            context['lists'] = listdata=Payment.objects.filter(created_on__gte=start_date,created_on__lte=end_date).order_by('-created_on')
            context['totalpaid'] = listdata.aggregate(sumT=Sum('paidAmount'))['sumT']
        else:
            context['header'] = ' Payment List [   ' + str(datetime.datetime.now().date())+']'
            context['lists'] =listdata=Payment.objects.filter(created_on__date=datetime.datetime.now().today()).order_by(
                '-created_on')
            context['totalpaid'] = listdata.aggregate(sumT=Sum('paidAmount'))['sumT']


        return render(request,self.template_name,context)



