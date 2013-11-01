import youtubetomp3.core.utils as Utils
import youtubetomp3.libs.youtube_dl as youtube_dl

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

        ydl.extract_info(self.link, download=True, callback=call)

        return Utils.createLink(os.path.basename(myfilename), self.user)

