#!/bin/bash

# Notify if not linux (for the first part)
# TODO Make cross-platform-isher
if [ "${OSTYPE}" != "linux-gnu" ]; then
    echo "Linux is supported. If something will fail, you will be alone..."
    echo "Trying to install it anyways..."
fi
# Exit if sudo 
# TODO Enable for root as well
if [ "$(id -u)" -eq 0 ]; then
        echo "For installing, do not execute with root privileges."
        echo "Aborted. Try without sudo instead."
        exit 1
fi

# Set up storage dir
# TODO Configure earlier, configure for root as well
storage_dir="${HOME}/.local/share/replace-to-umlauts"
if [ ! -d ${storage_dir} ]; then
    mkdir -p "${storage_dir}"
fi

json_dict="data/ngerman_dict.json" 
if [ ! -f "${json_dict}" ]; then
    echo "Could not find dictionary file. Are you in the correct directory?"
    exit 1
else
    cp "${json_dict}" "${storage_dir}"
fi

# Make it accessible in bin folder
chmod 755 ./replace-to-umlauts.py
user_bin="${HOME}/bin"
if [ ! -d "${user_bin}" ]; then
    mkdir "${user_bin}"
elif [ -f "${user_bin}/replace-to-umlauts" ]; then
    rm "${user_bin}/replace-to-umlauts"
fi
cp ./replace-to-umlauts.py "${user_bin}/replace-to-umlauts" 

if [ $? -eq 1 ]; then
    echo "Could not create link"
    exit 1
else
    echo "Installation successful"
fi
