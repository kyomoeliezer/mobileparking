from django.conf import settings
from django.contrib.auth.models import User

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
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

def get_user(self, user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None

