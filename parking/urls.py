from django.urls import path, re_path as url
from parking.views import *

from user.roles import YouDontHavePermission

urlpatterns=[
    


    url(r'^new-parking$', NewCarPark.as_view(),name='new_parking'),
    url(r'^(?P<pk>[\w-]+)/deleteparking$', ParkingDelete.as_view(),name='delete_parking'),
    url(r'^(?P<pk>[\w-]+)/generate-billing', GenerateParking.as_view(),name='generate_billing'),
    url(r'^(?P<pk>[\w-]+)/pay-bill', MakePayment.as_view(),name='pay_bill'),
    url(r'^(?P<pk>[\w-]+)/payment-details', PaymentDetail.as_view(),name='payment_details'),


    url(r'^parking-billing$', ParkingBilling.as_view(),name='parking_billing'),
    url(r'^paymentlists$', PaymentLists.as_view(),name='payment_lists'),
    url(r'^testImage', RecognizePlate.as_view(),name='testData'),

    url(r'^currentParking$', CurrentParkingList.as_view(),name='parking_lists'),
    url(r'^report', ReportParkingList.as_view(),name='parking_report'),

    url(r'^$', BillingDashboard.as_view(),name='dashboard'),









    ##ENDPER

]
