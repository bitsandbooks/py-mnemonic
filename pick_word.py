#!/usr/bin/env python3

import random

def main():
    word_file = open("wordlist.txt", "r")
    words = word_file.readlines()[2:]
    word_file.close()

    print(random.choice(words).rstrip())

if __name__ == "__main__":
    main()
