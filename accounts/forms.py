from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','phone_no','password']

    def clean(self):    #ha inputs gheto internal operations kahi tari karto ani cleaned karto data la
        cleaned_data=super(UserForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')    

        if password!=confirm_password:  #heh password validations cha na non field errors madhe count hota ani non field errros can be handle in forms.py and field erors arised due to model fields 
            raise forms.ValidationError(           #non field ani field error cha red alert pop up registerUsermadhe handle kelay
                "Password Does not Match"
            )