from celery import task, current_task
from celery.result import AsyncResult

from time import sleep

from youtubetomp3.downloader import Downloader
from youtubetomp3.models import Media

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

	field = Media(mediafile=filename, user=current_user)
	field.save()

