from youtubetomp3.libs.pafy import Pafy
import youtubetomp3.core.utils as Utils
import youtubetomp3.libs.youtube_dl as youtube_dl

import os
from subprocess import call as Call

from youtubetomp3.const.constants import _Const
CONST = _Const()

class Downloader():
    """docstring for Downloader"""
    
    def __init__(self, link, user):
        self.link = link
        self.user = user
        self.path = Utils.createPath('', user)
    
    def download(self, call=None):
        
        # video = Pafy(self.link)
        # best = video.getbest(preftype=CONST.VIDEO_TO_PLAY_EXTENSION)
        # myfilename = Utils.uniquify(
        #     self.path + CONST.DEFAULT_MEDIA_NAME + '.' + best.extension)
        # myfilename = Utils.createPath(myfilename, self.user)
        # print myfilename
        # print "File to load: " + myfilename

        # var = Call([CONST.YOUTUBE_DL_PATH, self.link, 
        #     "-f", CONST.VIDEO_TO_PLAY_EXTENSION, 
        #     "-o", self.path + "%(title)s.%(ext)s"])

        # print var

        myfilename = Utils.uniquify(
            self.path + 
            CONST.DEFAULT_MEDIA_NAME + 
            '.' + CONST.VIDEO_TO_PLAY_EXTENSION)

        myfilename = Utils.createPath(myfilename, self.user)

        ydl = youtube_dl.YoutubeDL({
            'outtmpl': myfilename,
            'format': CONST.VIDEO_TO_PLAY_EXTENSION})
        # Add all the available extractors
        ydl.add_default_info_extractors()

        result = ydl.extract_info(self.link, download=True, callback=call)

        # if 'entries' in result:
        #     # Can be a playlist or a list of videos
        #     video = result['entries'][0]
        # else:
        #     # Just a video
        #     video = result

        # myfilename = video['title'] + '.' + video['ext']
        
        return Utils.createLink(os.path.basename(myfilename), self.user)
        # try:
        #     best.download(filepath=myfilename, callback=call, quiet=False)
        # except Exception:
        #     return None
        # else:
        #     pass
        # finally:
        #     return Utils.createLink(os.path.basename(myfilename), self.user)


