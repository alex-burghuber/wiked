import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from os import path
from wordcloud import WordCloud

JKU_CLOUD_FILE_NAME = "jku_cloud.png"
GENERATED_IMG_FOLDER = "generated_images"


def make_word_cloud(text: str, name: str):
    print("Generating word cloud...")

    word_cloud = WordCloud()
    word_cloud.generate(text)

    word_cloud.to_file(path.join(__images_folder(), name))

    print("Created %s" % name)
    print("Close the image window to continue")

    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def make_jku_logo_masked_world_cloud(text: str):
    print("Generating jku masked word cloud...")

    directory = __directory()

    jku_mask = np.array(Image.open(path.join(directory, "jku_mask.png")))
    word_cloud = WordCloud(
        background_color="black",
        max_words=2000,
        mask=jku_mask,
        contour_width=3,
        contour_color='black',
        collocations=False,
        regexp=r"\w+(?:[-:]+(?:\w+)?)*"
    )

    word_cloud.generate(text)

    word_cloud.to_file(path.join(__images_folder(), JKU_CLOUD_FILE_NAME))

    print("Created %s" % JKU_CLOUD_FILE_NAME)
    print("Close the image window to continue")

    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def __images_folder() -> str:
    directory = __directory()

    folder_path = path.join(directory, GENERATED_IMG_FOLDER)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def __directory():
    if "__file__" in locals():
        directory = path.dirname(__file__)
    else:
        directory = os.getcwd()

    return directory
