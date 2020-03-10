from django.urls import re_path

from . import feed

websocket_urlpatterns = [
        re_path(r'ws/videos/comment/(?P<video_id>\w+)/$', feed.CommentFeed),
]
