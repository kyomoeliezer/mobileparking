from xmlrpc.client import boolean
from django.db import models
from django.utils.timezone import localtime
from auditlog.registry import auditlog
import uuid

# Create your models here.

class BaseDBNormal(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class BaseDB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def get_local_created_on(self):
        return localtime(self.created_on)

class TimeSettings(BaseDB):
    chargeAmount=models.FloatField()
    minimumTime=models.FloatField(null=True)
    maximumTime=models.FloatField(null=True)
    hours=models.FloatField( null=True,verbose_name='Number of hours')
    def __str__(self):
        return str(self.minimumTime)+'-'+str(self.maximumTime)+'-'+str(self.chargedAmount)



class Parking(BaseDB):
    no=models.IntegerField(default=0)
    park_no=models.CharField(max_length=300,null=True)
    cardName=models.CharField(max_length=300)
    status = models.CharField(max_length=300,null=True)
    def __str__(self):
        return self.cardName


class ParkingBill(BaseDB):
    billedAmount = models.FloatField(null=True)
    timespentInMinutes = models.FloatField(null=True)
    status=models.CharField(max_length=200,null=True)
    parking= models.ForeignKey(
        Parking, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.billedAmount)


class Payment(BaseDB):
    no=models.IntegerField(null=True)
    paymentNo=models.CharField(max_length=200,null=True)
    paidAmount = models.FloatField(null=True)
    parkingbill= models.ForeignKey(ParkingBill, on_delete=models.PROTECT)
    def __str__(self):
        return self.paidAmount


class ParkingRequestLog(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, null=True)
    originate_from_ip = models.CharField(max_length=50, null=True)
    query_raw = models.TextField(null=True)
    our_response_raw = models.TextField(null=True)
    is_authentication = models.BooleanField(default=False)

    def __str__(self):
        return self.method
#auditlog.register(ParkingRequestLog)
auditlog.register(Payment)
auditlog.register(ParkingBill)
auditlog.register(Parking)
auditlog.register(TimeSettings)


