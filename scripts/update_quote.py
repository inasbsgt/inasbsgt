"""Write assets/quote.svg with a programming quote that changes every day."""
import datetime
from pathlib import Path

QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
]
M = "ui-monospace, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"
S = "'Segoe UI', -apple-system, Helvetica, Arial, 'DejaVu Sans', sans-serif"
OUT = Path(__file__).resolve().parent.parent / "assets" / "quote.svg"


def wrap(text, width=62):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    lines.append(line)
    return lines


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(quote, author):
    lines = wrap(quote)
    h = 96 + 40 * len(lines) + 40
    tl = "".join(
        f'<text x="600" y="{92 + 40 * i}" text-anchor="middle" font-family="{S}" font-size="26" fill="#3E2723">{esc(l)}</text>'
        for i, l in enumerate(lines))
    ay = 92 + 40 * len(lines) + 18
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {h}" width="1200" height="{h}" role="img" aria-label="{esc(quote)} — {esc(author)}">
  <defs><linearGradient id="qg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E3D2BA"/><stop offset="0.6" stop-color="#D6C0A3"/><stop offset="1" stop-color="#C9AE8C"/></linearGradient>
  <style>.c {{ animation: bl .9s steps(1) infinite; }} @keyframes bl {{ 50% {{ opacity: 0; }} }}</style></defs>
  <rect width="1200" height="{h}" rx="16" fill="url(#qg)"/>
  <rect x="0.5" y="0.5" width="1199" height="{h-1}" rx="15.5" fill="none" stroke="#C4A484" stroke-opacity="0.8"/>
  <text x="600" y="44" text-anchor="middle" font-family="{M}" font-size="13" letter-spacing="3" fill="#8B6F5A">// THOUGHT OF THE DAY</text>
  <text x="60" y="110" font-family="Georgia, serif" font-size="90" fill="#7E5F49" fill-opacity="0.3">&#8220;</text>
  {tl}
  <text x="600" y="{ay}" text-anchor="middle" font-family="{M}" font-size="16" fill="#6F4E37">— {esc(author)}<tspan class="c" fill="#6F4E37"> _</tspan></text>
</svg>
'''


def main():
    day = datetime.date.today().toordinal()
    q, a = QUOTES[day % len(QUOTES)]
    OUT.write_text(render(q, a), encoding="utf-8")
    print(f"quote: {q} — {a}")


if __name__ == "__main__":
    main()
