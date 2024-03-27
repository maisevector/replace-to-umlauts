# Replace to umlauts

In a nutshell, this script replaces "ae", "oe", "ue", and "ss" to the
respective umlauts "ä", "ö", "ü", "ß", only if a corresponding entry can be 
found in the `ngerman` dictionary on your machine.

## Motivation

On an English keyboard, many German text are written with "ae" etc.  Blindly 
replacing umlauts them to umlauts will not work for words such as "Reue".

This script takes text from stdin and replaces any incorrect word such as
"Naesse" and replaces it with the correct version from the dictionary,
"Nässe", but will leave "Reue" alone.

## Installation

The `replace_to_umlauts.py` Python script is a standalone script.  The
`install.sh` file will place it into `~/bin`, rename it to the more
bash-compatible manner `replace-to-umlauts`, and make it executable.

### Linux
Just use `make` in the current directory, which will place the Python script in 
your `$HOME/bin` directory.  From then on, everything should just work.  

### Others 

This script is tested on Linux but should also work on macOS if the system
dictionary is in the same place (not sure about the system dictionary location
there).

## Usage

### Terminal

`echo "Naesse und Reue" | replace-to-umlauts`

`cat my_text_file.txt | replace-to-umlauts`

Alternatively and in this directory, call it via Python:

`echo "Naesse und Reue" | python3 replace_to_umlauts.py`

### Vim
Visually select the text and use `replace-to-umlauts` as a filter:

`:'<,'>! replace-to-umlauts` should change the text in place.

## Troubleshooting

Make sure, your `$HOME/bin` directory is in `$PATH`.
