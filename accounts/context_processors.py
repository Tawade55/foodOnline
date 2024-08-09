from vendor.models import Vendor
from django.conf import settings
def get_vendor(request):
    try:
        vendor=Vendor.objects.get(user=request.user)  #fetching logged in user details
    except:
        vendor=None
    return dict(vendor=vendor)

def get_google_api(request):
    return {'GOOGLE-API-KEY':settings.GOOGLE_API_KEY}