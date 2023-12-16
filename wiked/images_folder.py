import os
from os import path

GENERATED_IMG_FOLDER = "generated_images"


def images_folder() -> str:
    curr_directory = directory()

    folder_path = path.join(curr_directory, GENERATED_IMG_FOLDER)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def directory():
    if "__file__" in locals():
        curr_directory = path.dirname(__file__)
    else:
        curr_directory = os.getcwd()

    return curr_directory
