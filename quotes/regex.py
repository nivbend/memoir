import re

REGEX_SPEAKER = re.compile(r'^([\w_]+):', re.MULTILINE)
REGEX_REFERENCE = re.compile(r'(?:^|[^\\])@([\w_]+)\b', re.MULTILINE)
