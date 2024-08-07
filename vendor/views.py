from django.shortcuts import get_object_or_404,render,redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from accounts.models import userprofile
from .models import Vendor
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)  
def vprofile(request):
    profile=get_object_or_404(userprofile,user=request.user)#userprofile cha data fetch kela same with vendor
    vendor=get_object_or_404(Vendor,user=request.user)

    if request.method=="POST":
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"Your Restaurant Details have been modified")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)  #heh ikde aadi forms banavle ani vprofile var render kele nantar var object valya line madhe tyancha data fetch kelay
        vendor_form=VendorForm(instance=vendor)
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,"vendor/vprofile.html",context)
