from django import forms
from .models import Video, Comment

class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'videofile']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['video_id', 'timestamp', 'text']
