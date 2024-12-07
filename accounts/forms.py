from django import forms
from .models import User,userprofile
from .validators import allow_only_images_validator

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
        

class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start Typing...', 'required':'required'}))
    profile_picture=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])

    #latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})])
    #longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})])
    class Meta:
        model=userprofile
        fields=['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']

    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly']='readonly'



class UserInfoForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','phone_no']