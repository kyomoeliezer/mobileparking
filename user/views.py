from django.utils.decorators import method_decorator

from user.common import send_Email
from user.decorators import *
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView
from django.shortcuts import redirect,reverse,resolve_url,render,HttpResponse
from django.contrib.auth.models import Group
from django.db.models import Q,Count,F,Max,ProtectedError
#from django.db.models import ProtectedError,Count,F,Q,Case,When,Value,FloatField,Sum
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login,logout # ,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from user.custombackend import authenticate
from user.form import CustomAuthenticationForm
from user.form import CustomUserCreationForm,UserForm,UserUpdateForm,UserUpdateFormPass,RoleForm
from django.contrib.auth.hashers import make_password
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib import messages
from parking.models import *
import csv
from django.core.files.storage import FileSystemStorage
from user.common import *
from user.models import Role,User,CustPermission
from django.template.loader import render_to_string
# Create your views here.
class TestEmiali(View):
    def get(self,request):
        message = render_to_string('email/welcome_email.html', {
                    'name': User.objects.first().first_name,
                    'message': '',
                    'urlw':request.build_absolute_uri(reverse('login_user')),
                    'user':User.objects.first(),
                    })
        return HttpResponse(send_mail('kyomo89elieza@gmail.com', 'testrrr', message))
    #return  HttpResponse(sendSMS('0739350620','FROM SYSTEM',request.user))
        
class RoleList(LoginRequiredMixin,ListView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Group
    context_object_name = 'lists'
    template_name = 'user/role_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(RoleList,self).get_context_data()
        context['Title']='Roles'

        return context

class UserDelete(LoginRequiredMixin,DeleteView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = User
    success_url = reverse_lazy('users')
    success_message = "Success! deleted"
    def get(self, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return self.post(*args, **kwargs)


class LoginView1(View):
    form_class = CustomAuthenticationForm
    #template_name = 'user/login1.html'
    #template_name='wananchi/wananchi_home.html'
    template_name='user/login_ubungo.html'
    # display blank form
    def get(self, request):
        logout(request)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    #process form data
    def post(self, request):
        form = self.form_class(data=request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')

        if form.is_valid():
            #if credentials are correct, this returns a user object
            user = authenticate(self,username=username, password=password)
            #return HttpResponse(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('users')
                    """
                    if 'wananchiadmin' in user.role.name:
                        return redirect(reverse('status_uandikishaji',kwargs={'pk':self.request.user.id}))
                    elif 'AMA' in user.role.code:
                        return redirect('dashboard')
                        #return redirect('app')

                    elif 'AMI' in user.role.code:
                        return redirect('ldashboard')

                    elif 'AC' in user.role.code:
                        return redirect('adashboard')

                    else:
                        return redirect('app')
                    """

            else:
                return render(request, self.template_name, {'form': form,'error':'Your email and password are incorect, please enter it well or if not registered register '+username})

        return render(request, self.template_name, {'form': form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_user')

####ROLES
deco=[manage_roles,]
@method_decorator(deco,name='dispatch')
class CreateRole(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Role
    form_class = RoleForm
    #fields = ['name','code','perm']
    template_name = 'user/new_role.html'
    context_object_name = 'form'
    header='New Role'
    success_url = reverse_lazy('roles')

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

deco=[manage_roles,]
#@method_decorator(deco,name='dispatch')
class UpdateRole(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')

    model = Role
    form_class = RoleForm
    template_name = 'user/new_role.html'
    context_object_name = 'form'
    header='Update Role'
    success_url = reverse_lazy('roles')

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

class Roles(LoginRequiredMixin,ListView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Role
    context_object_name = 'lists'
    template_name = 'user/role_role.html'
    header='Roles'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

#deco_user=[admin_required,reg_required]
#@method_decorator(deco_user,name='dispatch')
class Users(LoginRequiredMixin,ListView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = User
    context_object_name = 'lists'
    template_name = 'user/user_list.html'
    header='Users'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

deco=[manage_roles,]
@method_decorator(deco,name='dispatch')
class RoleDelete(LoginRequiredMixin,DeleteView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = Role
    success_message = "Success!  umefuta."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(request,'Huwezi kufuta aina user huyu, kuna data zinategemea data za user hii')
            return redirect('roles')

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('roles')
################################
###########CREATE PERMISSION#############
####ROLES
deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class CreatePermission(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = CustPermission
    fields = ['perm_name','perm_desc']
    template_name = 'perm/create.html'
    context_object_name = 'form'
    header='New Permission'
    success_url = reverse_lazy('permissions')

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class UpdatePermission(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')

    model = CustPermission
    fields = ['perm_name','perm_desc']
    template_name ='perm/create.html'
    context_object_name = 'form'
    header='Update Permission'
    success_url = reverse_lazy('permissions')
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class PermissionDelete(LoginRequiredMixin,DeleteView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = CustPermission
    success_message = "Success!  deleted permissions."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(request,'Huwezi kufuta permission hii, kuna data zinategemea data  hii')
            return redirect('permissions')

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('permissions')

class PermissionsList(LoginRequiredMixin,ListView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = CustPermission
    context_object_name = 'lists'
    template_name = 'perm/perm_list.html'
    header='Permissions'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        context['lists']=CustPermission.objects.all().order_by('id')
        return context

class PermissionRequired(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'perm/permission_required.html')
###END PERMISSION###########################
######MODULE###############################

###MODULE END
deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class NewUser(LoginRequiredMixin,CreateView):

    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model =User
    form_class = UserForm
    template_name = 'user/new_user.html'
    context_object_name = 'form'
    header='New User'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        context['roles']=Role.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('cpassword') in request.POST.get('password'):
                user=User.objects.create_user(username=request.POST.get('email'),email=request.POST.get('email'),mobile=request.POST.get('mobile'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),role_id=request.POST.get('role'),password=request.POST.get('password'),is_staff=True,is_active=True)
                user.set_password(request.POST.get('password'))
                user.save()
                messages.success(request,'Success! created '+request.POST.get('email'))
                subject='Welcome to DYG Microcredit'
                #sendSMS(user.mobile,' You have been registered in the DYG Microcredit. Your Password is '+str(request.POST.get('cpassword')),request.user)
                message = render_to_string('email/welcome_email.html', {
                    'name': request.user.first_name,
                    'urlw':request.build_absolute_uri(reverse('login_user')),
                    'message': '',
                    'password':request.POST.get('cpassword'),
                    'user':user,
                    })

                send_Mmail(request.POST.get('email'), subject, message)
                return redirect('users')
            else:
                return render(request,self.template_name,{'form':form,'header':self.header,'error':'Password Do not Match'})

        else:
            return render(request,self.template_name,{'form':form,'header':self.header})

deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class UpdateUser(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model =User
    form_class = UserUpdateForm
    template_name = 'user/update_user.html'
    context_object_name = 'form'
    header='Update User'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header

        return context
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():


            user=User.objects.filter(id= self.kwargs['pk']).update(username=request.POST.get('email'),email=request.POST.get('email'),mobile=request.POST.get('mobile'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),role_id=request.POST.get('role'))
            user=User.objects.get(id= self.kwargs['pk'])
            #user.set_password('Mgaya$456')
            #user.save()
            messages.success(request,'Success! update '+request.POST.get('email'))
            return redirect('users')

                #return render(request,self.template_name,{'form':form,'header':self.header,'error':'Password Do not Match'})

        else:
            return render(request,self.template_name,{'form':form,'header':self.header})

##########################################################################################################
####################MWAKA WA FEDHA##############################



"""
class UpdateUser(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model =User
    form_class = UserForm
    template_name = 'user/edit_user.html'
    context_object_name = 'form'
    header='Update User'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        context['roles']=Role.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            if request.POST.get('email'):
                user=User.objects.create_user(username=request.POST.get('email'),email=request.POST.get('email'),mobile=request.POST.get('mobile'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),role_id=request.POST.get('role'),password=make_password(request.POST.get('password')),kata_id=request.POST.get('kata'),is_staff=True,is_active=True)
                messages.success(request,'Success! created '+request.POST.get('email'))
                return redirect('users')
            else:
                return render(request,self.template_name,{'form':form,'header':self.header,'error':'Password Do not Match'})

        else:
            return render(request,self.template_name,{'form':form,'header':self.header})

"""

class UpdateUserChangePassword(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model =User
    form_class = UserUpdateFormPass
    template_name = 'user/change_user_pass.html'
    context_object_name = 'form'
    header='CHANGE PASSWORD'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['userob']=User.objects.filter(id=self.kwargs['pk']).first()
        context['header']=self.header

        return context
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():


            user=User.objects.filter(id= self.kwargs['pk']).update(password=make_password(request.POST.get('password')))
            messages.success(request,'Success! update changed password')
            return redirect('users')

                #return render(request,self.template_name,{'form':form,'header':self.header,'error':'Password Do not Match'})

        else:
            return render(request,self.template_name,{'form':form,'header':self.header})

class TestRole(View):
    def get(self,request):
        if request.user.role.perm.filter(perm_name='admin').exists():
            return  HttpResponse('reg_view')

        return HttpResponse(request.user.role.perm.all())


################################
###########CREATE FEE SETTINGS#############
####FEEE
deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class CreateFeeSetting(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = TimeSettings
    fields = ['chargeAmount','hours']
    template_name ='setting/new_fee_settings.html'
    context_object_name = 'form'
    header='New Settings'
    success_url = reverse_lazy('fee_settings')

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class UpdateFeeSettings(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')

    model = TimeSettings
    fields = ['chargeAmount','hours']
    template_name ='setting/new_fee_settings.html'
    context_object_name = 'form'
    header='Fee Settings'
    success_url = reverse_lazy('fee_settings')
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

deco=[manage_setting,]
@method_decorator(deco,name='dispatch')
class FeeSettingnDelete(LoginRequiredMixin,DeleteView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = TimeSettings
    success_message = "Success!  deleted permissions."
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.warning(request,'Huwezi kufuta data hii, kuna data zinategemea data  hii')
            return redirect('fee_settings')

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('fee_settings')

class FeeSettingList(LoginRequiredMixin,ListView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = TimeSettings
    context_object_name = 'lists'
    template_name ='setting/fee_settings.html'
    header='Time Settings'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        context['lists']=TimeSettings.objects.all().order_by('id')
        return context


###END FEE SETTINGS###########################
######MODULE###############################
def import_roles(request):
    fs=FileSystemStorage(location='import/permission/')
    file_name='perm.csv'
    counter = 0
    with open(fs.path(file_name), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        #return HttpResponse(reader)
        #models.CustPermission.objects.all().delete()
        for row in reader:
            if row['perm_name'] and row['perm_desc'] :
                radio=False
                if row['radio']:
                    if int(row['radio']) == 1:
                        radio=True

                if CustPermission.objects.filter(perm_name__iexact=row['perm_name']).exists():

                    CustPermission.objects.filter(perm_name__iexact=row['perm_name']).update(
                        perm_name=row['perm_name'],
                        perm_desc=row['perm_desc'],
                    )
                else:
                    CustPermission.objects.create(
                    perm_name=row['perm_name'],
                    perm_desc=row['perm_desc'],
                   )
                counter += 1
        messages.success(request,'created permisions')
        return redirect(reverse('permissions'))
    return redirect(reverse('permissions'))

