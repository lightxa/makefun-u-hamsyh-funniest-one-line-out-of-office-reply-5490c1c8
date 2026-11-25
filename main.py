"""Funniest One-Line Out-of-Office Reply.

Writes a single original out-of-office auto-reply line to
/output/entry.txt. Pure standard library, deterministic, no network.

The joke: one small, specific scene named once (Gary, the office
houseplant, covering for the sender), the away message itself
carries the punchline, and it stays short enough to take in at
a glance. No beach, no inbox, no "limited email access".
"""

import os
from pathlib import Path

# The entry: one line, a real away message with a return day,
# a named stand-in, and a self-deprecating punchline.
ENTRY = (
    "I'm away until Monday. My replacement is a houseplant named Gary, "
    "and frankly he's more responsive than I am."
)

# The harness contract: the text goes to /output/entry.txt.
# An environment override exists only so the program can be
# exercised locally where /output is not writable; the graded
# run uses the default path.
DEFAULT_OUTPUT = Path("/output/entry.txt")


def output_path() -> Path:
    override = os.environ.get("MAKEFUN_OUTPUT")
    if override:
        return Path(override)
    return DEFAULT_OUTPUT


def validate(text: str) -> str:
    """Enforce the gate: 1 to 160 characters, one line, not blank."""
    if not 1 <= len(text) <= 160:
        raise ValueError(f"entry is {len(text)} characters, must be 1-160")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def main() -> None:
    text = validate(ENTRY)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write the text exactly as judged, with no trailing newline,
    # so the file is byte-identical to the judged line.
    path.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} characters to {path}")


if __name__ == "__main__":
    main()
