"""Copy the one-line lie from entry.txt to the output directory.

Stdlib only: the grader image has no third-party packages.
Reads entry.txt next to this file and writes it atomically to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt by default),
then validates the result: one line, 1-5 words, at most 88 chars.
"""

import os
import sys

MAX_CHARS = 88
MAX_WORDS = 5


def entry_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def read_line(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.strip().splitlines()
    if len(lines) != 1:
        raise ValueError("entry.txt must contain exactly one line")
    return lines[0]


def validate(line):
    words = line.split()
    if not 1 <= len(words) <= MAX_WORDS:
        raise ValueError("lie must be 1-%d words, got %d" % (MAX_WORDS, len(words)))
    if len(line) > MAX_CHARS:
        raise ValueError("lie must be at most %d chars, got %d" % (MAX_CHARS, len(line)))
    if not line.strip():
        raise ValueError("lie must not be empty")
    if line != line.strip():
        raise ValueError("lie must not have leading or trailing whitespace")
    if len(line) >= 2 and line[0] in "\"'" and line[-1] == line[0]:
        raise ValueError("lie must not be wrapped in quotes")


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def main():
    line = read_line(entry_path())
    validate(line)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    write_atomic(out_path, line + "\n")
    written = read_line(out_path)
    validate(written)
    if written != line:
        raise ValueError("output does not match entry.txt")
    print("wrote %s (%d words, %d chars)" % (out_path, len(line.split()), len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
