from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from .models import User,Role,CustPermission
class RoleForm(forms.ModelForm):
    perm=forms.ModelMultipleChoiceField(queryset=CustPermission.objects.all(), required=False, widget=forms.CheckboxSelectMultiple,label='Permission(s)')
    class Meta:
        model=Role
        fields=('perm','name')
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email')

class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model=User
        fields=('username','password','last_name','last_name','first_name')

class CustomAuthenticationForm(forms.Form):
    username=forms.CharField(label='Email/Mobile',required=True)
    password=forms.CharField(widget=forms.PasswordInput(),label='Password')

class UserFormWananchi(forms.ModelForm):
    email=forms.EmailField(required=True,)
    mobile=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'phone-mobile'}))
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    #role=forms.ModelChoiceField(queryset=None,label='Role kwenye system')
    #kata=forms.ModelChoiceField(queryset=None,label='Kata Anakotoka',required=False)
    password=forms.CharField(widget=forms.PasswordInput())
    cpassword=forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')
    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super(UserFormWananchi, self).__init__(*args, **kwargs)
        #self.fields['kata'].queryset = Kata.objects.all()
        #self.fields['kata'].widget.attrs['class'] = 'select2'
        #self.fields['role'].queryset = Role.objects.all()
        #self.fields['role'].widget.attrs['class'] = 'select2'

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Email already exists"
            )
        else:
            return email

    def clean(self):
        cleaned_data = super(UserFormWananchi, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("cpassword")

        if password != confirm_password:
            raise forms.ValidationError(
                "The password and confirm password does not match"
            )



class UserForm(forms.ModelForm):
    email=forms.EmailField(required=True)
    mobile=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'phone-mobile'}))
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    role=forms.ModelChoiceField(queryset=None,label='Role kwenye system')
    #kata=forms.ModelChoiceField(queryset=None,label='Kata Anakotoka',required=False)
    password=forms.CharField(widget=forms.PasswordInput())
    cpassword=forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')
    class Meta:
        model=User
        fields=['first_name','last_name','role','email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #self.fields['kata'].queryset = Kata.objects.all()
        self.fields['role'].widget.attrs['class'] = 'select2'
        self.fields['role'].queryset = Role.objects.all()
        self.fields['role'].widget.attrs['class'] = 'select2'

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Email already exists"
            )
        else:
            return email

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("cpassword")
        if password != confirm_password:
            raise forms.ValidationError(
                "The password and confirm password does not match"
            )


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(required=True)
    mobile=forms.CharField(required=True)
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    role=forms.ModelChoiceField(queryset=None,label='Role kwenye system')
    #password=forms.CharField(widget=forms.PasswordInput())
    #cpassword=forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')
    class Meta:
        model=User
        fields=['first_name','last_name','email','role','mobile']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()
        self.fields['role'].widget.attrs['class'] = 'select2'


class UserUpdateFormPass(forms.ModelForm):
    last_name=forms.CharField(required=False)
    password=forms.CharField(widget=forms.PasswordInput())
    cpassword=forms.CharField(widget=forms.PasswordInput(),label='Confirm Password')
    class Meta:
        model=User
        fields=['last_name',]

    def clean(self):
        cleaned_data = super(UserUpdateFormPass, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("cpassword")
        if password != confirm_password:
            raise forms.ValidationError(
                "The password and confirm password does not match"
            )
