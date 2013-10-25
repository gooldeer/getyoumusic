from celery import task, current_task

from youtubetomp3.core.downloader import Downloader
from youtubetomp3.core.converter import Converter

from youtubetomp3.models import Media
from youtubetomp3.models import Playlist

@task(name="jobs.convert")
def convert(url, current_user):
    "Download video file from youtube directly on server"
    print 'working...'

    def downloading(total, *progress_stats):
        percent = progress_stats[1] * 100
        current_task.update_state(state='PROGRESS',
            meta={'current': percent, 'total': 100})

    downloader = Downloader(link=url, user=current_user)
    dlr = downloader.download(call=downloading)
    print dlr + ' downloaded'

    extension = 'mp3'
    filename = Converter(current_user).convert(dlr, extension)
    print filename + ' converted'

    playlist_field = create_default_playlist(current_user, True)

    if filename != None:
        Media.objects.create_media(playlist=playlist_field, mediafile=filename)
        
    return filename


def create_default_playlist(user, is_audio):
    """ Creates default playlist if it's not exitst """
    if is_audio:
        name = 'audios'
    else:
        name = 'videos'

    playlist_field = playlist_field = Playlist.objects.create_playlist(
        name=name, user=user, is_audio=is_audio)

    if playlist_field == "DUBLICATE" :
        playlist_field = Playlist.objects.get(
            name=name, user=user, is_audio=is_audio)

    return playlist_field
