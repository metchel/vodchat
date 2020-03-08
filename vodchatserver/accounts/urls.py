from django.urls import path
from . import views

urlpatterns = [
    path('',views.signup, name='signup'),
    path('login', views.do_login, name='login'),
    path('logout', views.do_logout, name='logout'),
]
