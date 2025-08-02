from user.models import User
def _can_create_processing_shipment(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_create_processing_shipment').exists():
                return True
    return False

def _can_ship_processing_shipment(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_ship_processing_shipment').exists():
                return True
    return False


def _can_send_processing_email(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_send_processing_email').exists():
                return True
    return False

def _can_close_processing_shipment(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_close_processing_shipment').exists():
                return True
    return False

def _can_open_processing_shipment(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_open_processing_shipment').exists():
                return True
    return False

def _can_add_shipping_user(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_add_shipping_user').exists():
                return True
    return False


def _can_view_processing_shipment(user):
    if user.role:
        if user.role.perm:
            if  user.role.perm.filter(perm_name__iexact='can_view_processing_shipment').exists():
                return True
    return False


def _can_create_buying(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_creat_buying').exists():
                return True
    return False
def _can_close_buying(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_close_buying').exists():
                return True
    return False

def _can_only_view(user):
    print('user.role.role_name')
    if user.role:
        print(user.role.role_name)
        if user.role:
            if 'viewer'  in (user.role.role_name).lower():
                return True

    return False

def _can_create_offline(user):
    """changes to data"""
    #return False
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_work_create_offline').exists():
                return True
    return False

def _must_use_scale_capturing(user):
    """changes to data"""
    #return False
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='must_use_automatic_weight_capturing').exists():
                return True
    return False


def _can_do_analysis(user):
    """changes to data"""
    #return False
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_do_analysis').exists():
                return True
    return False

def _can_view_dashboard(user):
    """changes to data"""
    #return False
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_view_dashboard').exists():
                return True
    return False


def _can_view_buyers_report(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_view_buyers_report').exists():
                return True
    return False

def _can_review_request(user):

    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_view_buyers_report').exists():
                return True
    return False
