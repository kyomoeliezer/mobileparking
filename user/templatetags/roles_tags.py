
from django import template
from django.contrib.auth.models import Group
from django.db.models import Q
register = template.Library()


@register.simple_tag
def is_admin(user):
    if 'demo@' in user.username:
        return  True
    return user.role.perm.filter(perm_name='manage_user').exists()



@register.simple_tag
def is_account(user):
    if 'demo@' in user.username:
        return True
    return user.role.perm.filter(perm_name='manage_bill').exists()


@register.simple_tag
def can_create_update_loan(user):
     return user.role.perm.filter(perm_name__in=['create_update_loan']).exists()

@register.simple_tag
def can_delete_loan(user):
     return user.role.perm.filter(perm_name__in=['delete_loan']).exists()

@register.simple_tag
def can_disburse_loan(user):
     return user.role.perm.filter(perm_name__in=['disburse_loan']).exists()

@register.simple_tag
def can_approve_loan(user):
     return user.role.perm.filter(perm_name__in=['approve_loan']).exists()

@register.simple_tag
def can_create_update_account(user):
     return user.role.perm.filter(perm_name__in=['create_update_account']).exists()

@register.simple_tag
def can_post_journal(user):
     return user.role.perm.filter(perm_name__in=['post_journal']).exists()

@register.simple_tag
def can_post_receipt(user):
     return user.role.perm.filter(perm_name__in=['post_receipt']).exists()

@register.simple_tag
def can_post_repayment(user):
     return user.role.perm.filter(perm_name__in=['post_repayment']).exists()

@register.simple_tag
def can_post_expense(user):
     return user.role.perm.filter(perm_name__in=['post_expense']).exists()


############################################
#####SETTING ROLES
@register.simple_tag
def can_manage_setting(user):
     return user.role.perm.filter(perm_name__in=['manage_setting']).exists()

@register.simple_tag
def can_approve_loan(user):
     return user.role.perm.filter(perm_name__in=['approve_loan']).exists()

@register.simple_tag
def can_disburse_loan(user):
    if 'demo@ubungo.co.tz' in user.username:
        return True
    return user.role.perm.filter(perm_name__in=['disburse_loan']).exists()


@register.simple_tag
def can_create_update_user(user):
    if 'demo@ubungo.co.tz' in user.username:
        return True
    return user.role.perm.filter(perm_name__in=['create_update_user']).exists()

@register.simple_tag
def can_manage_role(user):
    if 'demo@ubungo.co.tz' in user.username:
        return True
    return user.role.perm.filter(perm_name__in=['manage_role']).exists()


@register.simple_tag
def role_name(user):
      if  not  user.groups.filter(name='admin').exists():
           return 'Admin'
      elif  not  user.groups.filter(name='manager').exists():
           return 'Manager'
      elif  not  user.groups.filter(name='teacher').exists():
           return 'Teacher'
      elif  not  user.groups.filter(name='parent').exists():
           return 'Parent'
      elif  not  user.groups.filter(name='academic').exists():
           return 'Academic'
      else:
           return ''

