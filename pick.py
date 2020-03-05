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

separator = "-"
file_name = "wordlist.txt"

def get_word():
    return random.choice(words).rstrip()

def get_string(word_count):
    string_list = [ get_word() ]
    for i in range(1,word_count):
        string_list.append( get_word() )
    return separator.join( str(item) for item in string_list )

file_path = str(sys.path[0]) + str(os.path.sep) + file_name
words_file = open(file_path, "r")
words = words_file.readlines()[2:] # skip the first two (comment) lines 
words_file.close()

if len(sys.argv) == 1 or int(sys.argv[1]) == 1:
    print( get_word() )
else:
    words_requested = int(sys.argv[1])
    print( get_string(words_requested) )
