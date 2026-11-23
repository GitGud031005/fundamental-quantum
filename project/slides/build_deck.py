"""Assemble slides/qsvt-slides.html from the skill's starter and slides/slides-body.html.

Run from the project folder:  python slides/build_deck.py
The starter is copied byte for byte (its motif sprite must stay identical); only the
<title> and the block between the SLIDES START / SLIDES END markers change. PNGs under
slides/assets/ are embedded as data URIs so the deck is one self-contained file.
"""
import base64
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
STARTER = REPO / ".claude" / "skills" / "educational-dark-design" / "assets" / "starter.html"
BODY = HERE / "slides-body.html"
OUT = HERE / "qsvt-slides.html"

START = "<!-- ================= SLIDES START ================= -->"
END = "<!-- ================= SLIDES END ================= -->"

html = STARTER.read_text(encoding="utf-8")
body = BODY.read_text(encoding="utf-8")


def embed(m):
    path = HERE / m.group(1)
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'src="data:image/png;base64,{data}"'


body = re.sub(r'src="(assets/[^"]+\.png)"', embed, body)

i, j = html.index(START), html.index(END)
html = html[: i + len(START)] + "\n" + body + "\n" + html[j:]
html = html.replace("<title>DECK TITLE</title>", "<title>From quantum foundations to QSVT</title>", 1)
assert '<html lang="vi">' in html
html = html.replace('<html lang="vi">', '<html lang="en">', 1)   # English deck: Lato body font

OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT.relative_to(REPO)} ({OUT.stat().st_size // 1024} KB, {body.count('<section class=')} slides)")
