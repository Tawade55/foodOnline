from django.shortcuts import get_object_or_404,render,redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from accounts.models import userprofile
from .models import Vendor
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category
from menu.models import FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify

# Create your views here.

def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor


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

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def menu_builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor).order_by('created_at')
    context={
        'categories':categories,
    }
    return render(request,"vendor/menu_builder.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def fooditems_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(vendor=vendor,category=category)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    print(fooditems)
    return render(request,"vendor/fooditems_by_category.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def add_category(request):
    if request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']    #hyat html madhe input ghetlau aapan categoru name cha ani slug sathi ikde paije input manun joh html madhla data aahe tyala ikde as a cleaned data ghetlay
            category=form.save(commit=False)    #data about to be save but not stored 
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)           
            form.save()
            messages.success(request,"Category Added Successfully")
            return redirect('menu_builder')
        
        else:
            #print(form.errors)
            messages.warning(request,"Oops!!This category all ready exists")
            return redirect('add_category')

    else:
        form=CategoryForm()
        
                            
    
    context={
        'form':form,
    }
    return render(request,"vendor/add_category.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=="POST":
        form=CategoryForm(request.POST,instance=category)   #from the above primary key we get a instance that need to be passed in form this instance will keep the existing data manje edit karshil teva paila je naav aahe category cha description aahe te edit karaychya aadi disnaar aaplya la
        if form.is_valid():
            category_name=form.cleaned_data['category_name']    #hyat html madhe input ghetlau aapan categoru name cha ani slug sathi ikde paije input manun joh html madhla data aahe tyala ikde as a cleaned data ghetlay
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)           
            form.save()
            messages.success(request,"Category Updated Successfully")
            return redirect('menu_builder')
        
        else:
            #print(form.errors)
            messages.warning(request,"Oops!!Changes didn't reflect,try again")
            return redirect('edit_category')

    else:
        form=CategoryForm(instance=category)
        
                            
    
    context={
        'form':form,
        'category':category,
    }
    return render(request,"vendor/edit_category.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,"Category Deleted Successfully!")
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def add_food(request):
    if request.method=="POST":
        form=FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']    #hyat html madhe input ghetlau aapan categoru name cha ani slug sathi ikde paije input manun joh html madhla data aahe tyala ikde as a cleaned data ghetlay
            food=form.save(commit=False)    #data about to be save but not stored 
            food.vendor=get_vendor(request)
            food.slug=slugify(foodtitle)           
            form.save()
            messages.success(request,"Food Item Added Successfully")
            return redirect('fooditems_by_category',food.category.id)
        
        else:
            #print(form.errors)
            messages.warning(request,"Oops!!This category all ready exists")
            return redirect('add_food')

    else:
        form=FoodItemForm()
        #modify this form
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form,
    }
    return render(request,'vendor/add_food.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def edit_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    if request.method=="POST":
        form=FoodItemForm(request.POST,request.FILES,instance=food)   #from the above primary key we get a instance that need to be passed in form this instance will keep the existing data manje edit karshil teva paila je naav aahe category cha description aahe te edit karaychya aadi disnaar aaplya la
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']    #hyat html madhe input ghetlau aapan categoru name cha ani slug sathi ikde paije input manun joh html madhla data aahe tyala ikde as a cleaned data ghetlay
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(foodtitle)           
            form.save()
            messages.success(request,"Food Item Updated Successfully")
            return redirect('fooditems_by_category',food.category.id)
        
        else:
            #print(form.errors)
            messages.warning(request,"Oops!!Changes didn't reflect,try again")
            return redirect('edit_food')

    else:
        form=FoodItemForm(instance=food)
        #modify this form
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form,
        'food':food,
    }
    return render(request,"vendor/edit_food.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def delete_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,"Food Item Deleted Successfully!")
    return redirect('fooditems_by_category',food.category.id)

    
