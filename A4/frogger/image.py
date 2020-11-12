import os


def get_image_path(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img', filename)
