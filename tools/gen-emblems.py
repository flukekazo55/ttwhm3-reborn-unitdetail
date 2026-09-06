# -*- coding: utf-8 -*-
"""Generate flat-vector heraldic faction banners (our own take, not game art).

    python tools/gen-emblems.py

Writes src/assets/emblems/<faction>.svg  (viewBox 0 0 120 150).
Each is a hanging banner: a wooden crossbar, a coloured gonfalon with a
swallow-tail hem, and the faction device on the cloth, so it reads on any card.
"""
import io
import os

OUT = "src/assets/emblems"
INK = "#2f2720"
WOOD = "#6b4a2c"


def p(d, fill, stroke=INK, w=5):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (d, fill, stroke, w)


def c(cx, cy, r, fill, stroke=INK, w=5):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        cx, cy, r, fill, stroke, w)


def e(cx, cy, rx, ry, fill, stroke=INK, w=5):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        cx, cy, rx, ry, fill, stroke, w)


def ln(x1, y1, x2, y2, stroke=INK, w=5):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round"/>' % (x1, y1, x2, y2, stroke, w))


def rc(x, y, w_, h, fill, rx=0, stroke=INK, sw=5):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"/>' % (x, y, w_, h, rx, fill, stroke, sw))


def banner(cloth, trim, device, band=True):
    """Crossbar + gonfalon with a swallow-tail hem, then the device on top."""
    o = []
    o.append(rc(16, 14, 88, 8, WOOD, rx=4))                 # crossbar
    o.append(c(16, 18, 5.5, trim))                          # finials
    o.append(c(104, 18, 5.5, trim))
    o.append(ln(40, 21, 40, 30, INK, 3))                    # cords
    o.append(ln(80, 21, 80, 30, INK, 3))
    o.append(p("M33 28 L87 28 L87 108 L74 122 L60 109 L46 122 L33 108 Z", cloth, w=5))
    if band:
        o.append(p("M35 30 L85 30 L85 40 L35 40 Z", trim, stroke="none"))
    o += device
    return o


def wrap(body, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 150" width="120" '
            'height="150" role="img" aria-label="%s"><g stroke-linejoin="round" '
            'stroke-linecap="round">%s</g></svg>\n' % (label, "".join(body)))


# --------------------------------------------------------------------- Khorne
def khorne():
    RED, BRASS, BONE = "#b8232b", "#c89a3c", "#e8ded0"
    dev = []
    dev.append(c(60, 66, 16, BONE, w=4))                    # cranium
    dev.append(e(53, 66, 4, 5.2, "#2b2521", stroke="none"))
    dev.append(e(67, 66, 4, 5.2, "#2b2521", stroke="none"))
    dev.append(p("M60 70 L56 78 L64 78 Z", "#2b2521", stroke="none"))
    dev.append(p("M50 78 L70 78 L68 90 L52 90 Z", BONE, w=4))  # jaw
    for x in (55, 60, 65):
        dev.append(ln(x, 80, x, 90, INK, 2.5))
    return banner(RED, BRASS, dev)


# --------------------------------------------------------------------- Kislev
def kislev():
    BLUE, GOLD, FUR = "#2d5c8c", "#e0b45c", "#cdd9e2"
    dev = []
    dev.append(c(50, 60, 7.5, FUR))                         # ears
    dev.append(c(70, 60, 7.5, FUR))
    dev.append(c(50, 60, 3.4, BLUE, stroke="none"))
    dev.append(c(70, 60, 3.4, BLUE, stroke="none"))
    dev.append(c(60, 70, 16, FUR))                          # face
    dev.append(e(60, 78, 9, 7, "#eef3f7"))                  # muzzle
    dev.append(e(60, 73, 4.2, 3.4, "#2b2521", stroke="none"))  # nose
    dev.append(c(53, 67, 2.6, "#2b2521", stroke="none"))
    dev.append(c(67, 67, 2.6, "#2b2521", stroke="none"))
    return banner(BLUE, GOLD, dev)


# --------------------------------------------------------------------- Cathay
def cathay():
    JADE, GOLD, PEARL = "#2f9e78", "#e6c15a", "#f3ede0"
    dev = []
    dev.append(c(60, 70, 17, "none", stroke=GOLD, w=8))     # dragon body ring
    dev.append(p("M60 70 L48 50 L72 50 Z", JADE, stroke="none"))  # open at top
    dev.append(p("M70 50 C82 42 90 50 84 58 C80 53 75 54 71 56 Z", GOLD, w=3.5))  # head
    dev.append(c(80, 49, 2.2, "#2b2521", stroke="none"))
    dev.append(p("M78 44 L85 39 L82 48 Z", GOLD, w=2.5))    # horn
    dev.append(p("M50 50 L42 44 L48 56 Z", GOLD, w=3))      # tail
    dev.append(c(60, 72, 8, PEARL, w=3.5))                  # pearl
    dev.append(c(57, 69, 2.2, "#ffffff", stroke="none"))
    return banner(JADE, GOLD, dev)


# ---------------------------------------------------------------------- Dwarfs
def dwarfs():
    BRONZE, DBRONZE, STEEL, GOLD = "#b8762b", "#8c5920", "#c2ccd4", "#e0b45c"
    dev = []
    # crossed hammer behind
    dev.append('<g transform="rotate(-22 60 70)">')
    dev.append(rc(56, 48, 8, 34, WOOD, rx=4, sw=3.5))       # handle
    dev.append(rc(46, 42, 28, 13, DBRONZE, rx=4, sw=3.5))   # head
    dev.append('</g>')
    # anvil
    dev.append(p("M44 78 L76 78 L76 84 L66 84 L69 94 L51 94 L54 84 L44 84 Z", STEEL, w=3.5))
    dev.append(p("M74 73 C86 71 88 78 77 78 L62 78 L62 71 Z", STEEL, w=3.5))  # horn
    dev.append(rc(47, 69, 26, 6, STEEL, rx=2, sw=3.5))      # top face
    return banner(BRONZE, GOLD, dev)


EMBLEMS = {"khorne": khorne, "kislev": kislev, "cathay": cathay, "dwarfs": dwarfs}


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, fn in EMBLEMS.items():
        with io.open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(wrap(fn(), name + " banner"))
    print("wrote %d banners -> %s" % (len(EMBLEMS), OUT))


if __name__ == "__main__":
    main()
