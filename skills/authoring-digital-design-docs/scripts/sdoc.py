"""Minimal SDoc reader for the design-document checks.

Parses just enough of StrictDoc's SDoc format to support structural checks that
StrictDoc itself does not perform. Not a substitute for `strictdoc export`,
which remains the authority on syntax and relation validity — run that first.

Pure standard library. StrictDoc requires Python, so nothing extra is needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

NODE_OPEN = re.compile(r"^\[\[?([A-Z][A-Z0-9_]*)\]\]?$")
NODE_CLOSE = re.compile(r"^\[\[/([A-Z][A-Z0-9_]*)\]\]$")
FIELD_START = re.compile(r"^([A-Z][A-Z0-9_]*): ?(.*)$")
REL_TYPE = re.compile(r"^- TYPE: (.+)$")
REL_ATTR = re.compile(r"^  ([A-Z_]+): (.+)$")

# Fields that hold prose rather than a single value. Everything not listed is
# still captured; this set only documents intent.
MULTILINE_SENTINEL_OPEN = ">>>"
MULTILINE_SENTINEL_CLOSE = "<<<"


@dataclass
class Node:
    tag: str
    file: str
    line: int
    uid: str | None = None
    fields: dict[str, str] = field(default_factory=dict)
    relations: list[dict[str, str]] = field(default_factory=list)

    @property
    def prefix(self) -> str | None:
        """The ID prefix, e.g. 'SG' for 'SG-01'."""
        if not self.uid:
            return None
        m = re.match(r"^([A-Za-z]+)-", self.uid)
        return m.group(1) if m else None

    @property
    def title(self) -> str:
        return self.fields.get("TITLE", "").strip()

    def text(self) -> str:
        """All field values concatenated — for scanning prose for references."""
        return "\n".join(self.fields.values())

    def targets(self, role: str | None = None) -> list[str]:
        return [
            r["VALUE"]
            for r in self.relations
            if "VALUE" in r and (role is None or r.get("ROLE") == role)
        ]

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.tag} {self.uid or '(no uid)'} {self.file}:{self.line}>"


def parse_file(path: Path) -> list[Node]:
    """Parse one .sdoc file into a flat list of nodes.

    Composite nesting is not modelled: children appear as siblings, which is
    all the checks need. GRAMMAR blocks are skipped, since an inline grammar
    contains field declarations that would otherwise look like node fields.
    """
    nodes: list[Node] = []
    lines = path.read_text(encoding="utf-8").split("\n")
    i = 0
    current: Node | None = None
    in_grammar = False

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if NODE_CLOSE.match(stripped):
            i += 1
            continue

        m = NODE_OPEN.match(stripped)
        if m:
            tag = m.group(1)
            in_grammar = tag == "GRAMMAR"
            if in_grammar:
                current = None
            else:
                current = Node(tag=tag, file=str(path), line=i + 1)
                nodes.append(current)
            i += 1
            continue

        if in_grammar or current is None:
            i += 1
            continue

        if stripped == "RELATIONS:":
            i += 1
            rel: dict[str, str] | None = None
            while i < len(lines):
                line = lines[i]
                mt = REL_TYPE.match(line)
                if mt:
                    rel = {"TYPE": mt.group(1).strip()}
                    current.relations.append(rel)
                    i += 1
                    continue
                ma = REL_ATTR.match(line)
                if ma and rel is not None:
                    rel[ma.group(1)] = ma.group(2).strip()
                    i += 1
                    continue
                break
            continue

        mf = FIELD_START.match(raw)
        if mf:
            name, rest = mf.group(1), mf.group(2)
            if rest.strip() == MULTILINE_SENTINEL_OPEN:
                body: list[str] = []
                i += 1
                while i < len(lines) and lines[i].strip() != MULTILINE_SENTINEL_CLOSE:
                    body.append(lines[i])
                    i += 1
                i += 1
                value = "\n".join(body)
            else:
                value = rest
                i += 1
            current.fields[name] = value
            if name == "UID":
                current.uid = value.strip()
            continue

        i += 1

    return nodes


def load(root: str | Path = ".") -> list[Node]:
    """Parse every .sdoc file under `root`."""
    root = Path(root)
    paths = sorted(root.rglob("*.sdoc"))
    nodes: list[Node] = []
    for p in paths:
        nodes.extend(parse_file(p))
    return nodes


def by_uid(nodes: list[Node]) -> dict[str, Node]:
    """Index nodes by UID. Later duplicates do not overwrite earlier ones —
    duplicate UIDs are StrictDoc's error to report, not ours."""
    index: dict[str, Node] = {}
    for n in nodes:
        if n.uid and n.uid not in index:
            index[n.uid] = n
    return index


def incoming(nodes: list[Node]) -> dict[str, list[tuple[Node, str]]]:
    """Map target UID -> [(source node, role)]."""
    rev: dict[str, list[tuple[Node, str]]] = {}
    for n in nodes:
        for r in n.relations:
            target = r.get("VALUE")
            if target:
                rev.setdefault(target, []).append((n, r.get("ROLE", "")))
    return rev


def allow_pipe() -> None:
    """Exit quietly when output is piped into something that closes early,
    such as `| head`. Without this, Python raises BrokenPipeError on exit."""
    try:
        import signal

        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass  # not POSIX, or not the main thread


def relpath(path: str) -> str:
    """Shorten a path for readable output."""
    try:
        return str(Path(path).relative_to(Path.cwd()))
    except ValueError:
        return Path(path).name
