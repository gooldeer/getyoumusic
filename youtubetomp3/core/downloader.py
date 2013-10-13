from youtubetomp3.libs.pafy import Pafy
import youtubetomp3.core.utils as Utils

class Downloader():
    """docstring for Downloader"""
    
    def __init__(self, link, user):
        self.link = link
        self.user = user
        self.path = Utils.createPath('', user)
    
    def download(self, call=None):
        
        video = Pafy(self.link)
        best = video.getbest(preftype='mp4', ftypestrict=False)
        # myfilename = '/media/track.' + best.extension
        myfilename = self.path + 'track.' + best.extension
        print myfilename

        try:
            best.download(filepath=myfilename, callback=call, quiet=False)
        except Exception:
            return None
        else:
            pass
        finally:
            return myfilename

