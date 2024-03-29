# Create your views here.

from celery.result import AsyncResult

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import simplejson as json
from django.utils.encoding import smart_str

import os

from youtubetomp3.core.jobs import convert as converter
from youtubetomp3.core.jobs import download as downloader

from youtubetomp3.models import Playlist
from youtubetomp3.models import Media

from youtubetomp3.const.constants import _Const
CONST = _Const()

import youtubetomp3.core.utils as Utils


def index(request):
    return render(request, 'youtubetomp3/index.html')

def contacts(request):
    return render(request, 'youtubetomp3/footer/contacts.html')

def support(request):
    return render(request, 'youtubetomp3/footer/support.html')

def about(request):
    return render(request, 'youtubetomp3/footer/about.html')

def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state

    return HttpResponse(json.dumps(data), mimetype='application/json')

def download(request):
    """ A view to start a background job """
    job = downloader.delay(request.POST['youtubeLink'], request.user)    
    return HttpResponse(job)

def convert(request, stream):
    """ A view to start a background job """
    if stream == 'audio':
        job = converter.delay(request.POST['medialink'], request.user)
    else:
        job = converter.delay(request.POST['medialink'], request.user, 
            CONST.VIDEO_TO_LOAD_EXTENSION)
        
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

def audio(request, playlistName, media, mediatype):
    
    response = HttpResponse(mimetype=mediatype)
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
    playlist.media_set.get(link_to_play=media).delete()

    return HttpResponseRedirect(
        reverse('youtubetomp3:playlist', args=[playlistName,]))

def change_playlist(request, playlistName, name=None, color=None):
    
    user = request.user
    redirect = False
    playlist = user.playlist_set.get(name=playlistName, user=user)

    if name == None:
        name = playlist.name
    elif color == None:
        color = playlist.color
    elif 'playlist' in request.POST:
        redirect = True
        name = request.POST['playlist']

    if playlistName != CONST.DEFAULT_VIDEO_PLAYLIST and playlistName != CONST.DEFAULT_AUDIO_PLAYLIST: 
        playlist.name = name
    else:
        name = playlistName
        
    playlist.color = color
    playlist.save()

    pair = {'name': name, 'color': color}

    if redirect:
        return HttpResponseRedirect(
            reverse('youtubetomp3:playlist', args=[name,]))
    else:
        return HttpResponse(json.dumps(pair), mimetype='application/json')

def change_media(request, playlistName, mediaId):

    if 'playlist' in request.POST:
        medianame = request.POST['playlist']

    media = Media.objects.get(id=mediaId)

    for med in Media.objects.filter(link_to_play=media.link_to_play): 
        med.rename(medianame)
        media = med

    pair = { 'id': mediaId, 'name': medianame, 
             'link_to_play': media.link_to_play, 
             'link_to_load': media.link_to_load }

    return HttpResponse(json.dumps(pair), mimetype='application/json')

def add_media_to_playlist(request, playlist_name, media):
    """ Adds media to given playlist """
    user = request.user
    playlist_to_add = user.playlist_set.get(name=playlist_name, user=user)
    media_field = Media.objects.filter(link_to_play=media)[0]

    Media.objects.create_media(playlist=playlist_to_add, 
        name=media_field.name,
        link_to_play=media_field.link_to_play, 
        link_to_load=media_field.link_to_load)

    return HttpResponseRedirect(
        reverse('youtubetomp3:playlist', args=[playlist_name,]))

