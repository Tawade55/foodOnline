from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User,userprofile
from vendor.forms import VendorForm
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

#Restrict The Vendor from accessing the customer page
def check_role_vendor(user):
        if user.role==1:
                return True
        else:
                return PermissionDenied

def check_role_customer(user):
        if user.role==2:
                return True
        else:
                return PermissionDenied

# Create your views here.
def registerUser(request):      #post request ne form save honaar
        if request.user.is_authenticated:
                messages.warning(request,"You are already loggedin!!")
                return redirect('dashboard')
        elif request.method=="POST":
                
                form=UserForm(request.POST)
                if form.is_valid():
                        #password=form.cleaned_data['password']
                        #user=form.save(commit=False)    #hyacha aarata ready to save
                        #user.set_password('password')
                        first_name=form.cleaned_data['first_name']
                        last_name=form.cleaned_data['last_name']
                        username=form.cleaned_data['username']
                        email=form.cleaned_data['email']
                        password=form.cleaned_data['password']
                        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
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

def registerVendor(request):
        if request.user.is_authenticated:
                messages.warning(request,"You are already loggedin!!")
                return redirect('dashboard')
        elif request.method=="POST":
                form=UserForm(request.POST)
                v_form=VendorForm(request.POST,request.FILES)
                if form.is_valid() and v_form.is_valid:
                        first_name=form.cleaned_data['first_name']
                        last_name=form.cleaned_data['last_name']
                        username=form.cleaned_data['username']
                        email=form.cleaned_data['email']
                        password=form.cleaned_data['password']
                        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                        user.role=User.VENDOR
                        user.save()
                        vendor=v_form.save(commit=False)
                        vendor.user=user
                        user_profile=userprofile.objects.get(user=user)
                        vendor.user_profile=user_profile
                        vendor.save()
                        messages.success(request,"Your account has been registered successfully!,Please wait for approval.")
                        return redirect('registerVendor')
                else:
                        print("Invalid Form")
                        print(form.errors)
        else:                                                
                form=UserForm()
                v_form=VendorForm()
        context={
                'form':form,
                'v_form':v_form,
        }
        return render(request,"accounts/registerVendor.html",context)
def login(request):
        if request.user.is_authenticated:
                messages.warning(request,"You are already loggedin!!")
                return redirect('myAccount')
        elif request.method =="POST":
                email=request.POST["email"]
                password=request.POST["password"]

                user=auth.authenticate(email=email,password=password)
                #return redirect('dashboard')
        
                if user is not None:
                        auth.login(request,user)
                        messages.success(request,"You are now logged in")
                        return redirect('myAccount')
                else:
                        messages.error(request,"Invalid Login Credentials")
                        return redirect('login')
        return render(request,"accounts/login.html")

def logout(request):
        auth.logout(request)
        messages.info(request,"You are logged out")
        return redirect('login')



@login_required(login_url='login')
def myAccount(request):
        user=request.user       #hi line cha aarta logged in user
        redirectUrl=detectUser(user)
        return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)        
def custdashboard(request):
        return render(request,"accounts/custdashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)  
def vendordashboard(request):
        return render(request,"accounts/vendordashboard.html")