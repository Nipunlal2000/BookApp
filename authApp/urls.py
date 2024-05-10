from django.urls import path
from . import views

urlpatterns = [

    path('',views.Home, name='home'),
    path('signup/',views.SignupPage, name='signup'),
    path('login/', views.LoginPage,name='login'),
    path('logout/', views.LogOut, name='logout'),

]
