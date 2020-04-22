from django import forms
from .models import Video, Comment, Vote

class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'videofile', 'thumbnailfile']
        labels = {
            'title': "Title",
            'description': "Description",
            'videofile': "Video (.mp4, .mov)",
            'thumbnailfile': "Thumbnail (.jpg, .png)"
        }

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['video_id', 'timestamp', 'text']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['video_id', 'comment_id', 'vote']
