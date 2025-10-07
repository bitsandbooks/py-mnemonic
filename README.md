# py-mnemonic

## About

Py-mnemonic generates somewhat-secure, psuedo-random passphrases, based upon a file containing a list of words. For reference, it uses [Oren Tirosh's "mnemonic" word lists][1] as examples. It also generates random UUIDs.

## Usage

For ease of use, it is recommended to symlink `pick.py` as `pick` to a folder on your `$PATH`. You can do this by entering the following at a shell prompt:

    $ chmod u+x /path/to/py-mnemonic/pick.py
    $ ln -s /path/to/py-mnemonic/pick.py /usr/local/bin/pick

You can use the command with the following options:

- `-w N`, `--words=N `: Number of words to use (1..20) in generating the passphrase. If omitted, defaults to a single word.
- `-l m`, `--letter=m`: Require all chosen words to start with the letter `m`, or other (case-insensitive) letter.
- `-c`, `--caps`: Randomly capitalize some of the words in the passphrase to provide better security. If a single word is requested, it is always capitalized.
- `-s spec`, `--separators=spec`: Separator spec: `dots`, `dashes`, `underscores`, `numbers`, `random`. For multi-word phrases, default is `dashes` if not specified. Multiple kinds allowed (e.g., `dots,numbers,underscores`). Each concrete kind appears at least once when possible, while `random` provides a random selection of the other types. For a single word, no separator is appended unless you supply `-s`.
- `-d, --no-dup-letters`: For multi-word phrases, ensure each chosen word starts with a different letter. Mutually exclusive with `-l`.
- `-q`, `--quiet`: Suppress warnings and informational notes.
- `-u`, `--uuid`: Print a random UUID. Lowercase by default; uppercase if `-c` is supplied.
- `--wordlist PATH`: Use `PATH` as the wordlist instead of `./wordlist.txt`
- `--all-words`: Print the entire wordlist file verbatim and exit.
- `--min-length N`: Keep only words ≥ N letters long before selecting.
- `--max-length N`: Keep only words ≤ N letters long before selecting.
- `--seed N`: Seed Python's random module to make results reproducible.
- `--json`: Output a JSON object with output, warnings, and metadata (no stderr).

## Examples:

    $ pick.py
    $ pick.py --seed 1111 -w 3
    $ pick.py -w 4 -l b -s dots
    $ pick.py -w 2 -s numbers -c
    $ pick.py -w 3 -s random
    $ pick.py -u
    $ pick.py --uuid -c --json

## License

This script is licensed under the [MIT License][2].

## Copyright

Copyright ©️ 2020, 2025 by Rob Dumas.


[1]: https://web.archive.org/web/20090918202746/http://tothink.com/mnemonic/wordlist.html "Wayback Machine snapshot of Oren Tirosh's web page"
[2]: https://opensource.org/licenses/MIT "MIT License at opensource.org"
