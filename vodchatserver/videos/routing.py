from django.urls import path, re_path

from . import feed

websocket_urlpatterns = [
        path('ws/feed/<str:video_id>/', feed.Feed),
]
