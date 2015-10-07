#!usr/bin/env python

import random

def main():
    wordFile = open("wordList.txt", "r")
    words = wordFile.readlines()[2:]
    wordFile.close()

    print(random.choice(words).rstrip())

if __name__ == "__main__":
    main()
