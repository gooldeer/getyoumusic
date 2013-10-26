# Create your views here.

from celery.result import AsyncResult

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import simplejson as json
from django.utils.encoding import smart_str

import os

from youtubetomp3.core.jobs import convert
from youtubetomp3.core.jobs import download

from youtubetomp3.models import Playlist
from youtubetomp3.models import Media

from youtubetomp3.const.constants import _Const
CONST = _Const()

import youtubetomp3.core.utils as Utils


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
        job = convert.delay(request.POST['youtubeLink'], request.user)
        
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
    media_set = playlist.media_set.all()

    template = loader.get_template('youtubetomp3/playlist.html')
    context = RequestContext(request, {'playlist' : playlist, 'media_set' : media_set})

    return HttpResponse(template.render(context))

def audio(request, playlistName, media):
    
    response = HttpResponse(mimetype='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(media)
    response['Accept-Ranges'] = 'bytes'
    path = Utils.createPath(os.path.basename(media), request.user)
    response['X-Sendfile'] = smart_str(path)

    return response

def new_playlist(request):
    """ Create new playlist """
    user = request.user

    if 'playlist' in request.POST:
        playlistName = request.POST['playlist']

        if 'is_audio' in request.POST:
            is_audio = True
        else:
            is_audio = False

    if playlistName != None:
        playlist = Playlist.objects.create_playlist(name=playlistName, user=user, is_audio=is_audio)

    if (playlist != CONST.DUBLICATE):
        print 'created new playlist with name ' + playlist.name

    return HttpResponseRedirect(reverse('youtubetomp3:playlists'))

def remove_playlist(request, playlistName, is_audio):
    """ Remove playlist """

    user = request.user

    # Fucking sheet! In some way if is_audio==False, it is string 'False' instead of bool
    if is_audio == 'False':
        is_audio = False

    playlist = Playlist.objects.get(
        name=playlistName, user=user, is_audio=is_audio)

    for media in playlist.media_set.all():
        media.delete()

    playlist.delete()

    return HttpResponseRedirect(reverse('youtubetomp3:playlists'))

def remove_media(request, playlistName, media):
    """ Remove media """
    
    user = request.user
    playlist = user.playlist_set.get(name=playlistName, user=user)
    playlist.media_set.get(mediafile=media).delete()

    return HttpResponseRedirect(reverse('youtubetomp3:playlist', args=[playlistName,]))

def change_playlist(request, playlistName, name=None, color=None):
    
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

    return HttpResponse(playlist.color)

def add_media_to_playlist(request, playlist_name, media):
    """ Adds media to given playlist """
    user = request.user
    playlist_to_add = user.playlist_set.get(name=playlist_name, user=user)

    

    Media.objects.create_media(playlist=playlist_to_add, mediafile=media)
    return HttpResponse('Added')

