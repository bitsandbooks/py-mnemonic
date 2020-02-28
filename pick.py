#!/usr/bin/env python

import os
import random
import sys

word_separator = "-"
word_file = "wordlist.txt"

def get_word():
    word_file_path = str(sys.path[0]) + str(os.path.sep) + word_file
    words = open(word_file_path, "r")
    word_list = words.readlines()[2:]
    words.close()
    return random.choice(word_list).rstrip()

def get_string(word_count):
    word_string = [ get_word() ]
    for i in range(1,word_count): word_string.append( get_word() )
    return word_separator.join(str(w) for w in word_string)


def main():
    if len(sys.argv) == 1 or int(sys.argv[1]) == 1:
        print( get_word() )
    else:
        words_requested = int(sys.argv[1])
        print( get_string(words_requested) )

if __name__ == "__main__":
    main()
