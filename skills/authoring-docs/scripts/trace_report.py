#!/usr/bin/env python3
"""Report the shape of the traceability graph.

Not a check — nothing here fails. It answers the questions a reviewer asks
before reading a document set: how big is it, which levels exist, do the
relations run the way they should, and does any level look thin.

Usage:
    python3 trace_report.py [project-root] [--chain UID]

With `--chain UID`, walks upward from one node and prints the full ancestry,
which is the fastest way to check that a low-level requirement really does
reach a business impact.
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdoc  # noqa: E402

LEVEL_OF = {
    "IMP": "L0", "SO": "L0", "BRC": "L0", "SUC": "L0", "RSK": "L0",
    "REC": "L0", "SH": "L0", "RS": "L0",
    "BG": "L1", "VP": "L1", "VCA": "L1", "BE": "L1", "BP": "L1",
    "PS": "L1", "PA": "L1", "BQR": "L1", "BC": "L1",
    "SG": "L2", "AP": "L2", "UT": "L2", "SE": "L2", "HE": "L2",
    "PE": "L2", "SSc": "L2", "SSt": "L2", "SA": "L2", "SQR": "L2", "SC": "L2",
    "G": "L3", "UC": "L3", "ST": "L3", "EX": "L3", "UI": "L3",
    "TF": "L3", "FS": "L3", "FA": "L3", "TI": "L3", "TO": "L3",
    "E": "L3", "QR": "L3", "C": "L3",
}
ORDER = ["L0", "L1", "L2", "L3", "?"]

# Structural nodes are not requirements and are excluded from the counts.
STRUCTURAL = {"DOCUMENT", "SECTION", "TEXT", "GRAMMAR"}


def level(prefix: str | None) -> str:
    return LEVEL_OF.get(prefix or "", "?")


def chain(uid: str, index: dict[str, sdoc.Node], depth: int = 0,
          seen: set[str] | None = None) -> None:
    seen = seen or set()
    if uid in seen:
        print("  " * depth + f"{uid} (cycle)")
        return
    seen.add(uid)
    node = index.get(uid)
    if node is None:
        print("  " * depth + f"{uid} — not found")
        return
    print("  " * depth + f"{uid} [{level(node.prefix)}] {node.title}")
    for rel in node.relations:
        target = rel.get("VALUE")
        if target:
            role = rel.get("ROLE", "")
            print("  " * (depth + 1) + f"↑ {role}")
            chain(target, index, depth + 1, set(seen))


def main(argv: list[str]) -> int:
    root = "."
    want_chain = None
    args = argv[:]
    if "--chain" in args:
        i = args.index("--chain")
        want_chain = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if args:
        root = args[0]

    nodes = sdoc.load(root)
    if not nodes:
        print(f"No .sdoc files found under {root!r}.")
        return 0
    index = sdoc.by_uid(nodes)

    if want_chain:
        chain(want_chain, index)
        return 0

    identified = [n for n in nodes if n.uid and n.tag not in STRUCTURAL]
    edges = [(n, r) for n in nodes for r in n.relations if r.get("VALUE")]

    print(f"{len(identified)} identified nodes, {len(edges)} relations\n")

    # nodes per level
    per_level = collections.Counter(level(n.prefix) for n in identified)
    print("Nodes per level")
    for lv in ORDER:
        if per_level.get(lv):
            print(f"  {lv:4} {per_level[lv]}")
    print()

    # edges by role
    roles = collections.Counter(r.get("ROLE", "(none)") for _n, r in edges)
    print("Relations by role")
    for role, count in sorted(roles.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {role:18} {count}")
    print()

    # level crossings — the shape that matters
    crossings: collections.Counter = collections.Counter()
    for node, rel in edges:
        src = level(node.prefix)
        tgt_uid = rel["VALUE"]
        tgt_node = index.get(tgt_uid)
        tgt = level(tgt_node.prefix) if tgt_node else "?"
        crossings[(src, tgt)] += 1
    print("Level crossings (source → target)")
    for (src, tgt), count in sorted(
        crossings.items(), key=lambda kv: (ORDER.index(kv[0][0]) if kv[0][0] in ORDER else 9, kv[0][1])
    ):
        marker = ""
        if src in ORDER and tgt in ORDER and src != "?" and tgt != "?":
            si, ti = ORDER.index(src), ORDER.index(tgt)
            if si == ti:
                marker = "  within level"
            elif ti > si:
                marker = "  ** DOWNWARD — relations should point upward **"
        print(f"  {src} → {tgt}   {count}{marker}")
    print()

    # nodes per prefix, to spot a thin section
    per_prefix = collections.Counter(n.prefix for n in identified if n.prefix)
    print("Nodes per type")
    grouped: dict[str, list[tuple[str, int]]] = collections.defaultdict(list)
    for prefix, count in per_prefix.items():
        grouped[level(prefix)].append((prefix, count))
    for lv in ORDER:
        if lv not in grouped:
            continue
        items = ", ".join(f"{p}-{c}" for p, c in sorted(grouped[lv]))
        print(f"  {lv:4} {items}")
    print()

    # most-referenced nodes — usually the load-bearing requirements
    rev = sdoc.incoming(nodes)
    hot = sorted(rev.items(), key=lambda kv: -len(kv[1]))[:8]
    print("Most referenced (the load-bearing requirements)")
    for uid, sources in hot:
        node = index.get(uid)
        title = node.title if node else "(not found)"
        print(f"  {uid:10} {len(sources):3} incoming   {title}")

    return 0


if __name__ == "__main__":
    sdoc.allow_pipe()
    sys.exit(main(sys.argv[1:]))
