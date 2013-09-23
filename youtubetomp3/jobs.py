from celery import task, current_task

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

	playlist_field = Playlist.objects.create_playlist(name='default', user=current_user, is_audio=False)
	
	if playlist_field == "DUBLICATE" :
		playlist_field = Playlist.objects.get(name='default', user=current_user, is_audio=False)

	mediafield = Media(mediafile=filename, playlist=playlist_field)
	mediafield.save()

