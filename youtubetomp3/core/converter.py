import os

from pydub import AudioSegment

import youtubetomp3.core.utils as Utils

class Converter(object):
    """Converter from video to needed extension"""

    def __init__(self, user):
        super(Converter, self).__init__()
        self.user = user

    def convert(self, path, ext):
        filename = Utils.uniquify(Utils.getName(path) + '.' + ext)

        AudioSegment.from_file(path).export(
            Utils.createPath(filename, self.user), 
            format=ext)
        
        os.remove(path)

        return Utils.createLink(filename, self.user)

