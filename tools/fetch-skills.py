# -*- coding: utf-8 -*-
"""Render totalwarhammerplanner lord pages with headless Chrome and pull the
real skill nodes (name, icon key, prerequisite, per-point effects)."""
import io
import json
import os
import re
import subprocess
import sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "https://totalwarhammerplanner.com/planner/vanilla3/%s/%s"
OUT = sys.argv[1]

CANDIDATES = [
    ("dwarfs", "thorgrim", "dwf_dwarfs", "dwf_thorgrim"),
    ("dwarfs", "ungrim", "dwf_dwarfs", "dwf_ungrim"),
    ("dwarfs", "belegar", "dwf_dwarfs", "dwf_belegar"),
    ("dwarfs", "grombrindal", "dwf_dwarfs", "dwf_grombrindal"),
    ("cathay", "miao-ying", "cth_cathay", "cth_miao_ying"),
    ("cathay", "zhao-ming", "cth_cathay", "cth_zhao_ming"),
    ("cathay", "yuan-bo", "cth_cathay", "cth_yuan_bo"),
]

NODE = re.compile(
    r'src="/imgs/vanilla3/([^"]+?)/([^"/]+?)\.webp"[^>]*>\s*'
    r'<div class="flex flex-col justify-center">\s*<h2[^>]*>([^<]+)</h2>', re.S)


def strip_tags(x):
    x = re.sub(r"<[^>]+>", "\n", x)
    out = []
    for t in x.split("\n"):
        t = t.strip()
        if t:
            out.append(t)
    return out


def unescape(x):
    return (x.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
             .replace("\ufffd", "'").replace("&lt;", "<").replace("&gt;", ">"))


def render(url, dest):
    if os.path.isfile(dest) and os.path.getsize(dest) > 100000:
        return io.open(dest, encoding="utf-8", errors="replace").read()
    with io.open(dest, "wb") as f:
        subprocess.call([CHROME, "--headless=new", "--disable-gpu",
                         "--virtual-time-budget=15000", "--dump-dom", url],
                        stdout=f, stderr=subprocess.DEVNULL)
    return io.open(dest, encoding="utf-8", errors="replace").read()


def parse(html):
    skills, seen = [], set()
    for icon_dir, icon, name in NODE.findall(html):
        name = unescape(name.strip())
        if name in seen:
            continue
        seen.add(name)
        prereq, effects = None, []
        # the tooltip repeats the name; read the block that follows it
        for m in re.finditer(r">%s<" % re.escape(name.replace("&", "&amp;")), html):
            block = strip_tags(html[m.start():m.start() + 2600])
            body = [t for t in block[1:] if t not in ("Ad Test", "Skill Up",
                                                      "Skill Down", "Close", name)]
            for t in body:
                pm = re.match(r'Available after unlocking "(.+)"$', t)
                if pm:
                    prereq = unescape(pm.group(1))
                elif t and not t.startswith("<") and len(t) < 160:
                    if t not in effects:
                        effects.append(unescape(t))
            if effects:
                break
        rank = None
        keep = []
        for t in effects:
            rm = re.match(r"Available at rank (\d+)$", t)
            if rm:
                rank = int(rm.group(1))
            elif not t.startswith("Available after unlocking"):
                keep.append(t)
        skills.append({"name": name, "icon": icon, "icon_dir": icon_dir,
                       "prereq": prereq, "rank": rank, "effects": keep[:5]})
    return skills


results = {}
for faction, lord, fkey, lkey in CANDIDATES:
    url = BASE % (fkey, lkey)
    dest = os.path.join(OUT, "planner_%s_%s.html" % (faction, lord))
    html = render(url, dest)
    skills = parse(html)
    results.setdefault(faction, {})[lord] = skills
    sys.stdout.write("%-7s %-12s %-22s %5d bytes  %2d nodes\n"
                     % (faction, lord, lkey, len(html), len(skills)))

with io.open(os.path.join(OUT, "skills.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
sys.stdout.write("saved skills.json\n")
