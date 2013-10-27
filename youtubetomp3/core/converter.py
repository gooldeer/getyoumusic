import os

from pydub import AudioSegment

import youtubetomp3.core.utils as Utils

class Converter(object):
    """Converter from video to needed extension"""

    def __init__(self, user):
        super(Converter, self).__init__()
        self.user = user

    def convert(self, path, ext, remove=True):
        path = Utils.createPath(os.path.basename(path), self.user)
        filename = Utils.uniquify(Utils.getName(path) + '.' + ext)

        video = AudioSegment.from_file(path)
        path_to_convert = Utils.createPath(filename, self.user)

        if ext == 'ogg':
            video.export(path_to_convert, format=ext, 
                codec="libvorbis", parameters=["-aq", "50"])
        else:
            video.export(path_to_convert, format=ext)

        # AudioSegment.from_file(path).export(
        #     Utils.createPath(filename, self.user), 
        #     format=ext, codec="libvorbis", parameters=["-aq", "50"])

        # AudioSegment.from_file(path).export(
        #     Utils.createPath(filename, self.user), 
        #     format=ext)

        if remove:
            os.remove(path)

        return Utils.createLink(filename, self.user)

