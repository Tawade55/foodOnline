
from django.contrib import admin
from django.urls import path
from .import views	#. manje tyach directory madhe views aahe jya directory madhe urls aaeht

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home name="home"),	
]
