from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UploadVideoForm, NewCommentForm
from .models import Video, Comment

import json

def index(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', { 'videos': videos })

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            form.save_m2m()
            return HttpResponseRedirect('/videos/')
    else:
        form = UploadVideoForm()
    return render(request, 'videos/upload_video.html', { 'form': form })

def watch_video(request):
    video_id = request.GET.get('video_id', '')
    try:
        video_instance = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404("Video does not exist")
    return render(request, 'videos/watch_video.html', { 'video': video_instance })

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.creator = request.user
            new_comment.save()
            form.save_m2m()
            return HttpResponse()
        else:
            raise Exception("Adding comment failed.")
    elif request.method == 'GET':
        return get_comments(request)
    else:
        return HttpResponse().status_code(405)

def get_comments(request):
    video_id = request.GET.get('video_id', '')
    try:
        comments = Comment.objects.filter(video_id=video_id).order_by('timestamp')
        comments_list = []
        for comment in comments:
            comments_list.append({
                'id': comment.id,
                'creator': comment.creator.get_username(),
                'upvotes': comment.upvotes,
                'downvotes': comment.downvotes,
                'timestamp': comment.timestamp,
                'text': comment.text
            })
    except Comment.DoesNotExist:
        pass
    return JsonResponse({ 'comments': comments_list })
