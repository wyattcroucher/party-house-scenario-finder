# Party House Scenario Finder
# All code except the main method is taken from https://github.com/phil-macrocheira/bean-bot
# Example Usage: python "Party House Scenario Finder.py" --include "MONKEY, TICKET TKR, CHEERLEADR, ROCK STAR, WEREWOLF, GANGSTER, GAMBLER, DANCER, AUCTIONEER, CELEBRITY, BARTENDER"

import json
import random
import math
import re 
import os
import string
import sys
from argparse import ArgumentParser

count = 0
includes = []
excludes = []

character_types = [
    ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
    "DANCER",              #11
    "HIPPY", 
    "CUTE DOG",
    "SECURITY",
    "WRESTLER",
    "WATCH DOG", 
    "SPY", 
    "DRIVER",
    "PRIVATE I.",
    "GRILLMASTR",      #20
    "ATHLETE", 
    "MR POPULAR",
    "CELEBRITY", 
    "COMEDIAN",
    "PHOTOGRAPHR", 
    "CATERER", 
    "TICKET TKR",
    "AUCTIONEER",
    "MONKEY",
    "ROCK STAR",        #30
    "GANGSTER",
    "GAMBLER", 
    "WEREWOLF",
    "MASCOT",
    "INTROVERT", 
    "COUNSELOR", 
    "STYLIST", 
    "BARTENDER", 
    "WRITER",
    "CLIMBER",            #40
    "CUPID", 
    "MAGICIAN",
    "GREETER", 
    "CHEERLEADR",
    ".", ".", ".", ".", ".",
    "ALIEN",                #50
    "DINOSAUR",
    "LEPRECHAUN",
    "GENIE", 
    "MERMAID", 
    "DRAGON",
    "GHOST", 
    "UNICORN", 
    "SUPERHERO"
]
pop_costs = {
    "DIVIDER": -1,
    "OLD FRIEND": 2,
    "OLD FRIEND": 2,
    "OLD FRIEND": 2,
    "OLD FRIEND": 2,
    "RICH PAL": 3,
    "RICH PAL": 3,
    "RICH PAL": 3,
    "RICH PAL": 3,
    "WILD BUDDY": 1,
    "WILD BUDDY": 1,
    "DANCER": 7,
    "HIPPY": 4,
    "CUTE DOG": 7,
    "SECURITY": 4,
    "WRESTLER": 9,
    "WATCH DOG": 4,
    "SPY": 8,
    "DRIVER": 3,
    "PRIVATE I.": 4,
    "GRILLMASTR": 5,
    "ATHLETE": 6,
    "MR POPULAR": 5,
    "CELEBRITY": 11,
    "COMEDIAN": 5,
    "PHOTOGRAPHR": 5,
    "CATERER": 5,
    "TICKET TKR": 4,
    "AUCTIONEER": 9,
    "MONKEY": 3,
    "ROCK STAR": 5,
    "GANGSTER": 6,
    "GAMBLER": 7,
    "WEREWOLF": 5,
    "MASCOT": 5,
    "INTROVERT": 4,
    "COUNSELOR": 7,
    "STYLIST": 7,
    "BARTENDER": 11,
    "WRITER": 8,
    "CLIMBER": 12,
    "CUPID": 8,
    "MAGICIAN": 5,
    "GREETER": 5,
    "CHEERLEADR": 5,
    "45": -1,
    "46": -1,
    "47": -1,
    "48": -1,
    "49": -1,
    "ALIEN": 40,
    "DINOSAUR": 25,
    "LEPRECHAUN": 50,
    "GENIE": 55,
    "MERMAID": 30,
    "DRAGON": 30,
    "GHOST": 45,
    "UNICORN": 45,
    "SUPERHERO": 50
}

CHAR_START = 11
CHAR_END = 44
CHAR_PRESTIGE_START = 50
CHAR_PRESTIGE_END = 58\

def sort_deck(deck):
    character_names = [character_types[index] for index in deck]
    sort_keys = [pop_costs[name] for name in character_names]
    combined = list(zip(deck, sort_keys))
    combined.sort(key=lambda x: x[1])
    sorted_deck,sorted_keys = zip(*combined)
    return sorted_deck

def rng_random():
    global rng_state_1, rng_state_2
    rng_state_1 = (65192 * (rng_state_1 & 65535)) + ((rng_state_1 & 4294901760) >> 16)
    rng_state_2 = (64473 * (rng_state_2 & 65535)) + ((rng_state_2 & 4294901760) >> 16)
    ret = (((rng_state_1 & 65535) << 16) + rng_state_2) & 4294967295
    return ret

def rng_random_int(arg0, arg1):
    r = rng_random()
    ret = arg0 + math.floor(((arg1 - arg0 + 1) * r) / 4294967296)
    return ret

def generate_scenario(seed):
    global rng_state_1, rng_state_2
    mask = 1431655765
    rng_state_1 = 1253089769 ^ (seed & mask)
    rng_state_2 = 2342871706 ^ (seed & ~mask)
    for i in range(20):
        rng_random()
    deck = []
    num_reg_chars = 11
    num_prestige_chars = 13 - num_reg_chars
    for i in range(num_reg_chars):
        while True:
            rand_char = rng_random_int(CHAR_START, CHAR_END)
            if rand_char not in deck and rand_char <= 44:
                deck.append(rand_char)
                break
        rng_random()
    for i in range(num_prestige_chars):
        while True:
            rand_char = rng_random_int(CHAR_PRESTIGE_START, CHAR_PRESTIGE_END)
            if rand_char not in deck and rand_char <= 58:
                deck.append(rand_char)
                break
        rng_random()
    return deck

def get_scenario_result(seed):
    global rng_state_1, rng_state_2
    rng_state_1 = -1
    rng_state_2 = -1
    if seed is None:
        seed = random.randint(0, 999999)
    #elif not isinstance(seed, (int, float)):
    #    return await interaction.response.send_message(content=f"Please specify a valid number value between **000000** and **999999**.", ephemeral=True)
    #elif seed < 0 or seed > 999999:
    #    return await interaction.response.send_message(content=f"That seed value is not between **000000** and **999999**.", ephemeral=True)
    seed = int(seed)
    deck = sort_deck(generate_scenario(seed)) # Input can be from 0 to 999999
    deck_names = [character_types[index] for index in deck]
    #return await interaction.response.send_message(f"**SEED {str(seed).zfill(6)}**\n\n{" ".join(deck_names)}")
    #return deck_names
    return deck

def fix_spelling(word):
    word = word.strip().upper()
    if "CHEERLEAD" in word:
        return "CHEERLEADR"
    elif "PHOTOGRAPH" in word:
        return "PHOTOGRAPHR"
    elif "GRILL" in word:
        return "GRILLMASTR"
    elif "POPULAR" in word:
        return "MR POPULAR"
    elif "PRIVATE" in word:
        return "PRIVATE I."
    elif "TICKET" in word:
        return "TICKET TKR"
    elif "ROCK" in word:
        return "ROCK STAR"
    elif "HIPP" in word:
        return "HIPPY"
    return word

# main method
parser = ArgumentParser()
parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print scenarios, just print the final count")
parser.add_argument("-i", "--include", dest="include", type=str, default = "",
                    help="guests that the scenario must include. Multiple guests must be in quotes and comma separated. Names must be all caps, spelling must match in-game spelling. example: --include \"PHOTOGRAPHR, STYLIST, CHEERLEADR\"")
parser.add_argument("-e", "--exclude", dest="exclude", type=str, default = "",
                    help="guests that the scenario must exclude")
parser.add_argument("-s", "--seed", dest="seed", type=int, default = -1,
                    help="show specific seed. don't use other arguments with this")
parser.add_argument("-m", "--min", dest="min", type=int, default = 0,
                    help="seed to start searching from")
parser.add_argument("-x", "--max", dest="max", type=int, default = 999999,
                    help="seed to stop searching at")

args = parser.parse_args()
if (args.seed >= 0 and args.seed < 1000000):
    min = args.seed
    max = args.seed + 1
else:
    min = args.min
    max = args.max + 1
    
if args.include:
    for word in args.include.split(','):
        word = fix_spelling(word)
        found = False
        for i, name in enumerate(character_types):
            if name == word:
                includes.append(i)
                found = True
                break
        if not found:
            print("Aborting. " + word + " isn't a valid guest.")
            sys.exit()
if args.exclude:
    for word in args.exclude.split(','):
        found = False
        word = fix_spelling(word)
        for i, name in enumerate(character_types):
            if name == word:
                excludes.append(i)
                found = True
                break
        if not found:
            print("Aborting. " + word + "isn't a valid guest.")
            sys.exit()
includes = sorted(includes)
excludes = sorted(excludes)

for i in range(min, max):
    scenario_result = get_scenario_result(i)
    skip = False
    for include in includes:
        if include not in scenario_result:
            skip = True
            break
    if skip:
        continue
    for exclude in excludes:
        if exclude in scenario_result:
            skip = True
            break
    if skip:
        continue
    count += 1
    if args.verbose:
        print(i)
        deck_names = [character_types[index] for index in scenario_result]
        for name in deck_names:
            print(name)
        print(os.linesep)
        
print("Total: ", end='')
print(count)