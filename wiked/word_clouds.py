import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from os import path
from wordcloud import WordCloud

import images_folder as imgf

JKU_CLOUD_FILE_NAME = "jku_cloud.png"


def make_word_cloud(text: str, name: str):
    print("Generating word cloud...")

    word_cloud = WordCloud()
    word_cloud.generate(text)

    word_cloud.to_file(path.join(imgf.images_folder(), name))

    print("Created %s" % name)
    print("Close the image window to continue")

    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def make_jku_logo_masked_world_cloud(text: str):
    print("Generating jku masked word cloud...")

    directory = imgf.directory()

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

    word_cloud.to_file(path.join(imgf.images_folder(), JKU_CLOUD_FILE_NAME))

    print("Created %s" % JKU_CLOUD_FILE_NAME)
    print("Close the image window to continue")

    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
