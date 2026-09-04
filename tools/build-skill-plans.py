# -*- coding: utf-8 -*-
"""Rebuild levelPlan + stages from the real scraped skill trees.

Ordering is still guide opinion, but every skill name, prerequisite and rank
gate now comes from the game, and the generated order is checked to be legal:
a skill is never taken before its prerequisite or before its rank unlocks.
"""
import io
import json
import os
import re
import sys

SP = sys.argv[1]
ICON_BASE = ("https://images.weserv.nl/?url=https%3A%2F%2Fimg.honga.net"
             "%2Fwarhammer%2Fimages%2Fwarhammer%2F{d}%2F{i}.png&w=640&output=png")

# per-lord priority keywords, matched against skill name + effect text
FOCUS = {
    ("dwarfs", "thorgrim"): (
        ["replenish", "movement", "grudge", "longbeard", "thunderer", "quarreller",
         "artillery", "cannon", "morale", "public order", "military spending"],
        ["ward", "armour", "hit points", "melee defence", "ammunition"]),
    ("dwarfs", "ungrim"): (
        ["slayer", "melee attack", "weapon strength", "charge", "unbreakable",
         "replenish", "movement", "hammerer", "vigour"],
        ["hit points", "armour", "ward", "morale"]),
    ("dwarfs", "belegar"): (
        ["ironbreaker", "irondrake", "thunderer", "melee defence", "armour",
         "replenish", "siege", "movement", "morale", "quarreller"],
        ["ward", "hit points", "ammunition", "public order"]),
    ("dwarfs", "grombrindal"): (
        ["melee attack", "melee defence", "armour", "ward", "hit points",
         "aura", "morale", "replenish", "movement", "longbeard", "hammerer"],
        ["ammunition", "artillery", "public order"]),
    ("cathay", "miao-ying"): (
        ["winds of magic", "spell", "harmony", "jade", "crossbow", "missile",
         "replenish", "movement", "range", "reload", "dragon"],
        ["armour", "melee defence", "hit points", "ward"]),
    ("cathay", "zhao-ming"): (
        ["metal", "spell", "artillery", "cannon", "missile", "reload", "range",
         "caravan", "trade", "replenish", "movement", "harmony"],
        ["armour", "melee defence", "hit points", "ward", "jade"]),
    ("cathay", "yuan-bo"): (
        ["compass", "harmony", "spell", "winds of magic", "jade", "dragon guard",
         "melee defence", "replenish", "movement", "aura"],
        ["armour", "hit points", "ward", "missile", "reload"]),
}

EARLY_BOOST = ["replenish", "movement", "upkeep", "recruit"]


def text_of(s):
    return (s["name"] + " " + " ".join(s["effects"])).lower()


def score(s, primary, secondary):
    t = text_of(s)
    v = 0
    for i, k in enumerate(primary):
        if k in t:
            v += 100 - i * 3
    for i, k in enumerate(secondary):
        if k in t:
            v += 40 - i * 2
    if any(k in t for k in EARLY_BOOST):
        v += 25
    if s["rank"]:
        v -= s["rank"]              # late-unlocking nodes drift later
    return v


def clean_effect(s):
    for e in s["effects"]:
        e = e.strip()
        if not e or e.startswith("(") or len(e) < 6:
            continue
        if e.startswith("Available after spending") or e.startswith("Available at rank"):
            continue
        e = re.sub(r"\s+", " ", e)
        if e.endswith(":"):        # a header for a unit list, not an effect
            continue
        if len(e) > 104:           # trim on a word boundary, never mid-word
            cut = e[:104].rsplit(" ", 1)[0]
            e = cut.rstrip(",") + "…"
        return e
    return "เก็บ node ตามสายหลักของ lord ตัวนี้"


def plan_for(faction, lord, skills):
    primary, secondary = FOCUS[(faction, lord)]
    by_name = {s["name"]: s for s in skills}
    taken, order = set(), []
    scored = sorted(skills, key=lambda s: -score(s, primary, secondary))
    for level in range(2, 51):
        pick = None
        for s in scored:
            if s["name"] in taken:
                continue
            if s["prereq"] and s["prereq"] not in taken:
                continue
            if s["rank"] and s["rank"] > level:
                continue
            pick = s
            break
        if pick is None:                      # nothing legal yet - take the
            for s in scored:                  # cheapest unlockable root
                if s["name"] not in taken and not s["prereq"]:
                    pick = s
                    break
        if pick is None:
            break
        taken.add(pick["name"])
        order.append((level, pick))
    return order


def icon_url(s, ok):
    u = ICON_BASE.format(d=s["icon_dir"].replace("/", "%2F"), i=s["icon"])
    return u if s["icon"] in ok else ""


def stages_from(order, ok):
    bands = [("EARLY", "Lv 2–10", 2, 10), ("MID", "Lv 11–25", 11, 25),
             ("LATE", "Lv 26–50", 26, 50)]
    out = []
    for keyname, title, lo, hi in bands:
        rows = [(lv, s) for lv, s in order if lo <= lv <= hi]
        n = min(7, len(rows))
        idx = [round(i * (len(rows) - 1) / (n - 1)) for i in range(n)] if n > 1 else [0]
        steps = []
        for i in sorted(set(idx)):
            lv, s = rows[i]
            steps.append({
                "order": str(lv),
                "name": s["name"],
                "points": ("Rank %d+" % s["rank"]) if s["rank"] else "",
                "reason": clean_effect(s),
                "iconUrl": icon_url(s, ok),
            })
        out.append({"key": keyname, "title": title, "steps": steps})
    return out


def main():
    data = json.load(io.open(os.path.join(SP, "skills.json"), encoding="utf-8"))
    ok = set(json.load(io.open(os.path.join(SP, "icons_ok.json"), encoding="utf-8")))
    plans = {}
    for faction in data:
        for lord, skills in data[faction].items():
            order = plan_for(faction, lord, skills)
            # legality check
            taken = set()
            for lv, s in order:
                assert not s["prereq"] or s["prereq"] in taken, (lord, s["name"])
                assert not s["rank"] or s["rank"] <= lv, (lord, s["name"], s["rank"], lv)
                taken.add(s["name"])
            rows = [{"level": lv, "skill": s["name"], "note": clean_effect(s)}
                    for lv, s in order]
            # a lord with fewer nodes than points spends the rest topping up
            # skills that have more than one rank - that is what the game does
            pad = 0
            for lv in range(len(order) + 2, 51):
                rows.append({"level": lv, "skill": "Flex point",
                             "note": "node หมดแล้ว - ลงแต้มเพิ่มใน skill ที่ยังไม่เต็มแรงค์"})
                pad += 1
            assert len(rows) == 49, (lord, len(rows))
            plans.setdefault(faction, {})[lord] = {
                "levelPlan": rows,
                "stages": stages_from(order, ok),
            }
            gated = sum(1 for _, s in order if s["rank"])
            print("%-7s %-12s %2d real nodes + %d flex | %d rank-gated | prereqs legal"
                  % (faction, lord, len(order), pad, gated))
    with io.open(os.path.join(SP, "plans.json"), "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=1)
    print("saved plans.json")


if __name__ == "__main__":
    main()
