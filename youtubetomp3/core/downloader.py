from youtubetomp3.libs.pafy import Pafy
import youtubetomp3.core.utils as Utils

import os

from youtubetomp3.const.constants import _Const
CONST = _Const()

class Downloader():
    """docstring for Downloader"""
    
    def __init__(self, link, user):
        self.link = link
        self.user = user
        self.path = Utils.createPath('', user)
    
    def download(self, call=None):
        
        video = Pafy(self.link)
        best = video.getbest(preftype=CONST.VIDEO_TO_PLAY_EXTENSION)
        myfilename = Utils.uniquify(
            self.path + CONST.DEFAULT_MEDIA_NAME + '.' + best.extension)
        myfilename = Utils.createPath(myfilename, self.user)
        print myfilename

        try:
            best.download(filepath=myfilename, callback=call, quiet=False)
        except Exception:
            return None
        else:
            pass
        finally:
            return Utils.createLink(os.path.basename(myfilename), self.user)

