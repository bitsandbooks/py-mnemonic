#!/usr/bin/env python3
"""
AUTHOR'S NOTE: This file is licensed under the MIT License (below); copyright
for the word list file may reside with its author and you may freely
substitute your own.

Copyright 2020, 2025 by Rob Dumas.

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

import argparse
import random
import sys
import uuid
import json
from pathlib import Path
from collections import defaultdict

DEFAULT_WORDLIST = Path("wordlist.txt")
MAX_WORDS = 20
MIN_WORDS = 1

# Canonical separator kinds (tokens)
BASIC_KINDS = ["dots", "dashes", "underscores", "numbers"]

# Accept many aliases, but normalize to canonical tokens above (+ "random")
SEPARATOR_ALIASES = {
    "dashes": "dashes",
    "dash": "dashes",
    "-": "dashes",
    "dots": "dots",
    "dot": "dots",
    ".": "dots",
    "underscores": "underscores",
    "underscore": "underscores",
    "_": "underscores",
    "numbers": "numbers",
    "number": "numbers",
    "random": "random",  # special pseudo-kind
}

def load_wordlist(path):
    if not path.exists() or not path.is_file():
        raise FileNotFoundError("Wordlist file not found: {}".format(path))
    words = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            w = line.strip()
            if w:
                words.append(w)
    if not words:
        raise ValueError("Wordlist at {} contains no words.".format(path))
    return words

def filter_by_letter(words, letter):
    letter = letter.lower()
    return [w for w in words if w.lower().startswith(letter)]

def filter_by_length(words, min_len, max_len):
    return [w for w in words if (min_len is None or len(w) >= min_len)
            and (max_len is None or len(w) <= max_len)]

def parse_separators(spec):
    parts = [p.strip() for p in spec.split(",") if p.strip()]
    if not parts:
        raise ValueError("Empty separator specification")
    out = []
    for p in parts:
        key = p.lower()
        if key not in SEPARATOR_ALIASES:
            valid = ", ".join(sorted(set(SEPARATOR_ALIASES.keys())))
            raise ValueError("Unknown separator '{}'. Valid options: {}".format(p, valid))
        out.append(SEPARATOR_ALIASES[key])  # normalize to canonical token
    return out  # list of canonical tokens: dots|dashes|underscores|numbers|random

def _render_separator_instance(token):
    """Return the concrete separator string for a canonical token."""
    if token == "random":
        token = random.choice(BASIC_KINDS)
    if token == "numbers":
        return str(random.randint(1, 999))
    if token == "dots":
        return "."
    if token == "dashes":
        return "-"
    if token == "underscores":
        return "_"
    # Fallback (shouldn't happen)
    return "-"

def choose_separators_cover_all(tokens, slots):
    """
    Ensure each explicitly requested CONCRETE kind appears at least once when possible.
    'random' does NOT add a required kind; it only expands the pool for filling.
    Returns (list_of_rendered_separators, covered_all_required: bool, chosen_tokens_debug: list[str])
    """
    if slots <= 0:
        return [], True, []

    explicit_concrete = [t for t in tokens if t in BASIC_KINDS]
    has_random = any(t == "random" for t in tokens)

    # Required kinds are only the explicit concrete ones (order-preserving unique)
    required_kinds = list(dict.fromkeys(explicit_concrete))
    # Pool for filling remaining slots: if random present, all basic kinds; else only required kinds
    random_pool = (BASIC_KINDS if has_random else (required_kinds if required_kinds else BASIC_KINDS))

    covered_all = True
    chosen_tokens = []

    if slots >= len(required_kinds):
        # Place one of each required kind
        chosen_tokens.extend(required_kinds)
        # Fill remaining with random choices from the pool
        while len(chosen_tokens) < slots:
            chosen_tokens.append(random.choice(random_pool))
    else:
        # Not enough slots to cover every required kind
        covered_all = False
        chosen_tokens.extend(required_kinds[:slots])

    random.shuffle(chosen_tokens)
    rendered = [_render_separator_instance(t) for t in chosen_tokens]
    return rendered, covered_all, chosen_tokens  # chosen_tokens are canonical tokens actually chosen

def choose_single_separator(tokens):
    """Pick one canonical token and render it to a concrete separator."""
    token = random.choice(tokens)
    sep = _render_separator_instance(token)
    return sep, token  # return the canonical token name for notes

def apply_caps_to_word(word, caps_flag, single_word_always_cap):
    """
    If caps_flag is True:
      - Single word: always capitalize.
      - Multiple words: each has a 40% chance to be capitalized (Capitalize or UPPER).
    """
    if not caps_flag:
        return word
    if single_word_always_cap:
        return word.capitalize()
    if random.random() < 0.4:
        return random.choice([word.capitalize(), word.upper()])
    return word.lower()

def build_passphrase(words, separators_tokens, caps, single_word_always_cap):
    if len(words) == 1:
        return apply_caps_to_word(words[0], caps, single_word_always_cap)
    cased = [apply_caps_to_word(w, caps, False) for w in words]
    pieces = []
    for i, w in enumerate(cased):
        pieces.append(w)
        if i < len(cased) - 1:
            pieces.append(separators_tokens[i])
    return "".join(pieces)

def pick_words_no_dup_letters(pool, k):
    groups = defaultdict(list)
    for w in pool:
        if not w:
            continue
        groups[w[0].lower()].append(w)
    if len(groups) < k:
        raise ValueError("Not enough distinct starting letters in the pool to pick {} words.".format(k))
    letters = list(groups.keys())
    random.shuffle(letters)
    for letter in letters:
        random.shuffle(groups[letter])
    chosen = []
    for letter in letters:
        if len(chosen) == k:
            break
        if groups[letter]:
            chosen.append(groups[letter].pop())
    if len(chosen) != k:
        raise ValueError("Failed to assemble {} words with unique initial letters.".format(k))
    return chosen

def print_help_and_exit():
    print("""pick.py — generate memorable passphrases.

Options:
  -? / --help / -h       Show this help message
  -w N, --words=N        Number of words to use (1..20). If omitted, defaults to a single word.
  -l m, --letter=m       Require all chosen words to start with the given letter (case-insensitive).
  -c, --caps             Randomly capitalize about 40% of the words. If only one word is requested, it is always capitalized.
  -s spec, --separators=spec
                         Separator spec: dots, dashes, underscores, numbers, random.
                         For multi-word phrases, default is dashes if not specified.
                         Multiple kinds allowed (e.g. dots,dashes,random). Each concrete kind appears
                         at least once when possible (random expands the pool but is not “required”).
                         For a single word, NO separator is appended unless you supply -s.
  -d, --no-dup-letters   For multi-word phrases, ensure each chosen word starts with a different letter.
  -q, --quiet            Suppress warnings and informational notes.
  -u, --uuid             Print a random UUID (lowercase by default; uppercase if -c is supplied).
  --wordlist PATH        Use PATH as the wordlist instead of ./wordlist.txt
  --all-words            Print the entire wordlist file verbatim and exit.
  --min-length N         Keep only words of length >= N before selecting.
  --max-length N         Keep only words of length <= N before selecting.
  --seed N               Seed Python's random module to make results reproducible.
  --json                 Output a JSON object with output, warnings, and metadata (no stderr).

Examples:
  pick.py
  pick.py --seed 1111 -w 3
  pick.py -w 4 -l b -s dots
  pick.py -w 2 -s numbers -c
  pick.py -w 3 -s random
  pick.py -u
  pick.py --uuid -c --json
""")
    sys.exit(0)

def emit_json(status, payload, exit_code=0):
    print(json.dumps({"status": status, **payload}, ensure_ascii=False, indent=2))
    return exit_code

def main(argv=None):
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("-?", dest="qmark_help", action="store_true")
    p.add_argument("-h", "--help", dest="std_help", action="store_true")
    p.add_argument("-w", "--words", type=int)
    p.add_argument("-l", "--letter", metavar="m")
    p.add_argument("-c", "--caps", action="store_true")
    # IMPORTANT: default=None so we know if user actually provided -s
    p.add_argument("-s", "--separators", metavar="spec", default=None)
    p.add_argument("-d", "--no-dup-letters", action="store_true", dest="no_dup_letters")
    p.add_argument("-q", "--quiet", action="store_true", dest="quiet")
    p.add_argument("-u", "--uuid", action="store_true")  # <-- short alias added
    p.add_argument("--wordlist", metavar="PATH")
    p.add_argument("--all-words", action="store_true")
    p.add_argument("--min-length", type=int, dest="min_length")
    p.add_argument("--max-length", type=int, dest="max_length")
    p.add_argument("--seed", type=int, help="Seed Python's random module for reproducible output")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of plain text/warnings")

    args = p.parse_args(argv)
    if args.qmark_help or args.std_help:
        print_help_and_exit()

    # Apply seed ASAP (affects word selection, caps choices, and separators)
    if args.seed is not None:
        random.seed(args.seed)

    def error_exit(msg, code=2):
        if args.json:
            return emit_json("error", {"error": msg}, code)
        print(msg, file=sys.stderr)
        return code

    # Validate length filters
    if args.min_length is not None and args.min_length < 1:
        return error_exit("Error: --min-length must be >= 1.")
    if args.max_length is not None and args.max_length < 1:
        return error_exit("Error: --max-length must be >= 1.")
    if (args.min_length is not None and args.max_length is not None
            and args.min_length > args.max_length):
        return error_exit("Error: --min-length cannot be greater than --max-length.")

    wordlist_path = Path(args.wordlist) if args.wordlist else DEFAULT_WORDLIST

    if args.all_words:
        try:
            content = wordlist_path.read_text(encoding="utf-8").rstrip("\n")
        except Exception as e:
            return error_exit("Error reading wordlist {}: {}".format(wordlist_path, e))
        if args.json:
            return emit_json("ok", {"mode": "all-words", "output": content, "warnings": [], "meta": {
                "wordlist": str(wordlist_path)
            }})
        print(content)
        return 0

    if args.uuid:
        u = str(uuid.uuid4())
        u = u.upper() if args.caps else u.lower()
        if args.json:
            return emit_json("ok", {"mode": "uuid", "output": u, "warnings": [], "meta": {
                "caps": bool(args.caps)
            }})
        print(u)
        return 0

    try:
        words = load_wordlist(wordlist_path)
    except Exception as e:
        return error_exit("Error: {}".format(e))

    words = filter_by_length(words, args.min_length, args.max_length)
    if not words:
        return error_exit("Error: no words remain after applying length filters.")

    words_count = args.words if args.words is not None else 1
    if words_count < MIN_WORDS or words_count > MAX_WORDS:
        return error_exit("Error: number of words must be between {} and {}. You asked for {}."
                          .format(MIN_WORDS, MAX_WORDS, words_count))

    if args.letter and args.no_dup_letters and words_count > 1:
        return error_exit("Error: --letter with --no-dup-letters is only valid when requesting a single word (-w 1).")

    pool = filter_by_letter(words, args.letter) if args.letter else list(words)
    if len(pool) < words_count:
        return error_exit("Error: only {} usable words available, but {} requested."
                          .format(len(pool), words_count))

    # Parse separators only if user supplied -s; otherwise keep None
    separators_spec = None
    if args.separators is not None:
        try:
            separators_spec = parse_separators(args.separators)
        except ValueError as e:
            return error_exit("Error parsing separators: {}".format(e))

    # Choose words (no duplicates); optionally enforce unique starting letters
    try:
        if args.no_dup_letters and words_count > 1:
            chosen_words = pick_words_no_dup_letters(pool, words_count)
        else:
            chosen_words = random.sample(pool, words_count)
    except ValueError as e:
        if args.no_dup_letters and words_count > 1:
            distinct_letters = len({w[0].lower() for w in pool if w})
            return error_exit(("Error: {} (pool has {} distinct starting letters after filters). "
                               "Relax constraints or lower -w.").format(e, distinct_letters))
        return error_exit("Error: {}".format(e))

    single_word_always_cap = (words_count == 1 and args.caps)
    slots = max(0, words_count - 1)

    # For multi-word phrases, default separators to dashes if user didn't specify -s
    effective_separators = separators_spec
    if words_count > 1 and effective_separators is None:
        effective_separators = ["dashes"]

    # Warning condition is based ONLY on explicit concrete kinds (random is not required)
    explicit_concrete = []
    if effective_separators is not None:
        explicit_concrete = [t for t in effective_separators if t in BASIC_KINDS]
    distinct_required = len(set(explicit_concrete))
    warn_impossible_cover = (words_count >= 2) and (distinct_required > slots)

    warnings_out = []
    meta = {
        "mode": "words",
        "seed": args.seed,
        "wordlist": str(wordlist_path),
        "words_count": words_count,
        "caps": bool(args.caps),
        "letter": args.letter if args.letter else None,
        "min_length": args.min_length,
        "max_length": args.max_length,
        "no_dup_letters": bool(args.no_dup_letters),
        "separator_spec": separators_spec,          # what user provided (canonical tokens) or None
        "effective_separator_spec": effective_separators,  # the spec actually used (defaults applied)
        "chosen_words": chosen_words[:],
    }

    # Single-word behavior:
    if words_count == 1:
        base = apply_caps_to_word(chosen_words[0], args.caps, single_word_always_cap)
        if effective_separators is None:
            output = base
            if args.json:
                meta.update({
                    "appended_separator": None,
                    "separators_used": [],
                    "covered_all_required": True
                })
                return emit_json("ok", {"mode": "words", "output": output, "warnings": warnings_out, "meta": meta})
            print(output)
            return 0
        # -s provided: append exactly one chosen separator
        sep_str, picked_token = choose_single_separator(effective_separators)
        output = base + sep_str
        meta.update({
            "appended_separator": {"token": picked_token, "rendered": sep_str},
            "separators_used": [sep_str],
            "covered_all_required": True
        })
        if not args.quiet and len(set(effective_separators)) > 1:
            warnings_out.append("(Note: multiple -s kinds provided; appended one at random: '{}')".format(picked_token))
        if args.json:
            return emit_json("ok", {"mode": "words", "output": output, "warnings": warnings_out, "meta": meta})
        print(output)
        for w in warnings_out:
            print(w, file=sys.stderr)
        return 0

    # Multi-word: ensure coverage of explicit concrete kinds when possible
    sep_slots, covered_all, chosen_sep_tokens = choose_separators_cover_all(effective_separators, slots)
    meta.update({
        "separators_used": sep_slots,     # rendered separators used between words
        "chosen_separator_tokens": chosen_sep_tokens,  # canonical tokens picked per slot
        "covered_all_required": bool(covered_all),
    })
    output = build_passphrase(chosen_words, sep_slots, args.caps, single_word_always_cap)

    if not args.quiet and warn_impossible_cover and not covered_all:
        kinds_list = sorted(set(explicit_concrete))
        warnings_out.append(
            "Warning: you requested {} words ({} separator slot{}) but specified {} different separator kind{}: {}. "
            "It’s not possible to include every kind at least once with the available slots."
            .format(
                words_count,
                slots,
                "" if slots == 1 else "s",
                distinct_required,
                "" if distinct_required == 1 else "s",
                ", ".join(kinds_list) if kinds_list else "(none)"
            )
        )

    if args.json:
        return emit_json("ok", {"mode": "words", "output": output, "warnings": warnings_out, "meta": meta})

    # Plain-text mode
    print(output)
    for w in warnings_out:
        print(w, file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
