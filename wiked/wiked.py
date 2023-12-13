#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import requests
import json
import numpy as np
from PIL import Image
from os import path
from wordcloud import WordCloud


def make_word_cloud(text):
    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40, min_font_size=15).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def make_jku_logo_masked_world_cloud(text):
    print("Generating word cloud...")

    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    jku_mask = np.array(Image.open(path.join(d, "jku_mask.png")))

    wc = WordCloud(background_color="black", max_words=2000, mask=jku_mask, contour_width=3, contour_color='black',
                   collocations=False, regexp=r"\w+(?:[-:]+(?:\w+)?)*")

    wc.generate(text)

    wc.to_file(path.join(d, "jku_cloud.png"))

    print("Done")

    plt.figure()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def get_all_contributions_of_ip_range(iprange: str) -> list:
    params = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uciprange": iprange,
        "uclimit": 250,  # Can't use 500, a request timeout can occur with that value
        "ucdir": "newer",
        "formatversion": 2,
        "ucnamespace": "*"
    }

    de_contributions = query_contributions(params, "de")
    en_contributions = query_contributions(params, "en")

    all_contributions = de_contributions + en_contributions
    print("Loaded total of %s contributions" % len(all_contributions))

    return all_contributions


def query_contributions(given_params: {}, language_code: str) -> list:
    contributions = []
    last_continue = {}

    while True:
        params = given_params.copy()

        if last_continue:
            params['uccontinue'] = last_continue['uccontinue']

        print("Loading next contributions page with params: %s" % params)
        result = requests.get(url='https://%s.wikipedia.org/w/api.php' % language_code, params=params)
        print("Received result from %s" % result.url)

        result_data = result.json()

        if 'error' in result_data:
            raise Exception(result_data['error'])
        if 'warnings' in result_data:
            print(result_data['warnings'])
        if 'query' in result_data:
            contributions.extend(result_data["query"]["usercontribs"])
        if 'continue' not in result_data:
            break

        last_continue = result_data['continue']

    print("Loaded %s %s.wikipedia.org contributions" % (len(contributions), language_code))

    return contributions


def cache_contributions(contributions: list):
    with open("contributions.json", "w") as outfile:
        json.dump(contributions, outfile, indent=2)


JKU_IP_RANGE = "140.78.0.0/16"


def main():
    print(
        "Wiked (Wikipedia Edits) will create a word cloud of the wikipedia site titles of all contributions that were "
        "made with an ip address belonging to the JKU campus network.\nEnter any key to use locally cached values "
        "or enter 'r' to refresh from the web.")
    key = input()

    if key.lower() == 'r':
        contributions = get_all_contributions_of_ip_range(JKU_IP_RANGE)
        cache_contributions(contributions)
    else:
        try:
            file = open("contributions.json", "r")
            contributions = json.loads(file.read())
            file.close()
        except FileNotFoundError:
            print("No cached contributions found, loading new ones")
            contributions = get_all_contributions_of_ip_range(JKU_IP_RANGE)
            cache_contributions(contributions)

    print("Found %s contributions" % len(contributions))

    titles = [contribution["title"].replace(" ", "_") for contribution in contributions]
    text = " ".join(titles)
    make_jku_logo_masked_world_cloud(text)


if __name__ == '__main__':
    main()
