import re

REGEX_SPEAKER = re.compile(
    r''.join([
        r'^([\w_]+)',                   # Username.
        r'(?:\|([^":\s]+|"[^":]+"))?',  # Forced nickname.
        r':',
    ]),
    re.MULTILINE)

REGEX_REFERENCE = re.compile(
    r''.join([
        r'(^|[^\\])@',                  # Mark reference.
        r'([\w_]+)\b',                  # Username.
        r'(?:\|([^"\s]+|"[^"]+"))?',    # Forced nickname.
    ]),
    re.MULTILINE)
