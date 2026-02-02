#!/bin/bash

# This script uses the explicit /usr/bin/python3 path to ensure Python is found.

# 1. Change directory to the script's folder.
cd "$(dirname "$0")"

# 2. Execute the python script using the absolute path.
/usr/bin/python3 "GO - R/ui.py"