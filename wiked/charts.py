import numpy as np
import matplotlib.pyplot as plt
from os import path

import images_folder as imgf


def create_contributions_year_bar_chart(contributions: list, name: str):
    print("Creating bar chart of contributions per year...")

    timestamps = [contribution["timestamp"] for contribution in contributions]
    timestamps = sorted([timestamp[:4] for timestamp in timestamps])

    unique, counts = np.unique(timestamps, return_counts=True)

    plt.bar(unique, counts, 0.8, align='center')
    plt.title("Bar chart of all contributions")
    plt.xlabel("Year")
    plt.ylabel("Number of contributions")

    file = path.join(imgf.images_folder(), name)
    plt.savefig(file)
    print("Created %s" % file)
    print("Close the image window to continue")

    plt.show()
