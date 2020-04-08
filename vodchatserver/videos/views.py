from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .forms import UploadVideoForm, NewCommentForm, VoteForm
from .models import Video, Comment, Vote, Watch

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
    
    if request.user:
        print("saving...")
        watch = Watch(video=video_instance, watcher=request.user)
        watch.save()
    
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

            layer = get_channel_layer()

            room_group_name = 'video_%s' % new_comment.video_id.id

            async_to_sync(layer.group_send)(room_group_name, {
                'type': 'send.message',
                'message': {
                    'type': "NEW_COMMENT",
                    'comment': {
                        'id': new_comment.id,
                        'creator': new_comment.creator.get_username(),
                        'upvotes': 0,
                        'downvotes': 0,
                        'timestamp': new_comment.timestamp,
                        'text': new_comment.text
                    }
                }
            })
            return HttpResponse()
        else:
            raise Exception("Adding comment failed.")
    elif request.method == 'GET':
        return get_comments(request)
    else:
        response = HttpResponse()
        response.status_code = 405

        return response

def get_comments(request):
    video_id = request.GET.get('video_id', '')
    try:
        comments = Comment.objects.filter(video_id=video_id).order_by('timestamp')
        comments_list = []

        for comment in comments:

            upvotes = Vote.objects.filter(video_id=video_id, comment_id=comment.id, vote=1).count()
            downvotes = Vote.objects.filter(video_id=video_id, comment_id=comment.id, vote=-1).count()

            comments_list.append({
                'id': comment.id,
                'creator': comment.creator.get_username(),
                'upvotes': upvotes,
                'downvotes': downvotes,
                'timestamp': comment.timestamp,
                'text': comment.text
            })
    except Comment.DoesNotExist:
        pass
    return JsonResponse({ 'comments': comments_list })

@login_required
def vote(request):
    print(request.POST)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            new_vote = form.save(commit=False)
            new_vote.voter = request.user
            new_vote.save()
            form.save_m2m()

            layer = get_channel_layer()

            room_group_name = 'video_%s' % new_vote.video_id.id

            async_to_sync(layer.group_send)(room_group_name, {
                'type': 'send.message',
                'message': {
                    'type': 'UPVOTE' if new_vote.vote > 0 else 'DOWNVOTE',
                    'comment_id': new_vote.comment_id.id,
                }
            })

            return HttpResponse()
        else:
            raise Exception("Vote failed")
    else:
        response = HttpResponse()
        response.status_code = 405

        return response

def profile(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        users = User.objects.filter(username=username)

        if len(users) < 1:
            return Http404("No user {}.".format(username))

        user = users[0]
        videos = Video.objects.filter(creator_id=user.id)
        watches = Watch.objects.filter(watcher=user.id).order_by('-datetime')

        return render(request, 'videos/profile.html', { 'videos': videos, 'username': user.username, 'watches': watches })
    else:
        response = HttpResponse()
        response.status_code = 405

        return response

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        videos = Video.objects.filter(title__icontains=q)

        return render(request, 'videos/home.html', { 'videos': videos })
    else:
        response = HttpResponse()
        response.status_code = 405

        return response