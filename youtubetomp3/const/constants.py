def constant(f):
    """Function to defin constants"""
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    """Constants class"""
    @constant
    def DUBLICATE():
        return 'DUBLICATE'
    @constant
    def VIDEO_EXTENSION():
        return 'mp4'
    @constant
    def AUDIO_TO_PLAY_EXTENSION():
        return 'ogg'
    @constant
    def AUDIO_TO_LOAD_EXTENSION():
        return 'mp3'
    @constant
    def DEFAULT_MEDIA_NAME():
        return 'track'
    @constant
    def DEFAULT_AUDIO_PLAYLIST():
        return 'audios'
    @constant
    def DEFAULT_VIDEO_PLAYLIST():
        return 'videos'
