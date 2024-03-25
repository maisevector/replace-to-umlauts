#!/usr/bin/env bash
set -euo pipefail

output=$(echo "Aeon Oese Uebelkeit aendern moeglich Hueter Gruesse Floss Israeli Oboe Reue" | python3 replace_to_umlauts.py)
testcase="Äon Öse Übelkeit ändern möglich Hüter Grüße Floß Israeli Oboe Reue"

if [ "${output}" = "${testcase}" ]; then
    exit 0
else
    echo "Error: output is output instead of testcase:"
    echo "${output}"
    echo "${testcase}"
    exit 1
fi
