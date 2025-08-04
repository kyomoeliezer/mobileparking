from django.urls import path, re_path as url
from user.views import *

from user.roles import YouDontHavePermission

urlpatterns=[
    

    url(r'^login-user$', LoginView1.as_view(),name='login_user'),
    url(r'^login-user$', LoginView1.as_view(),name='login-user'),
    url(r'^logout-user$', LogoutView.as_view(),name='logout_user'),
    url(r'^userroles$', Roles.as_view(),name='roles'),
    url(r'^users$', Users.as_view(),name='users'),
    url(r'^new-user$', NewUser.as_view(),name='new_user'),
    url(r'^test-role$',TestRole.as_view(),name='test_role'),

    url(r'^new-role$', CreateRole.as_view(),name='new_role'),
    url(r'^you-dont-have-permission$', YouDontHavePermission.as_view(),name='no_permission'),
    #####MODULE PERMISSION MODULE

    url(r'^new-user$', NewUser.as_view(),name='new_user'),
    url(r'^test-role$',TestRole.as_view(),name='test_role'),


    url(r'^(?P<pk>[0-9]+)/delete$', UserDelete.as_view(),name='delete_user'),
    url(r'^role/(?P<pk>[0-9]+)/update$', UpdateRole.as_view(),name='update_role'),
    url(r'^role/(?P<pk>[0-9]+)/delete', RoleDelete.as_view(),name='delete_role'),
    url(r'^(?P<pk>[0-9]+)/user-update$', UpdateUser.as_view(),name='update_user'),
    url(r'^(?P<pk>[0-9]+)/xx-change-pass$', UpdateUserChangePassword.as_view(),name='change_pass_user'),
    ###PERMIS
    url(r'^perm-required$', PermissionRequired.as_view(),name='permission_required'),
    url(r'^permissions$', PermissionsList.as_view(),name='permissions'),
    url(r'^new-permission$', CreatePermission.as_view(),name='new_permission'),
    url(r'^permission/(?P<pk>[0-9]+)/update$', UpdatePermission.as_view(),name='update_permission'),
    url(r'^permission/(?P<pk>[0-9]+)/delete$', PermissionDelete.as_view(),name='delete_permission'),
    ####FEES SETTINGS
    url(r'^fee-seetings', FeeSettingList.as_view(), name='fee_settings'),
    url(r'^new-settings$', CreateFeeSetting.as_view(), name='new_fee_settings'),
    url(r'^seetings/(?P<pk>[\w-]+)/update$', UpdateFeeSettings.as_view(), name='update_fee_settings'),
    url(r'^settings/(?P<pk>[\w-]+)/delete$', FeeSettingnDelete.as_view(), name='delete_fee_settings'),
    ####


    ##ENDPER

]
