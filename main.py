"""The Printer Apology — make.fun entry.

Writes one line (<=120 chars) to /output/entry.txt.
Output resolution order: ENTRY_OUT (file or dir) -> MAKEFUN_OUTPUT_DIR
-> /output/entry.txt -> ./entry.txt (last resort).
"""

import os

def _apology():
    return "Sorry I jammed during your big presentation."


def _punch():
    return (
        "In my defence, your slides were the first thing "
        "to bore me to death."
    )


def build_entry():
    """Assemble the single entry line: apology first, punch last."""
    return _apology() + " " + _punch()


ENTRY_TEXT = build_entry()


def _validate(text):
    """The sealed gate needs 1-120 UTF-8 chars, not only whitespace."""
    if not 1 <= len(text) <= 120 or not text.strip():
        raise ValueError("entry must be 1-120 non-blank characters")
    return text


def resolve_output_path():
    """Pick where the entry text goes, in priority order."""
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        if os.path.isdir(entry_out):
            return os.path.join(entry_out, "entry.txt")
        return entry_out
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.txt"
    return os.path.join(os.getcwd(), "entry.txt")


def write_entry(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main():
    text = _validate(build_entry())
    path = resolve_output_path()
    write_entry(path, text)


if __name__ == "__main__":
    main()
