import os
import tempfile
import itertools as IT

from django.conf import settings

# Creates track + number name of file. Source: http://stackoverflow.com/questions/13852700/python-create-file-but-if-name-exists-add-number
def uniquify(path, sep = ''):
    """ Uniq filenames """
    print 'path : ' + path

    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))

    orig = tempfile._name_sequence 

    if os.path.exists(path):

        with tempfile._once_lock:
            tempfile._name_sequence = name_sequence()
            path = os.path.normpath(path)
            dirname, basename = os.path.split(path)
            filename, ext = os.path.splitext(basename)
            print dirname
            print basename
            print filename
            fd, path = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
            tempfile._name_sequence = orig

        os.close(fd)

    return os.path.basename(path)

def getName(url):
    return os.path.splitext(url)[0]

def createPath(path, current_user):
    directory = settings.MEDIA_ROOT + current_user.username + '/'

    if not os.path.exists(directory):
        os.makedirs(directory)
    return  directory + path

def createLink(path, current_user):
    return settings.MEDIA_URL + current_user.username + '/' + path
    