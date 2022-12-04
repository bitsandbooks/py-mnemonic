#!/usr/bin/env python
"""
AUTHOR'S NOTE: This file is licensed under the MIT License (below); copyright
for the word list file may reside with its author and you may freely
substitute your own.

Copyright 2020 Rob Dumas.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import random
import sys
import getopt

SEPARATOR = "-"
FILE_NAME = "wordlist.txt"

def get_word(list):
    return random.choice(list).rstrip()

def generate_password_string(list, number, separator):
    items = []
    for i in range(int(number)):
        word = get_word(list)
        if word not in items:
            items.append(word)
        else:
            --i
    return SEPARATOR.join( str(item) for item in items )

def generate_number_of_strings(list, number):
    items = []
    for i in range( int(number) ):
        item = random.choice(list).rstrip()
        if item not in items:
            items.append(item)
        else:
            --i
    return items

def generate_string_of_letter(list, letter):
    l = str.lower(letter)
    filtered_words = [ item for item in list if item.startswith(l) ]
    return random.choice(filtered_words).rstrip()


def main(argv):
    file_path = str(sys.path[0]) + str(os.path.sep) + FILE_NAME
    words_file = open(file_path, "r")
    WORDS = words_file.read().splitlines()
    words_file.close()
    # print( "Loaded " + str( len(WORDS) ) + " words from dictionary.\n" )

    output = []

    try:
        opts, args = getopt.getopt( argv, "al:n:p:", [ "all", "letter=", "number=", "password=" ] )
    except getopt.GetoptError:
        print( 'USAGE: pick [ -a, --all ] [ -l <letter>, --letter <letter> ] [ -n <number>, --number <number> ] [ -p <number>, --password <number> ]' )
        sys.exit(2)

    # handle arguments
    for opt, arg in opts:
        if   opt in ("-p", "--password"):
            if int(arg) < 3:
                print("For security reasons, passwords should be at least 3 words long.")
                sys.exit(1)
            else:
                entry = generate_password_string(WORDS, arg, SEPARATOR)
                output.append(entry)
        elif opt in ("-n", "--number"):
            entries = generate_number_of_strings(WORDS, arg)
            for i in range( int(arg) ):
                output.append(entries[i])
        elif opt in ("-l", "--letter"):
            entry = generate_string_of_letter(WORDS, arg)
            if entry not in output:
                output.append(entry)
        elif opt in ("-a", "--all"):
            for entry in WORDS:
                if entry not in output:
                    output.append(entry)
        elif opt not in ("-a", "--all", "-l", "--letter", "-n", "--number", "-p", "--password"):
            entry = random.choice(WORDS).rstrip()
            if entry not in output:
                output.append(entry)

    for item in output:
        print(item)
    sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
