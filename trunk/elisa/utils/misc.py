import os

def file_is_picture(filename):
    path, extension = os.path.splitext(filename)
    # strip ext separator
    extension = extension[1:]
    extension = extension.lower()
    return extension in ('jpg', 'png', 'jpeg', 'gif')

