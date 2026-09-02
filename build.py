#!/usr/bin/env python3
"""Klistrar in gemensamma fragment (partials/) i sidorna.

En sida markerar var ett fragment ska in med ett kommentarspar:

    <!-- include:header -->
    <!-- /include:header -->

build.py byter ut allt mellan markörerna mot innehållet i
partials/header.html. Markörerna står kvar, så skriptet kan köras hur många
gånger som helst och alltid ge samma resultat. Filerna som ligger i repot är
de som deployas; det finns ingen separat utkatalog.

    python3 build.py          # uppdatera alla sidor
    python3 build.py --check  # avsluta med fel om någon sida är inaktuell
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PARTIALS = ROOT / "partials"
MARKER = re.compile(
    r"(?P<indent>[ \t]*)<!-- include:(?P<name>[\w-]+) -->\n"
    r".*?"
    r"[ \t]*<!-- /include:(?P=name) -->\n",
    re.S,
)


def expand(match):
    indent = match.group("indent")
    name = match.group("name")
    partial = PARTIALS / f"{name}.html"
    if not partial.is_file():
        sys.exit(f"build.py: saknar {partial.relative_to(ROOT)}")
    body = "".join(
        indent + line if line.strip() else line
        for line in partial.read_text(encoding="utf-8").splitlines(keepends=True)
    )
    return (
        f"{indent}<!-- include:{name} -->\n"
        f"{body.rstrip()}\n"
        f"{indent}<!-- /include:{name} -->\n"
    )


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for page in sorted(ROOT.rglob("*.html")):
        if PARTIALS in page.parents or ".git" in page.parts:
            continue
        old = page.read_text(encoding="utf-8")
        new, n = MARKER.subn(expand, old)
        if n == 0 or new == old:
            continue
        stale.append(page.relative_to(ROOT))
        if not check:
            page.write_text(new, encoding="utf-8")
    if check and stale:
        print("build.py: inaktuella sidor, kör python3 build.py:")
        print("\n".join(f"  {p}" for p in stale))
        sys.exit(1)
    for p in stale:
        print(f"uppdaterade {p}")


if __name__ == "__main__":
    main()
