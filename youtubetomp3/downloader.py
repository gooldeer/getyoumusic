from youtubetomp3.pafy import Pafy

class Downloader():

	def download(self, link="", call=None):
		
		video = Pafy(link)
		best = video.getbest()
		myfilename = '/media/test.' + best.extension

		try:
			best.download(filepath=myfilename, callback=call, progress=False)
		finally:
			return myfilename
		

		