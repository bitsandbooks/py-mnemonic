# py-mnemonic

## About

Py-mnemonic contains a Python script, *pick.py*, which will read an arbitrary number of words from a file containing a list of words. It also contains copies of [Oren Tirosh's "mnemonic" word lists][1] as examples.

## Usage

For ease of use, it is recommended to symlink `pick.py` as `pick` to a folder on your `$PATH`. You can do this by entering the following at a shell prompt:

    $ chmod u+x /path/to/py-mnemonic/pick.py
    $ ln -s /path/to/py-mnemonic/pick.py /usr/local/bin/pick

You can use the command by itself to get a single random word...

    $ pick
    pencil

...or you can pass an integer as an argument to get a dash-separated string:

    $ pick 3
    leopard-tennis-clean

Please note: the longer your word list file is, the lower the chance of repetition in long strings.

## License

This script is licensed under the [MIT License][2].


[1]: https://web.archive.org/web/20090918202746/http://tothink.com/mnemonic/wordlist.html "Wayback Machine snapshot of Oren Tirosh's web page"
[2]: https://opensource.org/licenses/MIT "MIT License at opensource.org"
