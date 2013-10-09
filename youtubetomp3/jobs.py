from celery import task, current_task
import os
from pydub import AudioSegment

from youtubetomp3.downloader import Downloader
from youtubetomp3.models import Media
from youtubetomp3.models import Playlist

@task(name="jobs.download")
def download(url, current_user):
	"Download video file from youtube directly on server"

	def downloading(progress):
			percent = progress * 100
			current_task.update_state(state='PROGRESS',
            	meta={'current': percent, 'total': 100})

	downloader = Downloader()
	d = downloader.download(link=url, call=downloading)
	print d + ' downloaded'

	filename = convert(d)
	print filename + 'converted'

	playlist_field = Playlist.objects.create_playlist(name='default', user=current_user, is_audio=True)
	
	if playlist_field == "DUBLICATE" :
		playlist_field = Playlist.objects.get(name='default', user=current_user, is_audio=True)

	if filename != None:
		Media.objects.create_media(playlist=playlist_field, mediafile=filename)

def convert(url):
	""" Convert video to mp3 """
	filename = getName(url) + '.mp3'
	AudioSegment.from_file(url).export(filename, format='mp3')
	os.remove(url)

	return filename

def getName(url):
	return os.path.splitext(url)[0]

