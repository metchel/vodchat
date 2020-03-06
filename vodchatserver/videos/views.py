from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import UploadVideoForm
from .models import Video

def index(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', { 'videos': videos })

def upload_video(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
