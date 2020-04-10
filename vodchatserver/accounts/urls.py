from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.signup, name='signup'),
    path('login', views.do_login, name='login'),
    path('logout', views.do_logout, name='logout'),
]
