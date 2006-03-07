import os

def file_extension_matches(filename, pattern_list):
    path, extension = os.path.splitext(filename)
    # strip ext separator
    extension = extension[1:]
    extension = extension.lower()
    return extension in pattern_list

def file_is_picture(filename):
    return file_extension_matches(filename,('jpg', 'png', 'jpeg', 'gif'))

def file_is_movie(filename):
    return file_extension_matches(filename,('avi','mov'))
    
