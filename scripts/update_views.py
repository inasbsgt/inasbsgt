"""Update the profile-views number inside assets/status-bar.svg.

The README contains an invisible komarev counter (style=pixel) that counts
every visit. This script reads the total from komarev, removes the hits added
by the script itself (one per run, stored in scripts/views_offset.txt) and
writes the number into the status bar from the template.
"""
import re
import sys
import urllib.request
from pathlib import Path

USERNAME = "inasbsgt"
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "assets" / "status-bar.template.svg"
OUTPUT = ROOT / "assets" / "status-bar.svg"
OFFSET_FILE = ROOT / "scripts" / "views_offset.txt"


def fetch_count() -> int:
    url = f"https://komarev.com/ghpvc/?username={USERNAME}&style=flat"
    req = urllib.request.Request(url, headers={"User-Agent": "profile-views-updater"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return parse_count(resp.read().decode("utf-8"))


def parse_count(svg: str) -> int:
    numbers = re.findall(r">\s*([\d][\d,\s]*)\s*<", svg)
    if not numbers:
        raise ValueError("Could not find the view count in the komarev badge")
    return int(re.sub(r"[^\d]", "", numbers[-1]))


def main() -> int:
    offset = int(OFFSET_FILE.read_text().strip() or 0) if OFFSET_FILE.exists() else 0
    raw = fetch_count()  # this request itself adds one hit
    offset += 1
    views = max(raw - offset, 0)
    svg = TEMPLATE.read_text(encoding="utf-8").replace("{{VIEWS}}", f"{views:,}".replace(",", " "))
    OUTPUT.write_text(svg, encoding="utf-8")
    OFFSET_FILE.write_text(f"{offset}\n")
    print(f"komarev={raw} offset={offset} views={views}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
