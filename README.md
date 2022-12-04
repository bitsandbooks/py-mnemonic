# py-mnemonic

## About

Py-mnemonic contains a Python script, *pick.py*, which will read an arbitrary number of words from a file containing a list of words. It also contains copies of [Oren Tirosh's "mnemonic" word lists][1] as examples.

## Usage

For ease of use, it is recommended to symlink `pick.py` as `pick` to a folder on your `$PATH`. You can do this by entering the following at a shell prompt:

    $ chmod u+x /path/to/py-mnemonic/pick.py
    $ ln -s /path/to/py-mnemonic/pick.py /usr/local/bin/pick

You can use the command with the following options:

- `-a` or `--all`: will return the complete list.
- `-l X` or `--letter X` will return a random word from the list starting with the letter *X*.
- `-n X` or `--number X` will return *X* number of random words.
- `-p X` or `--password X` will return a strong, easy-to-communicate password, comprised of *X* random words and separated by dashes. (To promote good password security, it will not produce a password of fewer than 3 words.)

## License

This script is licensed under the [MIT License][2].


[1]: https://web.archive.org/web/20090918202746/http://tothink.com/mnemonic/wordlist.html "Wayback Machine snapshot of Oren Tirosh's web page"
[2]: https://opensource.org/licenses/MIT "MIT License at opensource.org"
