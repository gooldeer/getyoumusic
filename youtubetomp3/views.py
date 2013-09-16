# Create your views here.

from celery.result import AsyncResult

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson as json

from youtubetomp3.jobs import download

def index(request):
	return render(request, 'youtubetomp3/index.html')

def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state

    return HttpResponse(json.dumps(data), mimetype='application/json')

def init_work(request):
    """ A view to start a background job """
    if 'youtubeLink' in request.POST:
    	job = download.delay(request.POST['youtubeLink'], request.user)
        
    return HttpResponse(job)

def profile(request):
    """ A profile view """
    template = loader.get_template('youtubetomp3/profiles/profile_detail.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def media(request):
    """ Media playlist """
    user = request.user

    if 'playlist' in request.GET:
        playlistName = request.GET['playlist']
    else:
        return HttpResponse('No playlist given')

    playlist = user.playlist_set.get(name=playlistName, user=user)
    media_set = playlist.media_set

    template = loader.get_template('youtubetomp3/profiles/playlist.html')
    context = RequestContext(request, {'playlist' : playlist, 'media_set' : media_set})

    return HttpResponse(template.render(context))