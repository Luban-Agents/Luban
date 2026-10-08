"""Check local Markdown targets without a network or documentation server."""

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failures = []
    pages = list(ROOT.glob("*.md"))
    for directory in (
        "docs",
        "impl_docs",
        "catalogs",
        "configs",
        "rules",
        "benchmarks",
        "ci",
        ".github",
    ):
        pages.extend((ROOT / directory).rglob("*.md"))
    pages.sort()
    for page in pages:
        source = re.sub(r"```.*?```", "", page.read_text(), flags=re.S)
        targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", source)
        targets += re.findall(r'(?:href|src)="([^"]+)"', source)
        for value in targets:
            target = value.split("#", 1)[0].strip().strip("<>")
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (page.parent / unquote(target)).exists():
                failures.append(f"{page.relative_to(ROOT)}: {target}")
    for failure in failures:
        print(failure)
    print(f"Local Markdown targets: {len(pages)} pages, {len(failures)} failures")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
