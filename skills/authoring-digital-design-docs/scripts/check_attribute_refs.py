#!/usr/bin/env python3
"""Check entity attribute references, which StrictDoc cannot validate.

Entity attributes are declared as table rows inside an entity's ATTRIBUTES
field, with IDs of the form `E-01.1`. Technical function steps and user
interface specifications reference those IDs in prose. Because the IDs are
table content rather than node UIDs, StrictDoc does not link-check them — a
renamed or renumbered attribute leaves stale references behind with no error.

This script closes that gap. It reports:

  1. References to attribute IDs that no entity declares
  2. Attribute IDs declared under the wrong entity (e.g. E-02.3 inside E-01)
  3. Duplicate attribute IDs within one entity
  4. Declared attributes that nothing references (informational only)

Usage:
    python3 check_attribute_refs.py [project-root]

Exit status is 1 if any error-level finding is present, 0 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdoc  # noqa: E402

# `| E-01.1 | attributeName | type | required | description |`
TABLE_ROW = re.compile(r"^\s*\|\s*([A-Za-z]+-\d+\.\d+)\s*\|\s*([^|]*)\|")
# Any attribute-style reference in prose
ATTR_REF = re.compile(r"\b([A-Za-z]+-\d+\.\d+)\b")

# Fields whose content is a declaration table rather than a reference.
DECLARING_FIELDS = ("ATTRIBUTES", "KEY_INFORMATION")


def main(root: str = ".") -> int:
    nodes = sdoc.load(root)
    if not nodes:
        print(f"No .sdoc files found under {root!r}.")
        return 0

    declared: dict[str, tuple[sdoc.Node, str]] = {}
    misplaced: list[tuple[sdoc.Node, str]] = []
    duplicates: list[tuple[sdoc.Node, str]] = []

    # --- collect declarations
    for node in nodes:
        for fname in DECLARING_FIELDS:
            body = node.fields.get(fname)
            if not body:
                continue
            seen_here: set[str] = set()
            for line in body.split("\n"):
                m = TABLE_ROW.match(line)
                if not m:
                    continue
                attr_id, attr_name = m.group(1), m.group(2).strip()
                if attr_id in seen_here:
                    duplicates.append((node, attr_id))
                seen_here.add(attr_id)
                owner = attr_id.rsplit(".", 1)[0]
                if node.uid and owner != node.uid:
                    misplaced.append((node, attr_id))
                declared.setdefault(attr_id, (node, attr_name))

    # --- collect references, skipping the declaration tables themselves
    references: dict[str, list[sdoc.Node]] = {}
    for node in nodes:
        for fname, body in node.fields.items():
            if fname in DECLARING_FIELDS:
                continue
            for attr_id in set(ATTR_REF.findall(body)):
                references.setdefault(attr_id, []).append(node)

    unknown = {a: ns for a, ns in references.items() if a not in declared}
    unreferenced = sorted(set(declared) - set(references))

    # --- report
    errors = 0

    if unknown:
        errors += len(unknown)
        print("ERROR — references to attribute IDs that no entity declares:")
        for attr_id in sorted(unknown):
            owner = attr_id.rsplit(".", 1)[0]
            hint = (
                f"entity {owner} exists but has no {attr_id}"
                if any(n.uid == owner for n in nodes)
                else f"no entity {owner} exists"
            )
            print(f"  {attr_id}  ({hint})")
            for node in unknown[attr_id]:
                print(
                    f"      referenced by {node.uid or node.tag}"
                    f"  {sdoc.relpath(node.file)}:{node.line}"
                )
        print()

    if misplaced:
        errors += len(misplaced)
        print("ERROR — attribute IDs declared under the wrong entity:")
        for node, attr_id in misplaced:
            print(
                f"  {attr_id} declared inside {node.uid}"
                f"  {sdoc.relpath(node.file)}:{node.line}"
            )
        print()

    if duplicates:
        errors += len(duplicates)
        print("ERROR — duplicate attribute IDs within one entity:")
        for node, attr_id in duplicates:
            print(f"  {attr_id} in {node.uid}  {sdoc.relpath(node.file)}:{node.line}")
        print()

    if unreferenced:
        print("INFO — declared attributes nothing references:")
        for attr_id in unreferenced:
            node, name = declared[attr_id]
            print(f"  {attr_id} {name}  (in {node.uid})")
        print(
            "  Not a defect. An attribute can exist because the data needs it,\n"
            "  without any function step or interface naming it explicitly.\n"
        )

    total_refs = sum(len(v) for v in references.values())
    print(
        f"{len(declared)} attributes declared, "
        f"{len(references)} distinct referenced ({total_refs} references), "
        f"{errors} error(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sdoc.allow_pipe()
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
