#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pitfall v1.0
By Danilo Lekovic for Game Design 12

filemanager.py

File manager for opening, reading, editing saved games
"""

# We are using Python's built-in JSON support
# because it is very easy to access with minimal code
import json


class FileManager:

    # Looks for key and returns value

    def readOption(option):
        jsonElements = None

        # Save game file is save.pitfall

        with open('save.pitfall', 'r') as f:
            output = f.read()

            jsonElements = json.loads(output)

        return jsonElements[option]

    # Edits key with value

    def edit(option, value):
        jsonElements = None

        # Read file first

        with open('save.pitfall', 'r') as f:
            output = f.read()

            jsonElements = json.loads(output)

        # Make changes

        jsonElements[option] = value

        # Save changes

        with open('save.pitfall', 'w') as outfile:
            json.dump(jsonElements, outfile)