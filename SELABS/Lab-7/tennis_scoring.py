"""Tennis scoring helpers - hardened against malformed input (Lab 7).

Name : Muhammad Affan Dumba
SRN  : PES1UG24CS280

Contract
--------
Every public function accepts a ``strict`` keyword (default False):

* strict=False (default): the function is *total* - it never raises, whatever it
  is given (None, wrong type, empty text, huge text, unicode digits, ...).
    - valid input   -> the documented result
    - invalid input -> None
* strict=True: invalid input raises ``ValueError`` with a descriptive message
  instead of returning None (useful when the caller wants to know *why*).

Accepted formats
----------------
parse_score  : "A-B"          e.g. "3-2"      non-negative integers, up to 18 digits
game_lead    : "X-Y"          e.g. "40-30"    X, Y in 0, 15, 30, 40, AD (case-insensitive)
                              AD is only valid against 40 ("AD-40" or "40-AD")
set_spread   : "g1,g2,..."    e.g. "6,4,7"    non-negative integers, up to 18 digits each
Spaces around values/separators are ignored.
"""
import re

# Only plain ASCII digits are valid.  str.isdigit()/int() accept things such as
# superscripts or Arabic-Indic digits (and isdigit() even lies about some of
# them), so a strict regex is used instead.
MAX_DIGITS = 18            # far above any real score, far below Python's 4300-digit int() limit
MAX_INPUT_LEN = 100_000    # reject absurdly long input before doing any work

_NUMBER = r"[0-9]{1,%d}" % MAX_DIGITS
_SCORE_RE = re.compile(r"(%s)-(%s)" % (_NUMBER, _NUMBER))
_CSV_RE = re.compile(r"%s(?:,%s)*" % (_NUMBER, _NUMBER))
_SPACE_AROUND_COMMA_RE = re.compile(r"[ \t\r\n\f\v]*,[ \t\r\n\f\v]*")

# Point labels.  AD (advantage) counts as one point above 40.
_POINTS = {'0': 0, '15': 1, '30': 2, '40': 3, 'AD': 4}


def _fail(message, strict):
    """Reject invalid input: raise in strict mode, otherwise return None."""
    if strict:
        raise ValueError(message)
    return None


def _clean(text):
    """Return stripped text if `text` is a reasonably sized str, else None."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LEN:
        return None
    return text.strip()


def parse_score(text, strict=False):
    """Parse 'A-B' (e.g. '3-2') into (3, 2).  Returns None if invalid."""
    cleaned = _clean(text)
    if cleaned is None:
        return _fail("expected a string of at most %d characters" % MAX_INPUT_LEN, strict)
    m = _SCORE_RE.fullmatch(cleaned)
    if m is None:
        return _fail("expected 'A-B' with non-negative integers of at most %d "
                     "digits, e.g. '3-2'" % MAX_DIGITS, strict)
    return int(m.group(1)), int(m.group(2))


def _label_value(label):
    """Numeric value of a point label ('0','15','30','40','AD'), else None."""
    # .upper() is safe here: no non-ASCII character upper-cases to "AD".
    return _POINTS.get(label.strip().upper())


def game_lead(text, strict=False):
    """Lead of the first player in a game score such as '40-30' (-> 1).

    Valid labels: 0, 15, 30, 40 and AD (advantage, only against 40).
    Returns None if invalid.
    """
    cleaned = _clean(text)
    if cleaned is None:
        return _fail("expected a string of at most %d characters" % MAX_INPUT_LEN, strict)
    parts = cleaned.split('-')
    if len(parts) != 2:
        return _fail("expected two point labels separated by '-', e.g. '40-30'", strict)
    first, second = _label_value(parts[0]), _label_value(parts[1])
    if first is None or second is None:
        return _fail("point labels must be 0, 15, 30, 40 or AD", strict)
    # Advantage only exists against 40 (otherwise the game would be over).
    if (first == 4 and second != 3) or (second == 4 and first != 3):
        return _fail("AD is only valid against 40 ('AD-40' or '40-AD')", strict)
    return first - second


def set_spread(games_csv, strict=False):
    """Max minus min of comma separated games won, e.g. '6,4,7' -> 3.

    Returns None if the input is empty, has empty/non-numeric/negative items.
    """
    cleaned = _clean(games_csv)
    if cleaned is None:
        return _fail("expected a string of at most %d characters" % MAX_INPUT_LEN, strict)
    # tolerate spaces around the commas: '6, 4 ,7'
    cleaned = _SPACE_AROUND_COMMA_RE.sub(",", cleaned)
    if _CSV_RE.fullmatch(cleaned) is None:
        return _fail("expected comma separated non-negative integers of at most "
                     "%d digits, e.g. '6,4,7'" % MAX_DIGITS, strict)
    games = [int(g) for g in cleaned.split(',')]
    return max(games) - min(games)


# ---------------------------------------------------------------------------
# Command line interface
# ---------------------------------------------------------------------------
INVALID_MSG = "Invalid input - please follow the example format and try again."


def _ask(prompt, func, label):
    """Prompt until `func` accepts the answer.  Returns None on end of input."""
    while True:
        try:
            raw = input(prompt)
        except EOFError:          # stdin closed / piped input exhausted
            print()
            return None
        result = func(raw)
        if result is not None:
            print(label, result)
            return result
        print(INVALID_MSG)


def main():
    try:
        print("==== Running parse_score ====")
        _ask("Enter points won as A-B (e.g. 3-2): ", parse_score, "Points A and B:")

        print("\n==== Running game_lead ====")
        _ask("Enter a game score (e.g. 40-30): ", game_lead, "Lead in Points:")

        print("\n==== Running set_spread ====")
        _ask("Enter games won per set as CSV (e.g. 6,4,7): ", set_spread, "Spread:")
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()
