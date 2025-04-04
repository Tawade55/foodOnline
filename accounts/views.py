import datetime
from django.shortcuts import render,HttpResponse,redirect

from orders.models import Order
from .forms import UserForm
from .models import User,userprofile
from vendor.forms import VendorForm
from django.contrib import messages,auth
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
#from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify

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

                        #send verification link
                        mail_subject="Activate your Account"
                        email_template='accounts/emails/account_verification_email.html'
                        send_verification_email(request,user,mail_subject,email_template)
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
                return redirect('myAccount')
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
                        vendor_name=v_form.cleaned_data['vendor_name']
                        vendor.vendor_slug=slugify(vendor_name)+'-'+str(user.id)
                        user_profile=userprofile.objects.get(user=user)
                        vendor.user_profile=user_profile
                        vendor.save()

                        #send verification link
                        mail_subject="Activate your Account"
                        email_template='accounts/emails/account_verification_email.html'
                        send_verification_email(request,user,mail_subject,email_template)
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

def activate(request,uidb64,token):
        #Activate the user by setting the is_active status

        try:
                uid=urlsafe_base64_decode(uidb64).decode()
                user=User._default_manager.get(pk=uid)   #match kela primary key la with the UID
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None

        if user is not None and default_token_generator.check_token(user,token):        #check kela user cha token no match hotoy ki nahi te
                user.is_active=True
                user.save()
                messages.success(request,"Congratulations your account is activated")
                return redirect('myAccount')
        else:
                messages.error(request,"Invalid link")
                return redirect('myAccount')

        




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
        orders=Order.objects.filter(user=request.user,is_ordered=True)
        recent_orders=orders[:5]
        order_count=orders.count()
        context={
                'orders':orders,
                'order_count':order_count,
                'recent_orders':recent_orders
        }
        return render(request,"accounts/custdashboard.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)  
def vendordashboard(request):
        vendor=Vendor.objects.get(user=request.user)
        orders=Order.objects.filter(vendors__in=[vendor.id],is_ordered=True).order_by('-created_at')
        recent_orders=orders[:5]

        #current Month
        current_month=datetime.datetime.now().month
        current_month_orders=orders.filter(vendors__in=[vendor.id],created_at__month=current_month)
        current_month_revenue=0
        for i in current_month_orders:
                current_month_revenue+=i.get_total_by_vendor()['grand_total']        
        
        #total revenue
        total_revenue=0
        for i in orders:
                total_revenue+=i.get_total_by_vendor()['grand_total']
        context={
                'orders':orders,
                'orders_count':orders.count(),
                'recent_orders':recent_orders,
                'total_revenue':total_revenue,
                'current_month_revenue':current_month_revenue,
        }
        return render(request,"accounts/vendordashboard.html",context)

def forget_password(request):
        if request.method=="POST":
                email=request.POST["email"]

                if User.objects.filter(email=email).exists():
                        user=User.objects.get(email__exact=email)

                        #send reset password email
                        mail_subject="Reset your Password"
                        email_template='accounts/emails/reset_password_email.html'
                        send_verification_email(request,user,mail_subject,email_template)
                        messages.success(request,"Password reset link has been sent to you!")
                        return redirect('login')
                else:
                        messages.error(request,"User Does Not Exist")
                        return redirect('forget_password')   
        return render(request,"accounts/forget_password.html")

def forget_password_validate(request,uidb64,token):
        #Activate the user by setting the is_active status

        try:
                uid=urlsafe_base64_decode(uidb64).decode()
                user=User._default_manager.get(pk=uid)   #match kela primary key la with the UID
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None

        if user is not None and default_token_generator.check_token(user,token):        #check kela user cha token no match hotoy ki nahi te
                request.session['uid']=uid      #apli pk hya session madhe store hote
                messages.info(request,"Please reset your password")
                return redirect('reset_password')
        else:
                messages.error(request,"Link has been expired")
                return redirect('myAccount')

def reset_password(request):
        if request.method=="POST":
                password=request.POST['password']
                confirm_password=request.POST['confirm_password']

                if password==confirm_password:
                        pk=request.session.get('uid')   #hyat uid chi pk ghetli aahe aani match kela ki hya user chi hich pk aahe ka ani mag tyacha password reset kelay
                        user=User.objects.get(pk=pk)
                        user.set_password(password)
                        user.is_active=True
                        user.save()
                        messages.success(request,"Password Reset Successfully")
                        return redirect('login')
                        
                else:
                        messages.error(request,"Password did not match")
                        return redirect("reset_password")

        return render(request,"accounts/reset_password.html")


