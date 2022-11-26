#!/usr/bin/env python3
"""
According to the German dictionary, replace ae, oe, ue, and ss with their umlauts and sharp s
"""
import json
import re
# import warnings
import sys
import os.path

def contains_possible_umlaut(word,umlaut_list):
    """
    Returns True if the word contains an umlaut.
    """
    # No need to remove anything, just check:
    if any(umlaut in word.lower() for umlaut in umlaut_list):
        return True
    return False

def replace_word(word,ngerman_dict):
    """
    Retrieves the correct word from the dictionary and then replaces the original word.
    -----
    1. Get rid of non-ascii characters in word
    2. Match word and replace in original if matched
    This approach checks for capitalized words in a second step if it was not found
    to not slip capitalized words. That does not work for uppercase words or something
    with capitalized letters in the middle.
    """
    # correct_word = word
    # Sanitize word and remove special characters
    word_cleaned = re.sub(r"[^a-zA-Z]","", word)
    # Search in dict
    if word_cleaned in ngerman_dict.keys():
        replacement = ngerman_dict[word_cleaned]
        match = True
        correct_word = word.replace(word_cleaned,replacement)
    # This should work for the "normal" case i.e. beginning of a new sentence.
    # However, it will incorrectly treat middle upper case, alternative: str.isupper()
    elif word_cleaned.lower() in ngerman_dict.keys():
        replacement = ngerman_dict[word_cleaned.lower()].capitalize()
        match = True
        correct_word = word.lower().replace(word_cleaned.lower(),replacement)
    else:
        match = False
        correct_word = word
    if correct_word == word and match is True:
        # Or should this be a warnings.warn?
        sys.stderr.write("Did not replace anything although we found a match! Word was ", word)
    return correct_word

input_text = sys.stdin.read()
# input_text = "Veraechtlich zeigte er Reue. Ueber Oesen im\nFloss."
DICT_PATH = '~/.local/share/replace-to-umlauts/ngerman_dict.json'
umlaut_list_lower = ["ae","oe","ue","ss"]

with open(os.path.expanduser(DICT_PATH),"r",encoding="utf8") as read_file:
    ngerman_dict = json.load(read_file)

lines = input_text.split('\n')
for i,line in enumerate(lines):
    words = line.split(' ')
    for j,word in enumerate(words):
        if contains_possible_umlaut(word,umlaut_list_lower):
            words[j] = replace_word(word,ngerman_dict)
    lines[i] = words

new_text_2 = "\n".join([" ".join(line) for line in lines])

sys.stdout.write(new_text_2)
