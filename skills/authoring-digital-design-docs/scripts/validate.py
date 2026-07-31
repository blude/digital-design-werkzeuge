#!/usr/bin/env python3
"""Validate a design-document project: syntax, relations, and structure.

Runs the whole verification chain in the order that fails fastest:

  1. `strictdoc export` — syntax, grammar conformance, relation targets.
     Authoritative. If this fails, nothing else is worth running, because the
     documents could not be parsed.
  2. Attribute reference check — the entity attribute IDs StrictDoc cannot
     link-check.
  3. Coverage check — the framework's own traceability expectations.

Usage:
    python3 validate.py [project-root]
    python3 validate.py --quick        # skip strictdoc, structural checks only

Exit status is 0 only if every stage passes, so this is usable as a CI gate.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdoc  # noqa: E402

HERE = Path(__file__).resolve().parent


def rule(title: str) -> None:
    print(f"\n{'─' * 66}\n{title}\n{'─' * 66}")


def run_strictdoc(root: Path) -> tuple[bool, str]:
    """Export to a throwaway directory and return (ok, output)."""
    if shutil.which("strictdoc") is None:
        return False, (
            "strictdoc is not on PATH.\n"
            "Install it with:  pip install strictdoc --break-system-packages"
        )
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            ["strictdoc", "export", ".", "--output-dir", tmp],
            cwd=root,
            capture_output=True,
            text=True,
        )
    combined = proc.stdout + proc.stderr
    errors = [
        ln for ln in combined.split("\n")
        if "error" in ln.lower() and "error source:" not in ln.lower()
    ]
    if errors:
        return False, "\n".join(errors)
    return True, "No syntax errors. Every relation target resolves."


def run_check(script: str, root: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(HERE / script), str(root)],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).rstrip()


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--quick"]
    quick = "--quick" in argv
    root = Path(args[0]).resolve() if args else Path.cwd()

    if not any(root.rglob("*.sdoc")):
        print(f"No .sdoc files found under {root}.")
        print("Run this from the project root — the directory containing docs/.")
        return 1

    failed: list[str] = []

    if not quick:
        rule("1/3  strictdoc export — syntax, grammar, relation targets")
        ok, out = run_strictdoc(root)
        print(out)
        if not ok:
            failed.append("strictdoc export")
            print(
                "\nStopping here. The documents did not parse, so the structural\n"
                "checks below would report against an incomplete reading.\n"
                "Fix these first — the error message names the field order it\n"
                "received, or the line it choked on."
            )
            return 1
    else:
        print("Skipping strictdoc export (--quick).")

    rule(f"{'2/3' if not quick else '1/2'}  entity attribute references")
    ok, out = run_check("check_attribute_refs.py", root)
    print(out)
    if not ok:
        failed.append("attribute references")

    rule(f"{'3/3' if not quick else '2/2'}  framework coverage expectations")
    ok, out = run_check("check_coverage.py", root)
    print(out)
    if not ok:
        failed.append("coverage")

    rule("result")
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("All checks passed.")
    print("\nFor the shape of the graph rather than its correctness:")
    print("    python3 trace_report.py")
    print("    python3 trace_report.py --chain <UID>")
    return 0


if __name__ == "__main__":
    sdoc.allow_pipe()
    sys.exit(main(sys.argv[1:]))
