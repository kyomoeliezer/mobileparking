import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random as r
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from parking.models import BaseDB


class CustPermission(models.Model):
    perm_name=models.CharField(max_length=300,verbose_name='Permission name')
    perm_desc=models.CharField(max_length=200,verbose_name='Description')
    def __str__(self):
        return  self.perm_desc
# models
class Role(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,null=True)
    code=models.CharField(max_length=10,null=False)
    perm=models.ManyToManyField(CustPermission)
    def __str__(self):
        return self.name



class User(AbstractUser):
    username = models.EmailField(unique=True,max_length=100)
    role=models.ForeignKey(Role,on_delete=models.DO_NOTHING,null=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    full_name=models.CharField(max_length=100,blank=True,null=True)
    mobile=models.CharField(max_length=20,null=True)
    velidate_string=models.CharField(max_length=200, null=True)
    is_validated=models.BooleanField(default=True)

    def __str__(self):
        return self.email
    def name(self):
        return self.username


class LoginLog(BaseDB):
    """Model definition for LoginLog."""

    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now=False, null=True, blank=True)

    class Meta:
        """Meta definition for LoginLog."""

        verbose_name = "LoginLog"
        verbose_name_plural = "LoginLogs"
        db_table = "login_log"

    def __str__(self):
        """Unicode representation of LoginLog."""
        return self.created_by.username

