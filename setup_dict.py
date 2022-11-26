#!/usr/bin/env python3
"""
Creates a json file of the relevant dictionary entries containing umlauts.
"""
import json
import os.path
import time

# Ideally, we create a json file using the standard library
#
# If the dictionary under "/usr/share/dict/ngerman" is updated, we re-run it

umlaut_dict = {"ä":"ae","ö":"oe","ü":"ue","Ä":"Ae","Ö":"Oe","Ü":"Ue"}
DICT_PATH = '/usr/share/dict/ngerman'
# expandhome
OUT_PATH = 'data/ngerman_dict.json'

if not os.path.exists(DICT_PATH):
    raise Exception("Dictionary at %s does not exist."%(DICT_PATH))

# If on GNU/Linux
with open(DICT_PATH,encoding='utf8') as f:
    lines = f.readlines()

# Use normal umlauts for this since they are valid also for Swiss

# The save lines are:
# 1) Words with umlauts but no ss (e.g. Gerät) -> umlaut_lines
# 2) Words with ß (e.g. mäßig) -> sz_lines

# The following lines need to be checked:
# 3) Words with umlauts and ss (e.g. mässig or Abwässer) -> unsafe_lines
# (mässig is a false positive here)

# Then loop over the sz_lines and check if there is the same unsafe_line if we
# replace ß with ss. If yes, then this one is a false positive can be removed.
# sz_lines: mäßig -> mässig which is also present in unsafe_lines
# We then end up with the lines truely contains ss and can be added.

# In the above example, for 3) this would be "Abwässer". This is faster than not
# subdividing, because the sz und unsafe only have about 6000 entries each.

umlaut_lines = []
unsave_lines = []
for line in lines:
    if any(umlaut in line for umlaut in umlaut_dict) and not "ss" in line:
        umlaut_lines += [line.strip()]
    elif any(umlaut in line for umlaut in umlaut_dict) and "ss" in line:
        unsave_lines += [line.strip()]

sz_lines = [line.strip() for line in lines if "ß" in line]

# Now doublecheck unsave lines
for sz_line in sz_lines:
    alt_line = str.replace(sz_line,"ß", "ss")
    if alt_line in unsave_lines:
        unsave_lines.remove(alt_line)

relevant_lines = sorted(sz_lines + umlaut_lines + unsave_lines)

# Values
values = relevant_lines
# Create keys: replace all umlauts one by one
keys = relevant_lines
full_dict = {"ä":"ae","ö":"oe","ü":"ue","ß":"ss","Ä":"Ae","Ö":"Oe","Ü":"Ue"}
for umlaut in full_dict:
    keys = [str.replace(key,umlaut,full_dict[umlaut]) for key in keys]

ngerman_dict = dict(zip(keys, values))

with open(os.path.expanduser(OUT_PATH),"w",encoding="utf8") as write_file:
    json.dump(ngerman_dict,write_file,indent=4,ensure_ascii=False)
