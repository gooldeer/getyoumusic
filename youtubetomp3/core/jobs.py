from celery import task, current_task

from youtubetomp3.core.downloader import Downloader
from youtubetomp3.core.converter import Converter

from youtubetomp3.models import Media
from youtubetomp3.models import Playlist

from youtubetomp3.const.constants import _Const
CONST = _Const()

@task(name="jobs.download")
def download(url, current_user):
    "Download video file from youtube directly on server"
    print 'downloading...'

    def downloading(total, *progress_stats):
        percent = progress_stats[1] * 100
        current_task.update_state(state='PROGRESS',
            meta={'current': percent, 'total': 100})

    downloader = Downloader(link=url, user=current_user)
    filename = downloader.download(call=downloading)
    print filename + ' downloaded'
    filename_to_load = filename
    filename_to_load = Converter(current_user).convert(filename, "mp4")
    print filename_to_load + " converted"

    playlist_field = create_default_playlist(current_user, False)

    if filename != None:
        Media.objects.create_media(playlist=playlist_field, 
            link_to_play=filename, link_to_load=filename_to_load)

    return filename


@task(name="jobs.convert")
def convert(path, current_user):
    "Convert video file to audio"
    print 'converting...'

    current_task.update_state(state='PROGRESS')

    filename_to_play = Converter(current_user).convert(path, 
        CONST.AUDIO_TO_PLAY_EXTENSION)
    print filename_to_play + " converted"
    filename_to_load = Converter(current_user).convert(path, 
        CONST.AUDIO_TO_LOAD_EXTENSION)
    print filename_to_load + " converted"
    
    current_user.playlist_set.get(
        name=CONST.DEFAULT_VIDEO_PLAYLIST).media_set.get(
        link_to_play=path).delete()

    playlist_field = create_default_playlist(current_user, True)

    if filename_to_play != None:
        Media.objects.create_media(playlist=playlist_field, 
            link_to_play=filename_to_play, link_to_load=filename_to_load)
        
    return filename_to_play


def create_default_playlist(user, is_audio):
    """ Creates default playlist if it's not exitst """
    if is_audio:
        name = CONST.DEFAULT_AUDIO_PLAYLIST
    else:
        name = CONST.DEFAULT_VIDEO_PLAYLIST

    playlist_field = playlist_field = Playlist.objects.create_playlist(
        name=name, user=user, is_audio=is_audio)

    if playlist_field == CONST.DUBLICATE :
        playlist_field = Playlist.objects.get(
            name=name, user=user, is_audio=is_audio)

    return playlist_field
