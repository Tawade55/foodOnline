from django.shortcuts import render,get_object_or_404
from vendor.models import Vendor
from menu.models import Category
from menu.models import FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .context_processors import get_cart_counter,get_cart_amounts
from .models import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count=vendors.count()
    context={
		'vendors':vendors,
        'vendor_count':vendor_count,
	}
    return render(request,"marketplace/listings.html",context)

def vendor_detail(request,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)

    categories=Category.objects.filter(vendor=vendor).prefetch_related( #aata bagh ikde ghetlay tya prefetch la je related_name mule aalay karan tech aahe ikde tyanna tech fooditems dakvayche aahet je available aahet
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,"marketplace/vendor_detail.html",context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if fooditem exist
            try:
                fooditem=FoodItem.objects.get(id=food_id)
                #check if the user has already added that food into the cart
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)

                    chkCart.quantity +=1
                    chkCart.save()
                    return JsonResponse({'status':'Success','message':'Increased the cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    chkCart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the food to the cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed','message':'This Food does not exist!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
        

    else:
        return JsonResponse({"status":"login_required",'message':'please login to continue'})
    
    #return HttpResponse(food_id)

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if fooditem exist
            try:
                fooditem=FoodItem.objects.get(id=food_id)
                #check if the user has already added that food into the cart
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkCart.quantity>1:

                        chkCart.quantity -=1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity=0
                    return JsonResponse({'status':'Success','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    
                    return JsonResponse({'status':'Failed','message':'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status':'Failed','message':'This Food does not exist!'})
        else:
            return JsonResponse({'status':'login_required','message':'Invalid request!'})
        

    else:
        return JsonResponse({"status":"Failed",'message':'please login to continue'})
        #return HttpResponse(food_id)
    #return JsonResponse({"status":"Failed",'message':'please login to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    context={
        'cart_items':cart_items,
    }
    return render(request,"marketplace/cart.html",context)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            try:
                #checck if the cart item exists
                cart_item=Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item has been deleted!','cart_counter':get_cart_counter(request),'cart_amount':get_cart_amounts(request)})
            except: 
                return JsonResponse({'status':'Failed','message':'Cart item does not exist!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request!'})

