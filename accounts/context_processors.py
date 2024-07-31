from vendor.models import Vendor
def get_vendor(request):
    try:
        vendor=Vendor.objects.get(user=request.user)  #fetching logged in user details
    except:
        vendor=None
    return dict(vendor=vendor)