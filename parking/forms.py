from parking.models import *
from django import forms


class SeachData(forms.ModelForm):
    seach_name=forms.CharField(label='LoanId',required=False)
    fromdate=forms.DateField(label='From Date',required=False,widget=forms.widgets.DateInput(
        attrs={'type': 'date'}))
    todate = forms.DateField(label='To Date', required=False,widget=forms.widgets.DateInput(
        attrs={'type': 'date'}))
    cardName=forms.CharField(required=False)

    class Meta:
        model=Parking
        fields=('cardName',)

class MakePaymentForm(forms.ModelForm):
    amount=forms.CharField(label='Amount ',required=False)

    class Meta:
        model=ParkingBill
        fields=('amount',)
