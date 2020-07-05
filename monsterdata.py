#!/bin/env python3

import requests
import urllib.request
import time
import sys

def sign(val):
    return f"{val:+}"


def mod(score):
    return sign((score-10)//2)

def challenge_str(challenge):
    xp = {
        0: "10",
        0.125: "25",
        0.25: "50",
        0.5: "100",
        1: "200",
        2: "450",
        3: "700",
        4: "1,100",
        5: "1,800",
        6: "2,300",
        7: "2,900",
        8: "3,900",
        9: "5,000",
        10: "5,900",
        11: "7,200",
        12: "8,400",
        13: "10,000",
        14: "11,500",
        15: "13,000",
        16: "15,000",
        17: "18,000",
        18: "20,000",
        19: "22,000",
        20: "25,000",
        21: "33,000",
        22: "41,000",
        23: "50,000",
        24: "62,000",
        25: "75,000",
        26: "90,000",
        27: "105,000",
        28: "120,000",
        29: "135,000",
        30: "155,000"
    }
    this_xp = xp[challenge]
    if challenge == 0.125:
        challenge = "1/8"
    elif challenge == 0.25:
        challenge = "1/4"
    elif challenge == 0.5:
        challenge = "1/2"
    else:
        challenge = str(challenge)
    return f"{challenge} ({this_xp}XP)"


def ability_str(ability):
    return f"""
\\begin{{monsteraction}}[{ability['name']}]
{ability['desc']}
\\end{{monsteraction}}
    """

def action_str(action):
    return f"""
\\begin{{monsteraction}}[{action['name']}]
{action['desc']}
\\end{{monsteraction}}
    """

def detail(level, category, data):
    api_str = f"{category}_{level}"
    tex_str = f"{category}{level}"
    if api_str in data:
        # For some things, it's just string, sometimes its an object with a name property
        return f"{tex_str} = {{{', '.join([thing.title() if type(thing) == str else thing['name'].title() for thing in data[api_str]])}}}"
    else:
        return ""

searchterm = ""
index = -1
for arg in sys.argv[1:]:
    if not arg.startswith("-"):
        searchterm += arg + " "
    else:
        index = int(arg[1:])

searchterm = searchterm.strip()
searchtype = "monsters"

url = f"https://www.dnd5eapi.co/api/{searchtype}/?name={searchterm.lower().replace(' ','+')}"
response = requests.get(url)
data = response.json()

newline = '\n'

if response.reason == "OK":
    if data['count'] == 0:
        print("No results")
    if data['count'] == 1 or index != -1:
        if index != -1:    
            new_url = "https://www.dnd5eapi.co" + data['results'][index]['url']
        else:
            new_url = "https://www.dnd5eapi.co" + data['results'][0]['url']
        new_response = requests.get(new_url)
        data = new_response.json()

        tex = f"""
\\begin{{monsterbox}}{{{data['name']}}}
\\textit{{{data['size']} {data['type']} ({data['subtype']}), {data['alignment']}}}\\\\
\\hline
\\basics[%
armorclass = {data['armor_class']},
hitpoints = {data['hit_points']},
speed = {{{', '.join([key.title() + ": " + data['speed'][key] for key in data['speed'].keys()])}}}
]
\\hline
\\stats[
STR = {data['strength']} ({mod(data['strength'])}),
DEX = {data['dexterity']} ({mod(data['dexterity'])}),
CON = {data['constitution']} ({mod(data['constitution'])}),
INT = {data['intelligence']} ({mod(data['intelligence'])}),
WIS = {data['wisdom']} ({mod(data['wisdom'])}),
CHA = {data['charisma']} ({mod(data['charisma'])}),
]
\\hline
\\details[%
skills = {{{newline.join([prof['name'].replace('Skill: ', '') + ' ' + sign(prof['value']) for prof in data['proficiencies']])}}},
senses = {{{', '.join([sense.replace('_', ' ').title() for sense in data['senses'].keys()])}}},
languages = {{{data['languages']}}},
challenge = {{{challenge_str(data['challenge_rating'])}}},
{detail('immunities', 'condition', data)},
{detail('resistances', 'condition', data)},
{detail('vulnerabilities', 'condition', data)},
{detail('immunities', 'damage', data)},
{detail('resistances', 'damage', data)},
{detail('vulnerabilities', 'damage', data)},
]
\\hline \\\\[1mm]
{newline.join([ability_str(ability) for ability in data['special_abilities']]) if 'special_abilities' in data else ''}
\\monstersection{{Actions}}
{newline.join([action_str(action) for action in data['actions']])}
\\end{{monsterbox}}
        """
        print(tex)
    else:
        print("Too many results, be more specific or use the index provided (with the argument `-#`:")
        for index, result in enumerate(data['results']):
            print(f"{index}: {result['name']}")
else:
    print(f"Could not find {searchterm}")
