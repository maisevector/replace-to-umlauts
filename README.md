# Replace to umlauts

In a nutshell, this script replaces "ae", "oe", "ue", and "ss" to the
respective umlauts according to the `ngerman` dictionary on your machine.

## Motivation

If you, like me, use the German language a lot, but prefer the American
keyboard layout for programming, you end up writing German mails and other
stuff with "ae", "oe", "ue", and "ss" instead of "ä", "ö", "ü", or "ß".
Blindly replacing them will not work for words such as "Reue".

This script takes text from stdin and replaces any incorrect word such as
"Naesse" and replaces it with the correct version from the dictionary,
"Nässe", but will leave "Reue" alone.

It was primarily written as a filter script for Vim.

## Installation

If you execute the `install.sh` script (as a normal user, not root), this
should be enough to set it up. This script is developed for Linux but should
also work on macOS.

It will create a python-dictionary from the system plain text dictionary and
copy the respective scripts into your local `$HOME/bin` directory.

## Usage

### Terminal

`echo "Mein Text" | replace-to-umlauts`

`cat mein_text_file.txt | replace-to-umlauts`

### Vim
Visually select the text and use `replace-to-umlauts` as a filter:

`:'<,'>! replace-to-umlauts` should change the text in place.

## Troubleshooting

Make sure, your `$HOME/bin` directory is in `$PATH`.
