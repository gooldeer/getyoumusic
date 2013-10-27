import os

from pydub import AudioSegment
from subprocess import call

import youtubetomp3.core.utils as Utils

class Converter(object):
    """Converter from video to needed extension"""

    def __init__(self, user):
        super(Converter, self).__init__()
        self.user = user

    def convert(self, path, ext):
        path = Utils.createPath(os.path.basename(path), self.user)
        filename = Utils.uniquify(Utils.getName(path) + '.' + ext)

        video = AudioSegment.from_file(path)
        path_to_convert = Utils.createPath(filename, self.user)

        if ext == 'ogg':
            video.export(path_to_convert, format=ext, 
                codec="libvorbis", parameters=["-aq", "50"])
        elif ext == 'mp4':
            call(["ffmpeg", "-i", path, "-vcodec", "libx264", "-preset", "ultrafast", "-b:v", "768k",  path_to_convert])
        else:
            video.export(path_to_convert, format=ext)

        return Utils.createLink(filename, self.user)

