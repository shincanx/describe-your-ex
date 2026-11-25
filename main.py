"""Describe Your Ex in One Word -- make.fun entry.

Writes a single word describing an ex (at most 111 characters) to
entry.txt in the output directory. Deterministic, no network, no
randomness, no input.

The word: "typo" -- the whole relationship was a typo. A small,
accidental error in the text of your life, the kind you backspace
without a second thought. Instantly a verdict on the ex (what they
were, not what happened), with a twist no one sees coming, and
everyone who has ever typed -- or dated -- recognises it at once.
"""

import os

# The entry: one word, a verdict on an ex. 4 characters, under the 111 cap.
WORD = "typo"


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(WORD) > 111:
        raise ValueError(f"word is {len(WORD)} characters, over the 111 cap")
    if len(WORD.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not WORD.strip():
        raise ValueError("entry must not be only whitespace")
    if not WORD.isalpha():
        # Craft: exactly one word, spelled correctly, no punctuation
        # tricks -- letters only, so the verdict arrives unadorned.
        raise ValueError("entry must be letters only, no punctuation tricks")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(WORD + "\n")

    # Round-trip check: what landed on disk is exactly the word.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != WORD:
        raise ValueError("entry.txt does not match the word")

    print(f"wrote {len(WORD)} characters to {path}")


if __name__ == "__main__":
    main()
