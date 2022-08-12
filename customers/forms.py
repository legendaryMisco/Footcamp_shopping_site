from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Register

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1']


    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class EditAccountForm(ModelForm):
    class Meta:
        model = Register
        fields ='__all__'
        exclude = ['user']

        labels = {
            'name':'Fullname',
            'picture':'Profile Picture'
        }


    def __init__(self,*args,**kwargs):
        super(EditAccountForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})






