from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_video, name='upload'),
    path('watch', views.watch_video, name='watch'),
    path('comment', views.add_comment, name='comment'),
    path('vote', views.vote, name='vote'),
]

app_name = 'videos'
