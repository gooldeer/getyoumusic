from youtubetomp3.pafy import Pafy

class Downloader():

	def download(self, link="", call=None):
		
		video = Pafy(link)
		best = video.getbest()
		myfilename = 'test.' + best.extension
		best.download(filepath=myfilename, callback=call)

		return myfilename