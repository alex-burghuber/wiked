#!/usr/bin/env python

import requests
import random

import caching
import word_clouds
import charts
import jku_cs_profs_scraper

JKU_IP_RANGE = "140.78.0.0/16"


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

        print("Loading next contributions page")
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


def command_loop(ip_range: str, contributions: list, is_jku: bool):
    while True:
        print("\n%s wikipedia contributions available for %s" % (
            len(contributions), "the JKU campus network" if is_jku else ip_range))
        print("Enter a command (wc, timestamp, nightowls, bar, " + ("profs, " if is_jku else "") + "exit)")

        command = input().strip().lower()
        if command == "wc":
            titles = [contribution["title"].replace(" ", "_") for contribution in contributions]
            text = " ".join(titles)

            if is_jku:
                word_clouds.make_jku_logo_masked_world_cloud(text)
            else:
                name = "wc" + ip_range.replace("/", "_") + ".png"
                word_clouds.make_word_cloud(text, name)

        elif command == "count":
            print("Number of contributions: %s" % len(contributions))
        elif command == "timestamp":
            print("Show all contributions after a timestamp")
            print("Enter a timestamp (e.g. 2023-01-01T00:00:00Z)")
            timestamp = input()
            after_timestamp = [c for c in contributions if c["timestamp"] > timestamp]
            print("Contributions after %s: %s" % (timestamp, len(after_timestamp)))
            for c in after_timestamp:
                print("%s at %s" % (c["title"], c["timestamp"]))
        elif command == "nightowls":
            print("25 random night owls:")
            night_owls = [c for c in contributions if
                          22 <= int(c["timestamp"][11:13]) or int(c["timestamp"][11:13]) < 6]
            random.shuffle(night_owls)
            for owl in night_owls[:25]:
                print("Edited %s at %s" % (owl["title"], owl["timestamp"]))
        elif command == "bar":
            name = "bar" + ip_range.replace("/", "_") + ".png"
            charts.create_contributions_year_bar_chart(contributions, name)
        elif command == "profs" and is_jku:
            print("Show all contributions that contain a JKU CS professor name")

            prof_names = caching.load_professors()
            if prof_names is None:
                prof_names = jku_cs_profs_scraper.scrape_jku_cs_profs()
                caching.save_professors(prof_names)
                print("Cached JKU CS professors")

            prof_contributions = []
            for contribution in contributions:
                for prof_name in prof_names:
                    if prof_name in contribution["title"]:
                        prof_contributions.append(contribution)
                        break
            print("Found %s contributions that contain a JKU CS professor name" % len(prof_contributions))
            for contribution in prof_contributions:
                print("Edited %s at %s" % (contribution["title"], contribution["timestamp"]))

        elif command == "exit":
            break
        else:
            print("Unknown command")


def main():
    print(
        "\nWiked (Wikipedia Edits) is a tool that provides multiple options to visualise and analyze wikipedia contributions of an ip range.\n"
        "You can enter 'JKU' to use the JKU ip range (" + JKU_IP_RANGE + ") or enter any other ipv4 range manually."
    )

    user_input = input()

    use_jku = user_input.lower() == 'jku'
    ip_range = JKU_IP_RANGE if use_jku else user_input

    print("Refresh contributions from web? (otherwise cached values are used) (y/n)")
    refresh = input().lower() == 'y'

    if refresh:
        print("Loading new contributions (this may take a while...)")
        contributions = get_all_contributions_of_ip_range(ip_range)
        caching.save_contributions(contributions, ip_range)
    else:
        result = caching.load_contributions(ip_range)
        if result is not None:
            contributions = result
        else:
            print("No cached contributions found, loading new ones (this may take a while...)")
            contributions = get_all_contributions_of_ip_range(ip_range)
            caching.save_contributions(contributions, ip_range)

    command_loop(ip_range, contributions, use_jku)


if __name__ == '__main__':
    main()
