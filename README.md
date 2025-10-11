# py-mnemonic

## About

Py-mnemonic generates somewhat-secure, psuedo-random passphrases, based upon a file containing a list of words. For reference, it uses [Oren Tirosh's "mnemonic" word lists][1] as examples. It also generates random UUIDs.

## Usage

For ease of use, it is recommended to symlink `mnemonic.py` as something like `mnemonic` into a folder on your `$PATH`. You can do this by entering the following at a shell prompt:

    $ chmod u+x /path/to/py-mnemonic/mnemonic.py
    $ ln -s /path/to/py-mnemonic/mnemonic.py /usr/local/bin/mnemonic

## Options

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

    $ mnemonic
    $ mnemonic --seed 1111 -w 3
    $ mnemonic -w 4 -l b -s dots
    $ mnemonic -w 2 -s numbers -c
    $ mnemonic -w 3 -s random
    $ mnemonic -u
    $ mnemonic --uuid -c --json

## Reproducible Tests (using the default `wordlist.txt`)

If you run these commands, you should see the same results:

<table>
    <tr>
        <th>Label</th>
        <th>Command</th>
        <th>Expected output</th>
        <th>Expected errors/warnings (if any)</th>
    </tr>
    <tr>
        <td>T1: default single word</td>
        <td>mnemonic --seed 1111</td>
        <td>echo</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T2: single word + caps</td>
        <td>mnemonic --seed 1111 -c</td>
        <td>Echo</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T3: single word + dot</td>
        <td>mnemonic --seed 2222 -s dots</td>
        <td>dublin.</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T4: 3 words default separators</td>
        <td>mnemonic --seed 3333 -w 3</td>
        <td>cheese-pamela-phrase</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T5: 3 words + caps</td>
        <td>mnemonic --seed 4444 -w 3 -c</td>
        <td>Pandora-Sport-Madrid</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T6: 4 words coverage dots,dashes</td>
        <td>mnemonic --seed 5555 -w 4 -s dots,dashes</td>
        <td>maximum-cannon-bahama.expand</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T7: 3 words random separators</td>
        <td>mnemonic --seed 6666 -w 3 -s random</td>
        <td>effect108cockpit215falcon</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T8: 2 words (warning expected)</td>
        <td>mnemonic --seed 7777 -w 2 -s dots,dashes,numbers</td>
        <td>cinema.pasta</td>
        <td>Warning: you requested 2 words (1 separator slot) but specified 3 different separator kinds: dashes, dots, numbers. It’s not possible to include every kind at least once with the available slots.</td>
    </tr>
    <tr>
        <td>T9: single word + numbers</td>
        <td>mnemonic --seed 8888 -s numbers</td>
        <td>process272</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T10: 5 words no-dup-letters</td>
        <td>mnemonic --seed 9999 -w 5 -d</td>
        <td>libra-admiral-zodiac-xray-tactic</td>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>T11: 5 words len 4–6 random,dots,underscores</td>
        <td>mnemonic --seed 2468 -w 5 --min-length 4 --max-length 6 -s random,dots,underscores</td>
        <td>lake-shoe921lobby.druid_engine</td>
        <td>&nbsp;</td>
    </tr>
</table>


## License

This script is licensed under the [MIT License][2].

## Copyright

Copyright ©️ 2020, 2025 by Rob Dumas.


[1]: https://web.archive.org/web/20090918202746/http://tothink.com/mnemonic/wordlist.html "Wayback Machine snapshot of Oren Tirosh's web page"
[2]: https://opensource.org/licenses/MIT "MIT License at opensource.org"
