#!/usr/bin/env python

import requests

import caching
import word_clouds

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


def command_loop(ip_range: str, contributions: list, is_jku: bool):
    while True:
        print("\n")
        print("Enter a command (wc, exit)")

        command = input().lower()
        if command == "wc":
            titles = [contribution["title"].replace(" ", "_") for contribution in contributions]
            text = " ".join(titles)

            if is_jku:
                word_clouds.make_jku_logo_masked_world_cloud(text)
            else:
                name = ip_range.replace("/", "_") + ".png"
                word_clouds.make_word_cloud(text, name)
        elif command == "exit":
            break
        else:
            print("Unknown command")


def main():
    print(
        "Wiked (Wikipedia Edits) provides multiple options to visualise and analyze wikipedia contributions of an ip range.\n"
        "You can enter 'JKU' to access the JKU IP range (" + JKU_IP_RANGE + ") or enter any other ipv4 range manually."
    )

    user_input = input()

    use_jku = user_input.lower() == 'jku'
    ip_range = JKU_IP_RANGE if use_jku else user_input

    print("Refresh from web? (otherwise uses cached values) (y/n)")
    refresh = input().lower() == 'y'

    if refresh:
        contributions = get_all_contributions_of_ip_range(ip_range)
        caching.save_contributions(contributions, ip_range)
    else:
        result = caching.load_contributions(ip_range)
        if result is not None:
            contributions = result
        else:
            print("No cached contributions found, loading new ones")
            contributions = get_all_contributions_of_ip_range(ip_range)
            caching.save_contributions(contributions, ip_range)

    print("Found %s contributions" % len(contributions))
    command_loop(ip_range, contributions, use_jku)


if __name__ == '__main__':
    main()
