from django.contrib import admin
from django.urls import path
from .import views

urlpatterns=[
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myAccount/',views.myAccount,name="myAccount"),
    path('custdashboard/',views.custdashboard,name='custdashboard'),
    path('vendordashboard/',views.vendordashboard,name='vendordashboard'),

    #send verification link
    path('activate/<uidb64>/<token>',views.activate,name='activate'),

    path('forget_password/',views.forget_password,name='forget_password'),
    path('forget_password_validate/<uidb64>/<token>',views.forget_password_validate,name='forget_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),

]
