# Create your views here.

from celery.result import AsyncResult

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import simplejson as json

from youtubetomp3.jobs import download
from youtubetomp3.models import Playlist

def index(request):
    """ Index page view """
    return render(request, 'youtubetomp3/index.html')

def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state
    print data

    return HttpResponse(json.dumps(data), mimetype='application/json')

def init_work(request):
    """ A view to start a background job """
    if 'youtubeLink' in request.POST:
        job = download.delay(request.POST['youtubeLink'], request.user)
        
    return HttpResponse(job)

def playlists(request):
    """ Users playlists """
    template = loader.get_template('youtubetomp3/playlists.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def profile(request):
    """ A profile view """
    template = loader.get_template('profiles/profile_detail.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))

def playlist(request):
    """ Media playlist """
    user = request.user

    if 'playlist' in request.GET:
        playlist_name = request.GET['playlist']
    else:
        return HttpResponse('No playlist given')

    current_playlist = user.playlist_set.get(name=playlist_name, user=user)
    media_set = current_playlist.media_set

    template = loader.get_template('youtubetomp3/playlist.html')
    context = RequestContext(request, 
        {'playlist' : current_playlist, 'media_set' : media_set})

    return HttpResponse(template.render(context))

def new_playlist(request):
    """ Create new playlist """
    user = request.user

    if 'playlist' in request.POST:
        playlist_name = request.POST['playlist']
    else:
        return HttpResponse('No playlist given')

    plst = Playlist.objects.create_playlist(
        name=playlist_name, user=user, is_audio=False)

    if (plst != "DUBLICATE"):
        print 'created new playlist with name ' + plst.name

    return HttpResponseRedirect(reverse('profile_detail'))
