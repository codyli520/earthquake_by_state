import argparse
import json
import urllib.request
import datetime


def print_ca_top25(data):
    top25_list = []
    for earthquake in data["features"]:
        magnitude = earthquake["properties"]["mag"]
        location = earthquake["properties"]["place"]
        time = datetime.datetime.fromtimestamp(int(earthquake["properties"]["time"])//1000)\
            .strftime('%Y-%m-%dT%H:%M:%S+00:00')

        if not magnitude:
            continue

        if "CA" in location or "California" in location:
            entry = (time, location, magnitude)

            if len(top25_list) == 25:
                if entry[2] > top25_list[-1][2]:
                    top25_list.pop()
                else:
                    continue

            top25_list.append(entry)
            top25_list = sorted(top25_list, key=lambda x: x[2], reverse=True)

    for incident in top25_list:
        print("Time: {0[0]} | Location: {0[1]} | Magnitude: {0[2]}".format(incident))


def print_us_top5(data, us_states):
    count_by_state = {}
    top5 = []
    for earthquake in data["features"]:
        state = earthquake["properties"]["place"].split(",")
        if state == "" or not state:
            continue
        elif len(state) < 2:
            state = state[0].split(" ")[-1]
        else:
            state = state[-1]
        state = state.strip()

        for key, value in us_states.items():
            if state == key or state == value:
                if us_states[key] in count_by_state:
                    count_by_state[us_states[key]] += 1
                    break
                else:
                    count_by_state[us_states[key]] = 1
                    break

    for state, count in count_by_state.items():
        if len(top5) == 5:
            if count > top5[-1][1]:
                top5.pop()
            else:
                continue
        top5.append((state, count))
        top5 = sorted(top5, key=lambda x:x[1], reverse=True)

    for state in top5:
        print("State: {0[0]} | Earthquakes: {0[1]}".format(state))


def get_json_from_url(url):
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool for earthquake analysis')
    parser.add_argument('command', help='Always include "quakes" to run this tool', choices={"quakes"})
    parser.add_argument('--top5', help='List the top 5 US states by number of earthquakes,'
                                       ' highest to lowest', action='store_true', )
    parser.add_argument('--california', help='List the top 25 strongest earthquakes in California,'
                                             ' highest to lowest', action='store_true')

    args = parser.parse_args()

    data_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    if args.california:
        json_data = get_json_from_url(data_url)
        print_ca_top25(json_data)

    elif args.top5:
        json_data = get_json_from_url(data_url)
        print_us_top5(json_data, states)

    else:
        parser.print_help()
