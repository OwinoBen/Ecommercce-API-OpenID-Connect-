import os
import random


def property_image_path(instance, filename):
    return '/'.join(['property_images', filename])


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return f"property_images/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )
