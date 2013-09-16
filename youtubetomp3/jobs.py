from celery import task, current_task
from celery.result import AsyncResult

from time import sleep

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
	filename = downloader.download(link=url, call=downloading)
	print filename

	playlist_field = Playlist(name='default', user=current_user, is_audio=False)
	playlist_field.save()

	mediafield = Media(mediafile=filename, playlist=playlist)
	mediafield.save()

