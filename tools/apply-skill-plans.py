# -*- coding: utf-8 -*-
"""Write the real-skill level plans and stages into the faction JSON."""
import io
import json
import os
import sys

SP = sys.argv[1]

# skillBuild.summary rewritten to describe what the real tree actually contains
SUMMARY = {
    ("dwarfs", "thorgrim"):
        "สาย Grudge + ขวัญกำลังใจก่อน → Rune-Warded Armour/Full Plate ให้ยืนไหว "
        "→ สายบัฟแนวยิงกับปืนใหญ่ → ปิดด้วยสายชนของ Thorgrim เอง",
    ("dwarfs", "ungrim"):
        "เปิดสาย Slayer กับ Weapon Strength ก่อน → เก็บ vigour/hit points ให้ยืนไฟต์ยาว "
        "→ ปิดด้วยสายชนตัวต่อตัวของ Ungrim",
    ("dwarfs", "belegar"):
        "Replenishment + สาย Ironbreaker/Irondrake ก่อน → armour กับ melee defence "
        "→ ปิดด้วยสายยิงและ siege สำหรับตี Karak คืน",
    ("dwarfs", "grombrindal"):
        "เก็บสายตัวเอง (melee, armour, ward) คู่กับ aura ค้ำกอง "
        "→ แล้วค่อยลงสายบัฟยูนิต node ของ Grombrindal มีน้อยกว่าแต้ม จึงเหลือแต้มไปเติมแรงค์",
    ("cathay", "miao-ying"):
        "Replenishment + movement ก่อน → เปิดสเปล Lore of Life กับ Yin ให้ครบ "
        "→ Aura of Majesty แล้วต่อสายบัฟ Jade/แนวยิง → ปิดด้วยสายมังกร",
    ("cathay", "zhao-ming"):
        "Replenishment ก่อน → Lore of Metal ครบชุด (Glittering Robe, Final Transmutation) "
        "→ สายบัฟปืนใหญ่กับแนวยิง → ปิดด้วยสายคาราวานและสายชน",
    ("cathay", "yuan-bo"):
        "เปิด Wu Xing War Compass กับ Harmony ก่อน → สเปลสายซัพพอร์ต "
        "→ บัฟ Jade/Dragon Guard รอบ compass → ปิดด้วยสายตัวเอง",
}

# fields that stated the wrong magic lore
FIELD_FIX = {
    ("cathay", "miao-ying"): {
        "style": "Lore of Life + Yin",
        "summary": ("ตัวเริ่มต้นที่ง่ายที่สุดของ Cathay: ตั้งแนว Jade Warriors ค้ำหน้า, "
                    "Crossbowmen ยิงหลัง แล้ว Miao Ying ใช้สเปลสาย Lore of Life กับ Yin "
                    "(Earth Blood, Flesh to Stone, Talons of Night) ทั้งฟื้นกำลังพลและกดกองศัตรู "
                    "พอ late ค่อยแปลงร่างมังกรเข้าไปปิดไฟต์เอง"),
    },
    ("cathay", "yuan-bo"): {
        "style": "Wu Xing War Compass + Support Magic",
        "summary": ("สายค้ำแนวรอบ Wu Xing War Compass: ลากรถศึกไปกลางสนาม ตั้ง Jade Warriors "
                    "กับ Dragon Guard รอบ ๆ แล้วใช้ buff จาก compass บวกสเปลซัพพอร์ต "
                    "(Net of Amyntok, Blossom Wind, Comet of Casandora) "
                    "ทำให้ทั้งกองแข็งกว่าศัตรูทุกก้อน"),
    },
}


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


def save(p, d):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    plans = load(os.path.join(SP, "plans.json"))
    touched = 0
    for faction in plans:
        p = "src/assets/data/%s.json" % faction
        doc = load(p)
        for lord in doc["data"]["faction"]["lords"]:
            key = (faction, lord["id"])
            if lord["id"] not in plans[faction]:
                print("  skip %-7s %-12s (no scraped tree)" % (faction, lord["id"]))
                continue
            new = plans[faction][lord["id"]]
            lord["skillBuild"]["levelPlan"] = new["levelPlan"]
            lord["skillBuild"]["stages"] = new["stages"]
            if key in SUMMARY:
                lord["skillBuild"]["summary"] = SUMMARY[key]
            for field, value in FIELD_FIX.get(key, {}).items():
                lord[field] = value
            touched += 1
            print("  %-7s %-12s levelPlan+stages replaced%s"
                  % (faction, lord["id"], "  (+lore fields fixed)" if key in FIELD_FIX else ""))
        save(p, doc)
    print("updated %d lords" % touched)


if __name__ == "__main__":
    main()
