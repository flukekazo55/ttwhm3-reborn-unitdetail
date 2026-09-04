# -*- coding: utf-8 -*-
"""Generate flat-vector chibi SVGs for the faction guide.

Every figure is assembled from the same parts (head / beard / helmet / torso /
arms / weapon / shield / mount ...) so a new unit only needs one row in SPECS.

    python tools/gen-chibi.py

Writes:
    src/assets/units/<faction>/chibi/<unit-id>.svg
    src/assets/lords/<faction>/chibi/<lord-id>-lord.svg
"""
import io
import math
import os
import sys

OUT_ROOT = "src/assets"
VIEWBOX = "0 0 200 260"
INK = "#3a2f26"

# ---------------------------------------------------------------- palettes ---
C = {
    "skin": "#f2c9a0",
    "skin_dark": "#dba97e",
    "steel": "#b9c3cc",
    "steel_dark": "#7f8b96",
    "iron": "#6f7a85",
    "wood": "#a97844",
    "wood_dark": "#7d5730",
    "gold": "#e0b45c",
}
C["brass"] = "#c89a3c"
C["jade"] = "#2f9e78"
C["jade_dark"] = "#22795c"
C["jade_light"] = "#57bd97"
C["cathay_red"] = "#c0392b"
C["straw"] = "#d9b063"
C["cloth"] = "#cbb193"
C["terracotta"] = "#b5643c"
C["terracotta_dark"] = "#8e492a"
C["bronze"] = "#b8762b"
C["bronze_dark"] = "#8c5920"
C["leather"] = "#8b5e3c"
C["beard_orange"] = "#d1622a"
C["beard_white"] = "#ece7dd"
C["beard_grey"] = "#c3bcb0"
C["beard_brown"] = "#8a5a34"
C["khorne_red"] = "#b8232b"
C["khorne_dark"] = "#7d161c"
C["dark"] = "#4a4038"
C["flame"] = "#f08a2c"
C["glow"] = "#7fe3c4"
C["sail"] = "#e4d3ae"
C["cloud"] = "#eef3f6"


def el(tag, **attrs):
    body = attrs.pop("_body", None)
    parts = []
    for k, v in attrs.items():
        if v is None:
            continue
        parts.append('%s="%s"' % (k.replace("_", "-"), v))
    open_tag = "<%s %s" % (tag, " ".join(parts))
    if body is None:
        return open_tag + "/>"
    return open_tag + ">" + body + "</%s>" % tag


def path(d, fill, stroke=INK, w=4):
    return el("path", d=d, fill=fill, stroke=stroke, stroke_width=w)


def circ(cx, cy, r, fill, stroke=INK, w=4):
    return el("circle", cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=w)


def ell(cx, cy, rx, ry, fill, stroke=INK, w=4):
    return el("ellipse", cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=w)


def rect(x, y, w_, h, fill, rx=0, stroke=INK, w=4):
    return el("rect", x=x, y=y, width=w_, height=h, rx=rx, fill=fill,
              stroke=stroke, stroke_width=w)


def line(x1, y1, x2, y2, stroke=INK, w=4):
    return el("line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke,
              stroke_width=w, stroke_linecap="round")


def group(body, transform=None, opacity=None):
    return el("g", transform=transform, opacity=opacity, _body="".join(body))


# ------------------------------------------------------------------ helmets --
def helmet(kind, cfg):
    hat = cfg.get("hat", C["jade"])
    trim = cfg.get("trim", C["gold"])
    out = []
    if kind in ("conical", "straw", "conical-iron"):
        out.append(path("M100 16 L154 76 L46 76 Z", hat))
        out.append(ell(100, 76, 60, 11, hat))
        if kind == "conical-iron":
            out.append(circ(100, 18, 7, trim))
        else:
            out.append(line(100, 24, 100, 70, INK, 3))
    elif kind == "dome":
        out.append(path("M56 80 A44 44 0 0 1 144 80 Z", hat))
        out.append(rect(52, 74, 96, 13, hat, rx=6))
    elif kind == "dwarf-helm":
        out.append(path("M58 80 A42 42 0 0 1 142 80 Z", hat))
        out.append(rect(54, 74, 92, 14, trim, rx=7))
        out.append(rect(94, 84, 12, 26, hat, rx=5))  # nose guard
    elif kind == "dwarf-helm-winged":
        out.append(path("M46 66 C22 62 12 84 22 100 C34 92 44 88 56 88 Z", trim))
        out.append(path("M154 66 C178 62 188 84 178 100 C166 92 156 88 144 88 Z", trim))
        out.append(path("M58 80 A42 42 0 0 1 142 80 Z", hat))
        out.append(rect(54, 74, 92, 14, trim, rx=7))
        out.append(rect(94, 84, 12, 26, hat, rx=5))
    elif kind == "full-helm":
        out.append(path("M56 92 A44 46 0 0 1 144 92 L144 104 L56 104 Z", hat))
        out.append(rect(54, 98, 92, 22, hat, rx=8))
        out.append(rect(66, 104, 68, 9, "#2b2521", rx=4, stroke="none"))  # visor slit
        out.append(rect(94, 92, 12, 30, cfg.get("trim2", trim), rx=5))
    elif kind == "dragon-helm":
        out.append(path("M52 62 C30 44 22 60 30 78 C40 70 48 68 58 70 Z", trim))
        out.append(path("M148 62 C170 44 178 60 170 78 C160 70 152 68 142 70 Z", trim))
        out.append(path("M58 80 A42 42 0 0 1 142 80 Z", hat))
        out.append(rect(54, 74, 92, 13, trim, rx=6))
        out.append(path("M100 22 L110 46 L90 46 Z", trim))
    elif kind == "crown":
        out.append(path("M60 78 A40 40 0 0 1 140 78 Z", hat))
        out.append(path("M56 60 L68 34 L80 56 L100 26 L120 56 L132 34 L144 60 Z", trim))
        out.append(rect(54, 70, 92, 14, trim, rx=7))
    elif kind == "mohawk":
        out.append(path("M100 8 L112 40 L88 40 Z", cfg.get("crest", C["beard_orange"])))
        out.append(path("M74 30 L84 46 L64 50 Z", cfg.get("crest", C["beard_orange"])))
        out.append(path("M126 30 L116 46 L136 50 Z", cfg.get("crest", C["beard_orange"])))
        out.append(path("M64 52 C74 38 126 38 136 52 C120 44 80 44 64 52 Z",
                        cfg.get("crest", C["beard_orange"])))
    elif kind == "goggles":
        out.append(path("M58 78 A42 42 0 0 1 142 78 Z", cfg.get("hat", C["leather"])))
        out.append(rect(52, 72, 96, 13, C["leather"], rx=6))
        out.append(circ(78, 92, 15, C["cloud"]))
        out.append(circ(122, 92, 15, C["cloud"]))
        out.append(line(93, 92, 107, 92, INK, 5))
    elif kind == "mining-helm":
        out.append(path("M58 80 A42 42 0 0 1 142 80 Z", hat))
        out.append(rect(54, 74, 92, 13, C["leather"], rx=6))
        out.append(circ(100, 56, 12, C["gold"]))
    elif kind == "hood":
        out.append(path("M54 96 C50 40 150 40 146 96 C130 76 70 76 54 96 Z", hat))
        out.append(path("M54 96 C56 126 66 140 76 146 C62 132 58 114 58 96 Z", cfg.get("hat2", hat)))
    elif kind == "winged-helm":
        out.append(path("M48 70 C18 52 6 78 18 100 C34 86 42 80 58 80 Z", trim))
        out.append(path("M152 70 C182 52 194 78 182 100 C166 86 158 80 142 80 Z", trim))
        out.append(path("M58 84 A42 42 0 0 1 142 84 Z", hat))
        out.append(rect(54, 78, 92, 13, trim, rx=6))
        out.append(rect(94, 88, 12, 24, hat, rx=5))
    return out


# ------------------------------------------------------------------- beards --
BEARDS = {
    "short": "M64 96 C66 138 134 138 136 96 C124 112 76 112 64 96 Z",
    "long": "M62 94 C62 170 138 170 138 94 C124 114 76 114 62 94 Z",
    "forked": ("M62 94 C62 158 86 186 100 156 C114 186 138 158 138 94 "
               "C124 114 76 114 62 94 Z"),
}


# ------------------------------------------------------------------ weapons --
def weapon(kind, cfg):
    """Weapon drawn around a grip point at the origin, blade pointing up."""
    steel = cfg.get("steel", C["steel"])
    trim = cfg.get("trim", C["gold"])
    wood = C["wood"]
    o = []
    if kind == "sword":
        o += [rect(-6, -94, 12, 80, steel, rx=5),
              rect(-18, -20, 36, 9, trim, rx=4),
              rect(-5, -18, 10, 22, C["leather"], rx=4),
              circ(0, 8, 6, trim)]
    elif kind == "axe":
        o += [rect(-5, -100, 10, 116, wood, rx=4),
              path("M5 -96 C40 -88 40 -46 5 -38 Z", steel),
              path("M-5 -90 C-22 -84 -22 -58 -5 -52 Z", steel)]
    elif kind == "greataxe":
        o += [rect(-5, -116, 10, 132, wood, rx=4),
              path("M5 -112 C46 -102 46 -50 5 -40 Z", steel),
              path("M-5 -112 C-46 -102 -46 -50 -5 -40 Z", steel),
              circ(0, -76, 8, trim)]
    elif kind == "hammer":
        o += [rect(-5, -98, 10, 114, wood, rx=4),
              rect(-26, -104, 52, 30, steel, rx=6),
              rect(-26, -96, 52, 8, trim, rx=3, stroke="none")]
    elif kind == "halberd":
        o += [rect(-5, -132, 10, 148, wood, rx=4),
              path("M5 -128 C38 -118 38 -78 5 -70 Z", steel),
              path("M-5 -132 L-5 -150 L6 -150 L6 -128 Z", steel),
              path("M-5 -112 C-24 -106 -24 -86 -5 -80 Z", steel)]
    elif kind == "spear":
        o += [rect(-5, -136, 10, 152, wood, rx=4),
              path("M0 -168 C14 -148 12 -134 0 -128 C-12 -134 -14 -148 0 -168 Z", steel),
              rect(-8, -132, 16, 8, trim, rx=3)]
    elif kind == "lance":
        o += [path("M-8 20 L8 20 L4 -150 L-2 -158 Z", cfg.get("lance", steel)),
              rect(-14, -6, 28, 16, trim, rx=6)]
    elif kind == "crossbow":
        o += [rect(-14, -8, 62, 12, wood, rx=5),
              path("M34 -40 C58 -22 58 22 34 40", "none", INK, 7),
              line(36, -38, 36, 38, "#6b5a48", 3),
              rect(-6, -4, 14, 22, wood, rx=4)]
    elif kind == "bow":
        o += [path("M2 -46 C30 -28 30 28 2 46", "none", C["wood_dark"], 7),
              line(6, -43, 6, 43, "#6b5a48", 3),
              rect(-4, -8, 8, 16, C["leather"], rx=3)]
    elif kind == "gun":
        o += [rect(-16, -6, 74, 11, C["iron"], rx=4),
              rect(-24, -2, 22, 20, wood, rx=5),
              rect(40, -9, 12, 17, C["iron"], rx=3),
              rect(4, 4, 26, 8, wood, rx=3)]
    elif kind == "flamer":
        o += [rect(-16, -10, 62, 20, C["iron"], rx=8),
              rect(-26, -4, 22, 22, wood, rx=5),
              path("M46 -12 C74 -18 84 0 62 12 C74 2 62 -6 46 -2 Z", C["flame"]),
              circ(6, 0, 7, trim)]
    elif kind == "torpedo-gun":
        o += [rect(-16, -13, 70, 26, C["iron"], rx=10),
              rect(-28, -4, 24, 22, wood, rx=5),
              path("M54 -13 L70 0 L54 13 Z", steel),
              rect(-6, -20, 12, 12, C["iron"], rx=3)]
    elif kind == "staff":
        o += [rect(-5, -128, 10, 148, C["wood_dark"], rx=4),
              circ(0, -140, 17, cfg.get("orb", C["glow"])),
              circ(-5, -145, 5, "#ffffff", stroke="none")]
    elif kind == "pickaxe":
        o += [rect(-5, -96, 10, 112, wood, rx=4),
              path("M-42 -84 C-14 -100 14 -100 42 -84 C14 -90 -14 -90 -42 -84 Z", steel)]
    return o


def shield(cfg):
    face = cfg.get("shield_color", cfg.get("trim", C["gold"]))
    return [ell(0, 0, 27, 34, face),
            circ(0, 0, 9, cfg.get("shield_boss", C["steel"]))]


# --------------------------------------------------------------------- face --
def face(cfg):
    skin = cfg.get("skin", C["skin"])
    o = [circ(100, 82, 44, skin)]
    if cfg.get("helmet") not in ("full-helm",):
        eye = cfg.get("eye", "#332b25")
        for x in (82, 118):
            o.append(ell(x, 88, 6, 7.5, eye, stroke="none"))
            o.append(circ(x - 2.5, 85, 2.4, "#ffffff", stroke="none"))
        o.append(line(72, 72, 90, 78, INK, 5))
        o.append(line(128, 72, 110, 78, INK, 5))
        blush = cfg.get("blush", "#e79a86")
        o.append(el("ellipse", cx=68, cy=100, rx=9, ry=6, fill=blush, opacity="0.5"))
        o.append(el("ellipse", cx=132, cy=100, rx=9, ry=6, fill=blush, opacity="0.5"))
    return o


# ------------------------------------------------------------------ humanoid --
def humanoid(cfg):
    armor = cfg.get("armor", C["jade"])
    armor2 = cfg.get("armor2", armor)
    trim = cfg.get("trim", C["gold"])
    boots = cfg.get("boots", C["leather"])
    back, front = [], []

    if cfg.get("cloak"):
        back.append(path("M64 118 C28 152 32 202 42 218 L158 218 C168 202 172 152 136 118 Z",
                         cfg["cloak"]))
    if cfg.get("wings"):
        wc = cfg["wings"]
        back.append(path("M70 122 C22 88 0 132 16 176 C36 154 54 148 74 152 Z", wc))
        back.append(path("M130 122 C178 88 200 132 184 176 C164 154 146 148 126 152 Z", wc))

    body = []
    body.append(rect(76, 172, 20, 42, boots, rx=10))
    body.append(rect(104, 172, 20, 42, boots, rx=10))
    body.append(rect(66, 116, 68, 68, armor, rx=22))
    body.append(rect(66, 158, 68, 14, trim, rx=6))
    body.append(rect(46, 122, 20, 56, armor2, rx=10))
    body.append(rect(134, 122, 20, 56, armor2, rx=10))
    if cfg.get("chest_line", True):
        body.append(line(100, 124, 100, 154, INK, 3))

    head = face(cfg)
    if cfg.get("beard"):
        head.append(path(BEARDS[cfg["beard"]], cfg.get("beard_color", C["beard_brown"])))
    head += helmet(cfg.get("helmet", "none"), cfg)

    hands = [circ(56, 178, 10, cfg.get("skin", C["skin"])),
             circ(144, 178, 10, cfg.get("skin", C["skin"]))]

    w = cfg.get("weapon")
    if w:
        ang = cfg.get("weapon_angle", 12)
        front.append(group(weapon(w, cfg), "translate(144,178) rotate(%s)" % ang))
    if cfg.get("shield"):
        front.append(group(shield(cfg), "translate(50,152)"))
    w2 = cfg.get("weapon_left")
    if w2:
        front.append(group(weapon(w2, cfg), "translate(56,178) rotate(%s)" % -cfg.get("weapon_angle", 12)))

    return back + body + head + hands + front


# -------------------------------------------------------------------- mount --
def mount(cfg):
    body = cfg.get("mount_color", "#a97e52")
    mane = cfg.get("mane_color", "#6f5334")
    o = []
    for x in (48, 72, 124, 148):
        o.append(rect(x, 178, 18, 52, body, rx=9))
    o.append(rect(36, 138, 132, 58, body, rx=28))
    o.append(path("M160 146 C186 138 194 112 178 100 C166 92 150 104 148 124 Z", body))
    o.append(path("M176 96 L184 78 L190 98 Z", body))
    o.append(path("M40 140 C20 130 14 158 30 172 C34 158 36 148 44 144 Z", mane))
    o.append(ell(180, 118, 4, 5, "#332b25", stroke="none"))
    return o


def cavalry(cfg):
    o = mount(cfg)
    rider = humanoid(cfg)
    o.append(group(rider, "translate(24,-8) scale(0.72)"))
    return o


# ------------------------------------------------------------------ monster --
def monster(cfg):
    armor = cfg.get("armor", C["terracotta"])
    armor2 = cfg.get("armor2", C["terracotta_dark"])
    o = []
    o.append(rect(58, 176, 32, 52, armor2, rx=12))
    o.append(rect(110, 176, 32, 52, armor2, rx=12))
    o.append(rect(50, 104, 100, 82, armor, rx=24))
    o.append(rect(24, 108, 26, 74, armor2, rx=12))
    o.append(rect(150, 108, 26, 74, armor2, rx=12))
    o.append(rect(50, 150, 100, 14, cfg.get("trim", C["gold"]), rx=6))
    o.append(rect(62, 34, 76, 72, armor, rx=22))
    for x in (82, 118):
        o.append(ell(x, 68, 7, 9, cfg.get("eye_glow", C["glow"]), stroke="none"))
    o.append(rect(74, 90, 52, 9, armor2, rx=4))
    o.append(path("M70 34 L82 10 L100 26 L118 10 L130 34 Z", cfg.get("trim", C["gold"])))
    o.append(rect(66, 30, 68, 12, cfg.get("trim", C["gold"]), rx=5))
    return o


# ---------------------------------------------------------------- artillery --
def artillery(cfg):
    wood = cfg.get("wood", C["wood"])
    iron = cfg.get("iron", C["iron"])
    kind = cfg.get("barrel", "cannon")
    o = []
    o.append(path("M44 176 L156 176 L142 208 L58 208 Z", wood))
    if kind == "cannon":
        o.append(group([rect(-16, -82, 32, 92, iron, rx=10),
                        rect(-20, -84, 40, 14, C["brass"], rx=6)],
                       "translate(104,168) rotate(24)"))
    elif kind == "organ":
        for i, dx in enumerate((-24, -12, 0, 12, 24)):
            o.append(group([rect(-7, -76, 14, 84, iron, rx=6)],
                           "translate(%s,168) rotate(20)" % (104 + dx)))
        o.append(group([rect(-34, -80, 68, 14, C["brass"], rx=6)],
                       "translate(104,168) rotate(20)"))
    elif kind == "rocket":
        for dx, ang in ((-22, 34), (0, 24), (22, 14)):
            o.append(group([rect(-11, -78, 22, 86, cfg.get("tube", C["cathay_red"]), rx=9),
                            path("M-11 -78 L0 -96 L11 -78 Z", C["gold"])],
                           "translate(%s,168) rotate(%s)" % (104 + dx, ang)))
    elif kind == "catapult":
        o.append(group([rect(-6, -104, 12, 118, wood, rx=5),
                        path("M-20 -112 C-20 -134 20 -134 20 -112 Z", iron)],
                       "translate(104,166) rotate(-28)"))
        o.append(line(60, 176, 130, 120, C["wood_dark"], 5))
    elif kind == "flame":
        o.append(group([rect(-22, -60, 44, 70, iron, rx=16),
                        rect(-26, -64, 52, 14, C["brass"], rx=6),
                        path("M-26 -70 C-4 -92 22 -78 4 -62 C14 -74 0 -78 -26 -70 Z", C["flame"])],
                       "translate(104,168) rotate(22)"))
    for cx in (60, 146):
        o.append(circ(cx, 196, 28, wood))
        o.append(circ(cx, 196, 9, C["wood_dark"]))
        for a in (0, 45, 90, 135):
            dx = 20 * math.cos(math.radians(a))
            dy = 20 * math.sin(math.radians(a))
            o.append(line(cx - dx, 196 - dy, cx + dx, 196 + dy, C["wood_dark"], 3))
    crew = cfg.get("crew", {})
    if crew:
        body = [rect(-26, 26, 52, 44, crew.get("coat", C["leather"]), rx=16),
                circ(0, 0, 24, crew.get("skin", C["skin"]))]
        for x in (-10, 10):
            body.append(ell(x, 5, 3.6, 4.6, "#332b25", stroke="none"))
        if crew.get("beard"):
            body.append(path("M-21 11 C-19 42 19 42 21 11 C12 22 -12 22 -21 11 Z",
                             crew.get("beard_color", C["beard_brown"])))
        body += [group(helmet(crew.get("helmet", "dwarf-helm"), crew),
                       "scale(0.55) translate(-100,-100)")]
        o.append(group(body, "translate(154,144) scale(0.7)"))
    return o


# ------------------------------------------------------------------ aircraft --
def aircraft(cfg):
    armor = cfg.get("armor", C["bronze"])
    iron = cfg.get("iron", C["iron"])
    o = []
    o.append(rect(96, 46, 10, 34, iron, rx=4))
    o.append(rect(14, 34, 172, 10, iron, rx=5))
    o.append(rect(104, 128, 76, 14, armor, rx=6))
    o.append(path("M168 108 L188 128 L168 148 Z", C["steel"]))
    o.append(circ(96, 132, 46, armor))
    o.append(path("M54 138 A42 42 0 0 1 138 138 Z", C["cloud"]))
    o.append(circ(96, 128, 24, cfg.get("skin", C["skin"])))
    for x in (88, 104):
        o.append(ell(x, 130, 3.8, 4.8, "#332b25", stroke="none"))
    o.append(path("M78 140 C80 160 112 160 114 140 C104 148 88 148 78 140 Z",
                  cfg.get("beard_color", C["beard_brown"])))
    o.append(group(helmet("dwarf-helm", {"hat": C["steel"], "trim": C["gold"]}),
                   "translate(96,128) scale(0.56) translate(-100,-100)"))
    o.append(line(66, 176, 126, 176, C["steel"], 7))
    o.append(line(78, 168, 78, 180, C["steel"], 5))
    o.append(line(114, 168, 114, 180, C["steel"], 5))
    if cfg.get("bombs"):
        for x in (72, 96, 120):
            o.append(ell(x, 192, 11, 15, C["iron"]))
    return o


def airship(cfg):
    sail = cfg.get("sail", C["sail"])
    hull = cfg.get("hull", C["wood"])
    o = []
    o.append(ell(100, 68, 64, 44, sail))
    for x in (74, 100, 126):
        o.append(line(x, 30, x, 106, C["wood_dark"], 3))
    o.append(line(56, 100, 62, 150, C["wood_dark"], 4))
    o.append(line(144, 100, 138, 150, C["wood_dark"], 4))
    if cfg.get("lantern"):
        o.append(rect(84, 108, 32, 10, C["cathay_red"], rx=4))
        o.append(path("M78 150 C78 176 122 176 122 150 Z", hull))
        o.append(line(88, 176, 88, 200, C["cathay_red"], 3))
        o.append(line(112, 176, 112, 200, C["cathay_red"], 3))
    else:
        o.append(path("M44 148 L156 148 L136 200 C100 216 76 210 64 200 Z", hull))
        o.append(rect(44, 142, 112, 14, C["cathay_red"], rx=6))
        o.append(group([rect(-13, -54, 26, 62, C["iron"], rx=8)],
                       "translate(150,176) rotate(64)"))
        o.append(circ(84, 172, 16, cfg.get("skin", C["skin"])))
        for x in (78, 90):
            o.append(ell(x, 174, 2.8, 3.6, "#332b25", stroke="none"))
        o.append(path("M84 152 L104 168 L64 168 Z", C["straw"]))
    return o


TEMPLATES = {
    "humanoid": humanoid,
    "cavalry": cavalry,
    "monster": monster,
    "artillery": artillery,
    "aircraft": aircraft,
    "airship": airship,
}


def render(cfg):
    scale = cfg.get("scale", 1.0)
    body = TEMPLATES[cfg.get("template", "humanoid")](cfg)
    inner = group(body, "translate(%s,%s) scale(%s)" % (
        100 - 100 * scale, 260 - 260 * scale, scale)) if scale != 1.0 else "".join(body)
    shadow = el("ellipse", cx=100, cy=240, rx=54, ry=11, fill="#3a2f26", opacity="0.16")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" width="200" height="260" '
        'role="img" aria-label="%s">'
        '<g stroke-linejoin="round" stroke-linecap="round">%s%s</g></svg>'
    ) % (VIEWBOX, cfg.get("label", ""), shadow, inner)
    return svg


# ===================================================================== specs ==
CATHAY = {"armor": C["jade"], "armor2": C["jade_dark"], "trim": C["gold"],
          "hat": C["jade"], "boots": C["dark"]}
CATHAY_ELITE = dict(CATHAY, armor=C["gold"], armor2="#c39c46", trim=C["cathay_red"],
                    hat=C["gold"])
CATHAY_PEASANT = dict(CATHAY, armor=C["cloth"], armor2="#b39c80", trim=C["straw"],
                      hat=C["straw"])
DWARF = {"armor": C["bronze"], "armor2": C["bronze_dark"], "trim": C["gold"],
         "hat": C["steel"], "boots": C["leather"], "beard": "short",
         "beard_color": C["beard_brown"], "skin": "#eab892"}
DWARF_ELITE = dict(DWARF, armor=C["steel"], armor2=C["steel_dark"], hat=C["steel"],
                   trim=C["gold"])

SPECS = [
    # ---------------------------------------------------------------- Cathay
    ("units/cathay", "jade-warriors",
     dict(CATHAY, helmet="conical", weapon="sword", shield=True, label="Jade Warriors")),
    ("units/cathay", "jade-warriors-halberds",
     dict(CATHAY, helmet="conical", weapon="halberd", weapon_angle=8,
          label="Jade Warriors (Halberds)")),
    ("units/cathay", "jade-warrior-crossbowmen",
     dict(CATHAY, helmet="conical", weapon="crossbow", weapon_angle=-70,
          label="Jade Warrior Crossbowmen")),
    ("units/cathay", "peasant-longspearmen",
     dict(CATHAY_PEASANT, helmet="straw", weapon="spear", weapon_angle=6,
          label="Peasant Long Spearmen")),
    ("units/cathay", "peasant-archers",
     dict(CATHAY_PEASANT, helmet="straw", weapon="bow", weapon_angle=-18,
          label="Peasant Archers")),
    ("units/cathay", "iron-hail-gunners",
     dict(CATHAY, armor=C["iron"], armor2="#5c666f", hat=C["iron"], helmet="conical-iron",
          weapon="gun", weapon_angle=-64, label="Iron Hail Gunners")),
    ("units/cathay", "jade-lancers",
     dict(CATHAY, template="cavalry", helmet="conical", weapon="lance", weapon_angle=48,
          mount_color="#c8a06a", mane_color="#8a6a42", label="Jade Lancers")),
    ("units/cathay", "longma-riders",
     dict(CATHAY, template="cavalry", helmet="dragon-helm", weapon="lance",
          weapon_angle=48, mount_color=C["jade_light"], mane_color=C["jade_dark"],
          wings=C["cloud"], label="Longma Riders")),
    ("units/cathay", "celestial-dragon-guard",
     dict(CATHAY_ELITE, helmet="dragon-helm", weapon="sword", shield=True, scale=1.04,
          label="Celestial Dragon Guard")),
    ("units/cathay", "celestial-dragon-guard-halberds",
     dict(CATHAY_ELITE, helmet="dragon-helm", weapon="halberd", weapon_angle=8, scale=1.04,
          label="Celestial Dragon Guard (Halberds)")),
    ("units/cathay", "terracotta-sentinel",
     dict(template="monster", armor=C["terracotta"], armor2=C["terracotta_dark"],
          trim=C["gold"], eye_glow=C["glow"], label="Terracotta Sentinel")),
    ("units/cathay", "grand-cannon",
     dict(template="artillery", barrel="cannon",
          crew=dict(helmet="conical", hat=C["jade"], trim=C["gold"]), label="Grand Cannon")),
    ("units/cathay", "fire-rain-rocket",
     dict(template="artillery", barrel="rocket", tube=C["cathay_red"],
          crew=dict(helmet="conical", hat=C["jade"], trim=C["gold"]),
          label="Fire Rain Rocket")),
    ("units/cathay", "sky-junk", dict(template="airship", label="Sky-Junk")),
    ("units/cathay", "sky-lantern",
     dict(template="airship", lantern=True, sail="#f0d9a6", hull=C["cathay_red"],
          label="Sky Lantern")),
    ("lords/cathay", "miao-ying-lord",
     dict(CATHAY, helmet="crown", weapon="staff", orb=C["cloud"], cloak=C["jade_light"],
          armor="#8fd7bd", armor2=C["jade_light"], scale=1.06, label="Miao Ying")),
    ("lords/cathay", "zhao-ming-lord",
     dict(CATHAY, helmet="dragon-helm", weapon="halberd", weapon_angle=8,
          armor=C["iron"], armor2="#5c666f", hat=C["brass"], trim=C["brass"],
          cloak=C["cathay_red"], scale=1.06, label="Zhao Ming")),
    ("lords/cathay", "yuan-bo-lord",
     dict(CATHAY, helmet="crown", weapon="staff", orb=C["jade_light"],
          cloak=C["gold"], armor=C["jade_dark"], armor2="#1a5f47", scale=1.06,
          label="Yuan Bo")),
    # ----------------------------------------------------------------- Dwarfs
    ("units/dwarfs", "dwarf-warriors",
     dict(DWARF, helmet="dwarf-helm", weapon="axe", shield=True, label="Dwarf Warriors")),
    ("units/dwarfs", "dwarf-warriors-great-weapons",
     dict(DWARF, helmet="dwarf-helm", weapon="greataxe", weapon_angle=8,
          label="Dwarf Warriors (Great Weapons)")),
    ("units/dwarfs", "longbeards",
     dict(DWARF, helmet="dwarf-helm-winged", weapon="sword", shield=True, beard="long",
          beard_color=C["beard_grey"], armor=C["gold"], armor2="#c39c46",
          label="Longbeards")),
    ("units/dwarfs", "longbeards-great-weapons",
     dict(DWARF, helmet="dwarf-helm-winged", weapon="greataxe", weapon_angle=8,
          beard="long", beard_color=C["beard_grey"], armor=C["gold"], armor2="#c39c46",
          label="Longbeards (Great Weapons)")),
    ("units/dwarfs", "quarrellers",
     dict(DWARF, helmet="dwarf-helm", weapon="crossbow", weapon_angle=-70,
          label="Quarrellers")),
    ("units/dwarfs", "thunderers",
     dict(DWARF, helmet="dwarf-helm", weapon="gun", weapon_angle=-64,
          armor=C["dark"], armor2="#3a332c", label="Thunderers")),
    ("units/dwarfs", "irondrakes",
     dict(DWARF_ELITE, helmet="full-helm", weapon="flamer", weapon_angle=-60,
          trim2=C["gold"], label="Irondrakes")),
    ("units/dwarfs", "irondrakes-trollhammer-torpedo",
     dict(DWARF_ELITE, helmet="full-helm", weapon="torpedo-gun", weapon_angle=-58,
          trim2=C["brass"], label="Irondrakes (Trollhammer Torpedo)")),
    ("units/dwarfs", "ironbreakers",
     dict(DWARF_ELITE, helmet="full-helm", weapon="axe", shield=True, scale=1.04,
          shield_color=C["gold"], label="Ironbreakers")),
    ("units/dwarfs", "hammerers",
     dict(DWARF, helmet="dwarf-helm-winged", weapon="hammer", weapon_angle=8,
          armor=C["gold"], armor2="#c39c46", beard="long", beard_color=C["beard_brown"],
          scale=1.04, label="Hammerers")),
    ("units/dwarfs", "slayers",
     dict(DWARF, helmet="mohawk", weapon="axe", weapon_left="axe", armor=C["skin"],
          armor2=C["skin_dark"], trim=C["leather"], beard="forked",
          beard_color=C["beard_orange"], crest=C["beard_orange"], chest_line=False,
          label="Slayers")),
    ("units/dwarfs", "giant-slayers",
     dict(DWARF, helmet="mohawk", weapon="greataxe", weapon_angle=8, armor=C["skin"],
          armor2=C["skin_dark"], trim=C["leather"], beard="forked",
          beard_color="#e0752f", crest="#e0752f", chest_line=False, scale=1.05,
          label="Giant Slayers")),
    ("units/dwarfs", "miners-blasting-charges",
     dict(DWARF, helmet="mining-helm", hat=C["leather"], weapon="pickaxe",
          weapon_angle=10, armor=C["leather"], armor2="#6f4a2f",
          label="Miners (Blasting Charges)")),
    ("units/dwarfs", "rangers-great-weapons",
     dict(DWARF, helmet="hood", hat="#5f7048", hat2="#4a5838", weapon="greataxe",
          weapon_angle=8, armor="#6f7a52", armor2="#5a6442", cloak="#5f7048",
          label="Rangers (Great Weapons)")),
    ("units/dwarfs", "grudge-thrower",
     dict(template="artillery", barrel="catapult",
          crew=dict(helmet="dwarf-helm", hat=C["steel"], trim=C["gold"], beard=True),
          label="Grudge Thrower")),
    ("units/dwarfs", "cannon",
     dict(template="artillery", barrel="cannon",
          crew=dict(helmet="dwarf-helm", hat=C["steel"], trim=C["gold"], beard=True),
          label="Cannon")),
    ("units/dwarfs", "organ-gun",
     dict(template="artillery", barrel="organ",
          crew=dict(helmet="dwarf-helm", hat=C["steel"], trim=C["gold"], beard=True),
          label="Organ Gun")),
    ("units/dwarfs", "flame-cannon",
     dict(template="artillery", barrel="flame",
          crew=dict(helmet="dwarf-helm", hat=C["steel"], trim=C["gold"], beard=True),
          label="Flame Cannon")),
    ("units/dwarfs", "gyrocopter", dict(template="aircraft", label="Gyrocopter")),
    ("units/dwarfs", "gyrobomber",
     dict(template="aircraft", bombs=True, armor=C["bronze_dark"], label="Gyrobomber")),
    ("lords/dwarfs", "thorgrim-lord",
     dict(DWARF, helmet="crown", hat=C["gold"], weapon="hammer", weapon_angle=8,
          armor=C["gold"], armor2="#c39c46", trim=C["cathay_red"], beard="forked",
          beard_color=C["beard_grey"], cloak="#8c2b2b", scale=1.06,
          label="Thorgrim Grudgebearer")),
    ("lords/dwarfs", "ungrim-lord",
     dict(DWARF, helmet="mohawk", weapon="axe", weapon_left="axe", armor=C["skin"],
          armor2=C["skin_dark"], trim=C["gold"], beard="forked",
          beard_color=C["beard_orange"], crest=C["beard_orange"], chest_line=False,
          cloak="#b8451f", scale=1.06, label="Ungrim Ironfist")),
    ("lords/dwarfs", "belegar-lord",
     dict(DWARF_ELITE, helmet="dwarf-helm-winged", weapon="hammer", weapon_angle=8,
          shield=True, shield_color="#3f6fa8", beard="long",
          beard_color=C["beard_brown"], cloak="#3f6fa8", scale=1.06,
          label="Belegar Ironhammer")),
    ("lords/dwarfs", "malakai-lord",
     dict(DWARF, helmet="goggles", weapon="gun", weapon_angle=-64, armor=C["leather"],
          armor2="#6f4a2f", trim=C["brass"], beard="long",
          beard_color=C["beard_brown"], scale=1.06, label="Malakai Makaisson")),
    ("lords/dwarfs", "grombrindal-lord",
     dict(DWARF, helmet="dwarf-helm", hat=C["steel"], weapon="axe", weapon_angle=10,
          shield=True, shield_color=C["steel"], armor="#9aa4ad", armor2="#79848d",
          beard="forked", beard_color=C["beard_white"], cloak=C["cloud"], scale=1.06,
          label="Grombrindal, the White Dwarf")),
    # ----------------------------------------------------------------- Khorne
    ("lords/khorne", "valkia-lord",
     dict(helmet="winged-helm", hat=C["khorne_red"], trim=C["brass"],
          armor=C["khorne_red"], armor2=C["khorne_dark"], boots=C["dark"],
          skin=C["skin"], weapon="spear", weapon_angle=8, shield=True,
          shield_color=C["brass"], shield_boss=C["khorne_red"],
          wings=C["dark"], scale=1.06, label="Valkia the Bloody")),
]


def main():
    written = 0
    for folder, name, cfg in SPECS:
        out_dir = os.path.join(OUT_ROOT, folder, "chibi")
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, name + ".svg")
        with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(render(cfg) + "\n")
        written += 1
    sys.stdout.write("wrote %d chibi SVGs\n" % written)


if __name__ == "__main__":
    main()
