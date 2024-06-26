#!/usr/bin/env python3
"""
According to the German dictionary, replace ae, oe, ue, and ss with their 
umlauts and sharp s.
"""
import json
import re
import sys
import os
import os.path
import pathlib

UMLAUT_DICT = {"ä":"ae","ö":"oe","ü":"ue","Ä":"Ae","Ö":"Oe","Ü":"Ue"}
FULL_DICT = {"ä":"ae","ö":"oe","ü":"ue","ß":"ss","Ä":"Ae","Ö":"Oe","Ü":"Ue"}

def get_dict():
    """
    Get dictionary path, which should be at 
    "$XDG_DATA_DIR/.local/share/replace_to_umlauts/ngerman.dict".
    If XDG_DATA_DIR is not set, it will default to $HOME/.local/share.
    """
    try:
        xdg_data_dir = os.environ["XDG_DATA_DIR"]
    except KeyError:
        xdg_data_dir = os.path.expanduser('~/.local/share')
    dict_path = f"{xdg_data_dir}/replace_to_umlauts/ngerman.json"
    # If path does not exist, create the directory and run the setup for
    # creation
    if not os.path.exists(dict_path):
        pathlib.Path(os.path.dirname(dict_path)).mkdir(parents = True, exist_ok = True)
        create_dict(dict_path)
        if not os.path.exists(dict_path):
            raise RuntimeError(f"Could not create umlaut dict at {dict_path}")
    with open(os.path.expanduser(dict_path),"r",encoding="utf8") as read_file:
        ngerman_dict = json.load(read_file)
    return ngerman_dict

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
        sys.stderr.write(f"Did not replace anything although we found a match! Word was {word}")
    return correct_word

def replace_stdin_to_umlauts(umlaut_dict):
    """
    Main function executing the dictionary lookup for every word.
    """
    input_text = sys.stdin.read()
    umlaut_list_lower = ["ae","oe","ue","ss"]
    lines = input_text.split('\n')
    for i,line in enumerate(lines):
        words = line.split(' ')
        for j,word in enumerate(words):
            if contains_possible_umlaut(word,umlaut_list_lower):
                words[j] = replace_word(word,umlaut_dict)
        lines[i] = words
    new_text_2 = "\n".join([" ".join(line) for line in lines])
    sys.stdout.write(new_text_2)
    return True

def create_dict(our_dict_path):
    """
    Expected to be called if there is no replace-to-umlaut dict found.  Creates 
    the dictionary from /usr/share/dict/ngerman and places it $XDG_DATA_DIR or 
    .local/share under the folder replace-to-umlauts/ngerman_dict.json.
    ---
    The creation works as follows:
    1) Words with umlauts but no ss (e.g. Gerät) -> umlaut_lines
    2) Words with ß (e.g. mäßig) -> sz_lines
    The following lines are unsafe and need to be checked:
    3) Words with umlauts and ss (e.g. mässig or Abwässer) -> unsafe_lines
    (mässig is a false positive here)
    How do we do it?
    We loop over the sz_lines and check if there is the same unsafe_line if we
    replace ß with ss. If yes, then this one is a false positive can be removed.
    sz_lines: mäßig -> mässig which is also present in unsafe_lines
    We then end up with the lines truely contains ss and can be added.
    In the above example, for 3) this would be "Abwässer". This is faster than not
    subdividing, because the sz und unsafe ones only have about 6000 entries each.
    """
    if not os.path.exists(os_dict_path := '/usr/share/dict/ngerman'):
        raise RuntimeError(f"Dictionary at {os_dict_path} does not exist.")
    with open(os_dict_path,encoding='utf8') as file:
        lines = file.readlines()
    # Get umlaut words, they will be the values and keys in the new dictionary,
    # but the values will be replaced with their ascii counterparts.
    to_be_keys = _umlauts_from_dict(lines)
    values = to_be_keys
    for umlaut,umlaut_asciified in FULL_DICT.items():
        to_be_keys = [str.replace(key,umlaut,umlaut_asciified) for key in to_be_keys]
    ngerman_dict = dict(zip(to_be_keys, values))
    with open(os.path.expanduser(our_dict_path),"w",encoding="utf8") as write_file:
        json.dump(ngerman_dict,write_file,indent=4,ensure_ascii=False)
    return True

def _umlauts_from_dict(lines):
    """
    Returns the umlauts, which are the keys for the new dictionary.
    """
    umlaut_lines = []
    unsave_lines = []
    for line in lines:
        if any(umlaut in line for umlaut in UMLAUT_DICT) and not "ss" in line:
            umlaut_lines += [line.strip()]
        elif any(umlaut in line for umlaut in UMLAUT_DICT) and "ss" in line:
            unsave_lines += [line.strip()]
    # Now doublecheck unsave lines
    sz_lines = [line.strip() for line in lines if "ß" in line]
    for sz_line in sz_lines:
        alt_line = str.replace(sz_line,"ß", "ss")
        if alt_line in unsave_lines:
            unsave_lines.remove(alt_line)
    relevant_lines = sorted(sz_lines + umlaut_lines + unsave_lines)
    return relevant_lines

if __name__ == '__main__':
    umlaut_dict = get_dict()
    replace_stdin_to_umlauts(umlaut_dict)
    # Future ideas:
    # - Allow custom path passed via dash or double hyphen
