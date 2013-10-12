import os

from pydub import AudioSegment

import youtubetomp3.core.utils as Utils

class Converter(object):
    """Converter from video to mp3"""

    def __init__(self, user):
        super(Converter, self).__init__()
        self.user = user

    def convert(self, path):
        filename = Utils.uniquify(Utils.getName(path) + '.mp3', self.user)
        AudioSegment.from_file(path).export(filename, format='mp3')
        os.remove(path)

        return filename

