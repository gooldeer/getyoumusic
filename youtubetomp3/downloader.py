from youtubetomp3.pafy import Pafy

class Downloader():
    """docstring for Downloader"""
    
    def download(self, link='', call=None):
        
        video = Pafy(link)
        best = video.getbest()
        myfilename = '/media/test.' + best.extension
        print myfilename

        try:
            best.download(filepath=myfilename, callback=call, progress=True)
        except Exception:
            return None
        else:
            pass
        finally:
            return myfilename
