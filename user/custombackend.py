from django.conf import settings
from django.db.models import Q
from user.models import User

class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        elif '+255' in username:
            kwargs = {'mobile': username}

        elif username[0] == '0' and len(username)== 10:
            kwargs = {'mobile': username}

        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if User.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class CustomAuthenticationBackend:

    def authenticate(self, request, email_or_phone=None, password=None):
        try:
             user = User.objects.get(
                 Q(email=email_or_phone) | Q(mobile=email_or_phone)
             )
             pwd_valid = User.check_password(password)
             if pwd_valid:
                 return user
             return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

#def authenticate(self, username_or_mobile=None, password=None):
"""
def authenticate(self,username, password):
        kwargs = {'username': username}
        try:
            user = User.objects.get(username=username)
            return user
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
"""
def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'username': username}
        else:
            kwargs = {'mobile': username}
        try:
            user = User.objects.get(**kwargs)
            #return user

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

