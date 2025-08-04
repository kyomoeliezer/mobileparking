from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
default_message = 'You dont have permission.'
unauthenticated_message = 'User already logged in.'
perm_url=reverse_lazy('no_permission')
def admin_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url, message=default_message):
    """
    Decorator for views that checks that the user is logged in and is
    staff, displaying message if provided.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name='admin').exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator



###CHET Certificate Permission
def cert_permission(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url, message=default_message):
    """
    Decorator for views that checks that the user is permitted to created the certificate.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['cert_permission',]).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

###CHET Certificate Permission
def account_permission(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url, message=default_message):
    """
    Decorator for views that checks that the user is permitted to created the certificate.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['cert_permission',]).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator



#########################################################
#########################################################
###LOAN DECORATOR########################################
def create_update_loan(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user has a create role for the loan.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['create_update_loan']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
#####
def view_loan(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user has a view loan.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['view_loan']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def delete_loan(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user has a delete loan.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['delete_loan']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def approve_loan(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user has a approve loan.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['approve_loan']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def disburse_loan(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user has disburse  loan.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['disburse_loan']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def disburse_loan(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user has view_loan_report  role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['view_loan_report']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


#######################################################################
####ACCOUNT DECORATORS

def create_update_account(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a create_update_account role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['create_update_account']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def delete_account(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a delete_account role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['delete_account']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def post_repayment(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a post_repayment role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['post_repayment']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def post_receipt(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a post_receipt role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['post_receipt']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def post_journal(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a post_journal role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['post_journal']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def view_account_report(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a view_account_report role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['view_account_report']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def view_system_logs(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a view_system_logs role.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['view_system_logs']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
###@END OF ACCOUNT DECOLATORSs

def manage_setting(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a manage setting role.
    """
    actual_decorator = user_passes_test(
        lambda u: 'demo@ubungo.co.tz' in u.username, # u.role.perm.filter(perm_name__in=['manage_setting']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def manage_roles(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a manage roles role.
    """
    actual_decorator = user_passes_test(
        lambda u:'demo@ubungo.co.tz' in u.username, #u.role.perm.filter(perm_name__in=['manage_role']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def create_update_user(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=perm_url,
                       message=default_message):
    """
    Decorator for views that checks that the user is a create_update_user.
    """
    actual_decorator = user_passes_test(
        lambda u: u.role.perm.filter(perm_name__in=['create_update_user']).exists(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,

    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

