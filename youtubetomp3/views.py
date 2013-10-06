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

def playlist(request, playlistName):
    """ Media playlist """
    user = request.user
    playlist = user.playlist_set.get(name=playlistName, user=user)
    media_set = playlist.media_set

    template = loader.get_template('youtubetomp3/playlist.html')
    context = RequestContext(request, {'playlist' : playlist, 'media_set' : media_set})

    return HttpResponse(template.render(context))

def new_playlist(request):
    """ Create new playlist """
    user = request.user

    if 'playlist' in request.POST:
        playlistName = request.POST['playlist']

    if playlistName != None:
        playlist = Playlist.objects.create_playlist(name=playlistName, user=user, is_audio=False)

    if (playlist != "DUBLICATE"):
        print 'created new playlist with name ' + playlist.name

    return HttpResponseRedirect(reverse('youtubetomp3:playlists'))

def remove_playlist(request, playlistName):
    """ Remove playlist """

    user = request.user
    Playlist.objects.get(name=playlistName, user=user, is_audio=False).delete()

    return HttpResponseRedirect(reverse('youtubetomp3:playlists'))

def remove_media(request, playlistName, media):
    """ Remove media """
    
    user = request.user
    playlist = user.playlist_set.get(name=playlistName, user=user)

    playlist.media_set.get(mediafile=media).delete()

    return HttpResponseRedirect(reverse('youtubetomp3:playlist', args=[playlistName,]))

def change_playlist(request, playlistName, name=None, color=None):

    # user = request.user
    user = request.user
    playlist = user.playlist_set.get(name=playlistName, user=user)

    if name == None:
        name = playlist.name
    else:
        if color == None:
            color = playlist.color

    playlist.name = name
    playlist.color = color
    playlist.save()

    # playlist.update(name=name, color=color)

    return HttpResponseRedirect(reverse('youtubetomp3:playlist', args=[playlist.name,]))