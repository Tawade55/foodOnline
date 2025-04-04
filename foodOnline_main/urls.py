
from django.contrib import admin
from django.urls import path,include
from .import views	#. manje tyach directory madhe views aahe jya directory madhe urls aaeht
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),	
    path("accounts/",include('accounts.urls')),

    path('marketplace/',include("marketplace.urls")),

    path('cart/', MarketplaceViews.cart,name='cart'),

    

    #checkout
    path('checkout/',MarketplaceViews.checkout,name='checkout'),

    #Orders
    path('orders/',include("orders.urls")),
    path('search/',MarketplaceViews.search,name="search"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
