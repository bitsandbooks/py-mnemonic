# py-mnemonic

## About

Py-mnemonic contains a Python script, *pick.py*, which will read an arbitrary number of words from a file containing a list of words. It also contains copies of [Oren Tirosh's "mnemonic" word lists][1] as examples.

## Usage

You can use the command by itself to get a single random word...

    $ /path/to/py-mnemonic/pick.py
    pencil

...or you can pass an integer as an argument to get a dash-separated string:

    $ /path/to/py-mnemonic/pick.py 3
    leopard-tennis-clean

Please note: the longer your word list file is, the lower the chance of repetition in long strings.

## License

This script is licensed under the [MIT License][2].


[1]: https://web.archive.org/web/20090918202746/http://tothink.com/mnemonic/wordlist.html "Wayback Machine snapshot of Oren Tirosh's web page"
[2]: https://opensource.org/licenses/MIT "MIT License at opensource.org"
