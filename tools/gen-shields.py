# -*- coding: utf-8 -*-
"""Generate faction shield emblems (riveted metal shield + faction rune).

    python tools/gen-shields.py     -> src/assets/shields/<faction>.svg

Our own flat-vector take on the classic Warhammer faction shield: a steel
riveted frame, a glossy coloured field, and a bold rune, one per faction.
"""
import io
import os

OUT = "src/assets/shields"
INK = "#2b2f34"

# shield outline (viewBox 0 0 200 224, centre ~100,112)
SHIELD = ("M46 26 L154 26 C169 26 179 35 179 51 L177 118 "
          "C175 160 147 192 100 206 C53 192 25 160 23 118 "
          "L21 51 C21 35 31 26 46 26 Z")


def rune_khorne(gold):
    # blocky skull rune, close to the reference art
    o = []
    o.append('<path d="M64 74 C64 54 136 54 136 74 L136 82 L100 76 L64 82 Z" '
             'fill="%s"/>' % gold)                                             # domed brow
    o.append('<path d="M66 88 L96 88 L88 110 L66 110 Z" fill="%s"/>' % gold)   # left eye
    o.append('<path d="M134 88 L104 88 L112 110 L134 110 Z" fill="%s"/>' % gold)  # right eye
    o.append('<path d="M100 94 L93 110 L107 110 Z" fill="%s"/>' % gold)        # nose
    for i, x in enumerate((66, 82, 98, 114, 130)):
        h = 22 if i in (0, 4) else 15
        o.append('<rect x="%d" y="114" width="9" height="%d" rx="2" fill="%s"/>' % (x, h, gold))
    return o


def rune_kislev(gold):
    # bold bear head
    o = []
    o.append('<circle cx="74" cy="72" r="14" fill="%s"/>' % gold)   # ears
    o.append('<circle cx="126" cy="72" r="14" fill="%s"/>' % gold)
    o.append('<circle cx="100" cy="96" r="30" fill="%s"/>' % gold)  # head
    o.append('<ellipse cx="100" cy="110" rx="16" ry="13" fill="#2f6aa8"/>')  # muzzle (field colour)
    o.append('<ellipse cx="100" cy="102" rx="6.5" ry="5.5" fill="#22405f"/>')  # nose
    o.append('<circle cx="86" cy="90" r="4.5" fill="#22405f"/>')
    o.append('<circle cx="114" cy="90" r="4.5" fill="#22405f"/>')
    return o


def rune_cathay(gold, field):
    # coiled dragon around a pearl
    o = []
    o.append('<circle cx="100" cy="104" r="30" fill="none" stroke="%s" stroke-width="15"/>' % gold)
    o.append('<path d="M100 104 L78 66 L122 66 Z" fill="%s"/>' % field)     # open ring top
    o.append('<path d="M120 66 C142 52 156 66 145 82 C138 72 128 74 121 78 Z" fill="%s"/>' % gold)  # head
    o.append('<circle cx="141" cy="64" r="4" fill="%s"/>' % field)
    o.append('<path d="M138 54 L150 46 L145 62 Z" fill="%s"/>' % gold)      # horn
    o.append('<path d="M80 66 L66 54 L76 78 Z" fill="%s"/>' % gold)         # tail
    o.append('<circle cx="100" cy="106" r="13" fill="%s"/>' % gold)         # pearl
    o.append('<circle cx="100" cy="106" r="7" fill="%s"/>' % field)
    return o


def rune_dwarfs(gold, field):
    # anvil + crossed hammer
    o = []
    o.append('<g transform="rotate(-22 100 100)">')
    o.append('<rect x="94" y="60" width="13" height="52" rx="5" fill="%s"/>' % field)   # handle dark
    o.append('<rect x="78" y="50" width="44" height="20" rx="6" fill="%s"/>' % gold)    # head
    o.append('</g>')
    o.append('<path d="M64 118 L136 118 L136 130 L112 130 L118 150 L82 150 L88 130 L64 130 Z" fill="%s"/>' % gold)
    o.append('<path d="M132 108 C154 105 158 118 134 118 L108 118 L108 105 Z" fill="%s"/>' % gold)  # horn
    o.append('<rect x="70" y="104" width="60" height="11" rx="3" fill="%s"/>' % gold)   # top face
    return o


FACTIONS = {
    "khorne": dict(field="#b31f24", field2="#7d1417", rune=rune_khorne, args=("#f2c21e",)),
    "kislev": dict(field="#2f6aa8", field2="#1e4670", rune=rune_kislev, args=("#e9d49a",)),
    "cathay": dict(field="#2f9e78", field2="#1c6a50", rune=rune_cathay, args=("#e9c65a", "#2f9e78")),
    "dwarfs": dict(field="#a06a22", field2="#6f4715", rune=rune_dwarfs, args=("#f2c21e", "#6f4715")),
}

RIVETS = [(54, 35), (80, 30), (120, 30), (146, 35), (28, 58), (172, 58),
          (30, 92), (170, 92), (38, 126), (162, 126), (54, 160), (146, 160),
          (86, 186), (114, 186)]


def build(name, cfg):
    uid = "s_" + name
    parts = []
    parts.append('<defs>')
    parts.append('<linearGradient id="%s_m" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0" stop-color="#c6cfd6"/><stop offset="1" stop-color="#7c8894"/>'
                 '</linearGradient>' % uid)
    parts.append('<radialGradient id="%s_f" cx="50%%" cy="34%%" r="72%%">'
                 '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
                 '</radialGradient>' % (uid, cfg["field"], cfg["field2"]))
    parts.append('</defs>')
    # metal frame
    parts.append('<path d="%s" fill="url(#%s_m)" stroke="%s" stroke-width="6" '
                 'stroke-linejoin="round"/>' % (SHIELD, uid, INK))
    # bottom studs
    for x in (74, 88, 100, 112, 126):
        parts.append('<path d="M%d 196 L%d 208 L%d 196 Z" fill="#8a939c" stroke="%s" '
                     'stroke-width="3" stroke-linejoin="round"/>' % (x - 6, x, x + 6, INK))
    # field, inset via scale about centre
    parts.append('<g transform="translate(100 112) scale(0.84) translate(-100 -112)">')
    parts.append('<path d="%s" fill="url(#%s_f)" stroke="#2b2f34" stroke-width="4" '
                 'stroke-linejoin="round"/>' % (SHIELD, uid))
    parts.append('<path d="%s" fill="#ffffff" opacity="0.10"/>'
                 % "M46 26 L154 26 C169 26 179 35 179 51 L178 92 L22 92 L21 51 C21 35 31 26 46 26 Z")
    parts.append('</g>')
    # rivets
    for (x, y) in RIVETS:
        parts.append('<circle cx="%d" cy="%d" r="4.6" fill="#5f6a74" stroke="%s" '
                     'stroke-width="2.2"/>' % (x, y, INK))
        parts.append('<circle cx="%d" cy="%d" r="1.6" fill="#aeb7bf"/>' % (x - 1, y - 1))
    # rune
    parts += cfg["rune"](*cfg["args"])
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 224" width="200" '
            'height="224" role="img" aria-label="%s shield">%s</svg>\n'
            % (name, "".join(parts)))


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, cfg in FACTIONS.items():
        with io.open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(build(name, cfg))
    print("wrote %d shields -> %s" % (len(FACTIONS), OUT))


if __name__ == "__main__":
    main()
