#!/bin/bash
set -euo pipefail

# Make it accessible in bin folder
chmod 755 ./replace_to_umlauts.py
user_bin="${HOME}/bin"
if [ ! -d "${user_bin}" ]; then
    mkdir "${user_bin}"
fi
cp ./replace_to_umlauts.py "${user_bin}/replace-to-umlauts" 

if [ $? -eq 1 ]; then
    echo "Could not copy replace-to-umlauts to ${user_bin} directory"
    exit 1
else
    echo "Installation successful"
fi
