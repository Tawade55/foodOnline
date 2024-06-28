from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.
def registerUser(request):      #post request ne form save honaar
        if request.method=="POST":
                
                form=UserForm(request.POST)
                if form.is_valid():
                        password=form.cleaned_data['password']
                        user=form.save(commit=False)    #hyacha aarata ready to save
                        user.set_password('password')
                        user.role=User.CUSTOMER
                        user.save()
                        messages.success(request,'Your account has been registered successfully!')
                        return redirect('registerUser')
                else:
                        print("Inavlid form")
                        print(form.errors)
        else:
                form=UserForm()
        context = {
                'form':form,
        }
        return render(request,'accounts/registerUser.html',context)