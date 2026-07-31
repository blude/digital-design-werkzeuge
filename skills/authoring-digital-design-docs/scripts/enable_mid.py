#!/usr/bin/env python3
"""Turn StrictDoc machine identifiers (MIDs) on or off across a project.

A MID is a generated 32-character identifier that StrictDoc attaches to a node
alongside its human UID. Its value is that it **survives a UID rename and a node
move**, so a diff between two revisions can tell a renamed requirement from a
deleted one plus a new one. Without MIDs that distinction is guesswork.

MIDs are off by default in this framework because they cost one opaque line per
node in documents whose value depends on being readable by people. Enable them
when a document set is stable enough that renames and history matter more than
the noise — typically once it is under review rather than under construction.

What enabling does:

  1. Adds a `MID` field to every element of every grammar, inline or `.sgra`.
     StrictDoc requires this: with `ENABLE_MID: True` and an element missing the
     field, it refuses to parse.
  2. Adds `ENABLE_MID: True` as the first key of each document's `OPTIONS`.
  3. Leaves the values to StrictDoc. Run `strictdoc format .` afterwards to
     inject them — `export` does not write back.

What disabling does:

  Sets `ENABLE_MID: False` — which is what `strictdoc format` itself writes when
  the feature is off. The `MID` fields and their values stay, deliberately: they
  are inert without the setting, and discarding them would throw away the
  identity history that made them worth having. Re-enabling picks up where it
  left off.

Usage:
    python3 enable_mid.py [project-root] [--disable] [--dry-run]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdoc  # noqa: E402

MID_FIELD = ["  - TITLE: MID", "    TYPE: String", "    REQUIRED: False"]

# Document header fields, in the order StrictDoc requires. OPTIONS must be
# inserted after the last of these that is present.
HEADER_ORDER = ["TITLE", "UID", "VERSION", "DATE", "CLASSIFICATION", "PREFIX", "ROOT"]


def add_mid_to_grammar(lines: list[str]) -> tuple[list[str], int]:
    """Insert a MID field declaration after each element's `FIELDS:` line."""
    out: list[str] = []
    added = 0
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if lines[i].startswith("- TAG: "):
            # walk to this element's FIELDS: line
            j = i + 1
            while j < len(lines) and not lines[j].startswith("- TAG: "):
                if lines[j] == "  FIELDS:":
                    break
                j += 1
            if j < len(lines) and lines[j] == "  FIELDS:":
                # already declared?
                k = j + 1
                has_mid = False
                while k < len(lines) and not lines[k].startswith("- TAG: "):
                    if lines[k].strip() == "- TITLE: MID":
                        has_mid = True
                        break
                    k += 1
                out.extend(lines[i + 1:j + 1])
                if not has_mid:
                    out.extend(MID_FIELD)
                    added += 1
                i = j + 1
                continue
        i += 1
    return out, added


def set_enable_mid(lines: list[str], enable: bool) -> tuple[list[str], bool]:
    """Set `ENABLE_MID` to True or False as the first key of OPTIONS.

    `strictdoc format` writes the key explicitly as `ENABLE_MID: False`, so a
    project that has ever been formatted already has it. The value must be
    flipped rather than the key inserted, or enabling silently does nothing.
    """
    want = "  ENABLE_MID: True" if enable else "  ENABLE_MID: False"

    for idx, ln in enumerate(lines):
        if ln.strip().startswith("ENABLE_MID:"):
            if ln == want:
                return lines, False
            return lines[:idx] + [want] + lines[idx + 1:], True

    if not enable:
        return lines, False  # absent means already off

    if "OPTIONS:" in lines:
        idx = lines.index("OPTIONS:")
        return lines[:idx + 1] + [want] + lines[idx + 1:], True

    # no OPTIONS block — insert one after the last header field present
    last = -1
    for idx, ln in enumerate(lines[:40]):
        name = ln.split(":", 1)[0]
        if name in HEADER_ORDER:
            last = idx
    if last < 0:
        return lines, False
    return lines[:last + 1] + ["OPTIONS:", want] + lines[last + 1:], True


def inline_grammar_span(lines: list[str]) -> tuple[int, int] | None:
    """Locate an inline [GRAMMAR] block, if the document has one."""
    try:
        start = lines.index("[GRAMMAR]")
    except ValueError:
        return None
    if start + 1 < len(lines) and lines[start + 1].startswith("IMPORT_FROM_FILE:"):
        return None
    end = start + 1
    while end < len(lines) and not re.match(r"^\[\[?[A-Z]", lines[end]):
        end += 1
    return start, end


def main(argv: list[str]) -> int:
    disable = "--disable" in argv
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path.cwd()

    sdocs = sorted(root.rglob("*.sdoc"))
    sgras = sorted(root.rglob("*.sgra"))
    if not sdocs:
        print(f"No .sdoc files found under {root}.")
        return 1

    action = "Disabling" if disable else "Enabling"
    print(f"{action} MIDs under {root}" + (" (dry run)" if dry else ""))
    print()

    changes: list[tuple[Path, str]] = []

    if not disable:
        for path in sgras:
            lines = path.read_text(encoding="utf-8").split("\n")
            new, added = add_mid_to_grammar(lines)
            if added:
                changes.append((path, f"MID field added to {added} element(s)"))
                if not dry:
                    path.write_text("\n".join(new), encoding="utf-8")

    for path in sdocs:
        lines = path.read_text(encoding="utf-8").split("\n")
        notes: list[str] = []

        if not disable:
            span = inline_grammar_span(lines)
            if span:
                start, end = span
                block, added = add_mid_to_grammar(lines[start:end])
                if added:
                    lines = lines[:start] + block + lines[end:]
                    notes.append(f"inline grammar: MID added to {added} element(s)")

        lines, touched = set_enable_mid(lines, enable=not disable)
        if touched:
            notes.append(
                "ENABLE_MID set to False" if disable else "ENABLE_MID set to True"
            )

        if notes:
            changes.append((path, "; ".join(notes)))
            if not dry:
                path.write_text("\n".join(lines), encoding="utf-8")

    if not changes:
        print("Nothing to change — the project is already in the requested state.")
        return 0

    for path, note in changes:
        print(f"  {sdoc.relpath(str(path))}: {note}")
    print()

    if dry:
        print("Dry run — nothing written. Re-run without --dry-run to apply.")
        return 0

    if disable:
        print(
            "ENABLE_MID set to False. The MID fields and values are intentionally\n"
            "left in place: they are inert without the setting, and keeping them\n"
            "preserves the identity history if you re-enable later."
        )
    else:
        print(
            "Next: run  strictdoc format .  to inject the MID values.\n"
            "`export` does not write back, so nothing is generated until you do.\n\n"
            "Commit before running format — it rewrites every document, and the\n"
            "first run produces a large diff that is almost entirely MID lines."
        )
    return 0


if __name__ == "__main__":
    sdoc.allow_pipe()
    sys.exit(main(sys.argv[1:]))
