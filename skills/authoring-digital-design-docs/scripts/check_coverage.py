#!/usr/bin/env python3
"""Check the traceability expectations the framework states but StrictDoc cannot.

StrictDoc verifies that every relation target exists. It has no opinion on
which relations *should* exist. This script checks the framework's own rules:

  1. Downward coverage — "every system goal should have at least one system
     scenario demonstrating how the system achieves it", and the equivalent for
     element goals and expected impacts.
  2. Upward parents — a requirement that traces to nothing above it is either
     gold-plating or a forgotten link. Legitimate exceptions are marked with
     `EXTERNALLY_SOURCED: Yes`, `ELEMENT_SPECIFIC: Yes` or `DERIVED: Yes`, and
     are reported separately rather than as errors.
  3. Undeclared mentions — prose claiming a relationship the relations do not
     declare. A scenario whose text says it demonstrates two goals while
     declaring one is the failure this catches.

Role names are treated as expectations rather than requirements: the checks match
on which nodes point at which, so a project that customised the grammar's roles
still passes, with any divergence reported as information rather than an error.

A rule is skipped entirely when no node of the relevant kind exists in the
project, so writing one level in isolation produces no spurious findings.

Usage:
    python3 check_coverage.py [project-root]

Exit status is 1 if any error-level finding is present, 0 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdoc  # noqa: E402

# parent prefix -> (child prefixes that should point at it, role, why)
INBOUND_EXPECTED = {
    "SG": (("SSc",), "Achieves",
           "every system goal needs a scenario demonstrating how it is achieved"),
    "G": (("UC", "TF"), "Achieves",
          "every element goal needs a use case or technical function achieving it"),
    "IMP": (("SUC",), "Measures",
            "every expected impact should have a success criterion measuring it"),
}

# child prefix -> (acceptable parent prefixes, role or None for any, exempt field)
UPWARD_EXPECTED = {
    "BG": (("IMP",), "Satisfies", None),
    "VP": (("BG",), "Satisfies", None),
    "VCA": (("VP",), "Realises", None),
    "BP": (("BG",), "Supports", None),
    "BQR": (("BG",), "Satisfies", None),
    "BC": (("BRC",), "Refines", None),
    "SG": (("BG",), "Satisfies", None),
    "UT": (("VCA",), "Represents", None),
    "SE": (("VCA",), "Realises", None),
    "SSc": (("SG",), "Achieves", None),
    "SQR": (("BQR",), "Supports", "EXTERNALLY_SOURCED"),
    "SC": (("BC",), "Refines", "EXTERNALLY_SOURCED"),
    "G_L3": (("SG",), "Satisfies", None),
    "UC": (("SSc",), "Realises", None),
    "QR": (("SQR",), "Supports", "ELEMENT_SPECIFIC"),
    "C": (("SC",), "Implements", "ELEMENT_SPECIFIC"),
    "SUC": (("IMP",), "Measures", None),
    "E": (("BE",), "Refines", None),
}

# Alternative-flow nodes must always anchor to a step.
ANCHOR_REQUIRED = {"EX": "ST", "PA": "PS", "SA": "SSt", "FA": "FS"}


def prefixes_present(nodes: list[sdoc.Node]) -> set[str]:
    return {n.prefix for n in nodes if n.prefix}


def exempt(node: sdoc.Node, field_name: str | None) -> bool:
    if not field_name:
        return False
    return node.fields.get(field_name, "").strip() == "Yes"


def main(root: str = ".") -> int:
    nodes = sdoc.load(root)
    if not nodes:
        print(f"No .sdoc files found under {root!r}.")
        return 0

    present = prefixes_present(nodes)
    rev = sdoc.incoming(nodes)
    errors = 0
    warnings = 0
    divergent: list[str] = []

    # ---------------------------------------------------------------- inbound
    lines: list[str] = []
    for parent_prefix, (child_prefixes, role, why) in INBOUND_EXPECTED.items():
        if parent_prefix not in present:
            continue
        if not any(c in present for c in child_prefixes):
            continue  # the child section was not written; not our business
        uncovered = []
        for node in nodes:
            if node.prefix != parent_prefix or not node.uid:
                continue
            sources = [
                (src, r) for src, r in rev.get(node.uid, [])
                if src.prefix in child_prefixes
            ]
            if not sources:
                uncovered.append(node)
                continue
            # covered — but flag a role this framework would not have used
            for src, r in sources:
                if r != role:
                    divergent.append(
                        f"    {src.uid} → {node.uid} uses {r!r};"
                        f" this framework uses {role!r}"
                    )
        if uncovered:
            errors += len(uncovered)
            lines.append(f"  {why}:")
            for node in uncovered:
                lines.append(
                    f"    {node.uid} {node.title}"
                    f"  — no {'/'.join(child_prefixes)} declares {role}"
                )
    if lines:
        print("ERROR — missing downward coverage:")
        print("\n".join(lines))
        print()

    # ---------------------------------------------------------------- upward
    missing: list[str] = []
    exempted: list[str] = []
    for node in nodes:
        if not node.uid or not node.prefix:
            continue
        # L3 goals share the `G` prefix; distinguish by their expected parent
        key = node.prefix
        if key == "G" and "SG" in present:
            key = "G_L3"
        rule = UPWARD_EXPECTED.get(key)
        if not rule:
            continue
        parents, role, exempt_field = rule
        if not any(p in present for p in parents):
            continue  # that level is not in this project
        matching = [
            r for r in node.relations
            if r.get("VALUE")
            and any(r["VALUE"].startswith(p + "-") for p in parents)
        ]
        if matching:
            for r in matching:
                if r.get("ROLE") != role:
                    divergent.append(
                        f"    {node.uid} → {r['VALUE']} uses {r.get('ROLE')!r};"
                        f" this framework uses {role!r}"
                    )
            continue
        entry = (
            f"    {node.uid} {node.title}"
            f"  — expected {role} → {'/'.join(parents)}"
        )
        if exempt(node, exempt_field):
            exempted.append(entry + f"  [{exempt_field}: Yes]")
        else:
            missing.append(entry)

    for node in nodes:
        if node.prefix in ANCHOR_REQUIRED and node.uid:
            want = ANCHOR_REQUIRED[node.prefix]
            if not any(t.startswith(want + "-") for t in node.targets("Extends")):
                missing.append(
                    f"    {node.uid} {node.title}"
                    f"  — alternative flow with no Extends → {want}"
                )

    if missing:
        errors += len(missing)
        print("ERROR — missing upward relations:")
        print("\n".join(missing))
        print()

    if exempted:
        print("INFO — no upward relation, but explicitly marked as expected:")
        print("\n".join(exempted))
        print()

    # ------------------------------------------------------ undeclared mentions
    flagged: list[str] = []
    for parent_prefix, (child_prefixes, role, _why) in INBOUND_EXPECTED.items():
        pattern = re.compile(rf"\b({parent_prefix}-\d+)\b")
        for node in nodes:
            if node.prefix not in child_prefixes or not node.uid:
                continue
            declared = set(node.targets())
            mentioned = set(pattern.findall(node.text())) - declared
            mentioned = {m for m in mentioned if m in {n.uid for n in nodes}}
            for m in sorted(mentioned):
                flagged.append(
                    f"    {node.uid} mentions {m} in its text"
                    f" but declares no {role} relation to it"
                )
    if flagged:
        warnings += len(flagged)
        print("WARNING — prose mentions a relationship the relations do not declare:")
        print("\n".join(flagged))
        print(
            "  Some of these are legitimate context. Check each: if the node really\n"
            "  does what the prose says, the relation is missing.\n"
        )

    if divergent:
        print("INFO — relations using a different role than this framework expects:")
        print("\n".join(sorted(set(divergent))))
        print(
            "  Not an error. The coverage checks match on which nodes point at which,\n"
            "  so a customised grammar still passes. Worth a look only if the\n"
            "  divergence was unintentional.\n"
        )

    counted = sum(1 for n in nodes if n.uid)
    print(f"{counted} identified nodes checked, {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sdoc.allow_pipe()
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
