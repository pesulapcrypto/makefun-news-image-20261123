#!/usr/bin/env python3
"""THE WIDE LEDGER — compose.py (NI23 G4, akun12).

One-page broadsheet front page for Monday 23 November 2026, drawn with PIL.
Local build tool only; the shipped entry program (main.py) is stdlib copy-only.
Layouts A and B are rendered from the same verified story set (pool
ni23-pool.md) and duelled at thumbnail size; the winner becomes entry.png.
Data is kept in fleet style: grid / NUMS / TL / BRIEFS_L / BRIEFS_R / dc / PINS.
"""

import sys
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MARGIN = 14

IVORY = (246, 240, 221)
IVORY_DARK = (238, 229, 203)
INK = (46, 26, 71)          # deep purple ink
INK_SOFT = (74, 54, 102)
MUSTARD = (217, 164, 4)
RED = (166, 38, 57)
WHITE = (255, 253, 246)

REGIONS = {
    "MIDDLE EAST": (179, 84, 30),
    "EUROPE": (36, 86, 166),
    "SOUTHEAST ASIA": (14, 124, 97),
    "SOUTH ASIA": (166, 38, 57),
    "NORTH AMERICA": (108, 74, 176),
    "AFRICA": (138, 109, 31),
    "ASIA-PACIFIC": (46, 127, 168),
    "GLOBAL": (85, 80, 73),
}
CHIP_COLORS = {
    "REPORTED": (36, 86, 166),
    "CLAIM": (179, 84, 30),
    "DENIAL": (166, 38, 57),
    "ONGOING": (138, 109, 31),
    "OFFICIAL": (14, 124, 97),
    "ON RECORD": (108, 74, 176),
}
CHIPS = {1: "OFFICIAL", 2: "REPORTED", 3: "OFFICIAL", 4: "CLAIM",
         5: "REPORTED", 6: "ON RECORD", 7: "ONGOING", 8: "OFFICIAL",
         9: "REPORTED", 10: "REPORTED", 11: "OFFICIAL", 12: "ONGOING",
         13: "REPORTED"}

F_BLACK = FONT_DIR + "PlayfairDisplay-Black.ttf"
F_ARCH = FONT_DIR + "Archivo.ttf"
F_ABOLD = FONT_DIR + "Archivo-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fb(n):
    return font(F_ABOLD, n)


def fr(n):
    return font(F_ARCH, n)


def fsr(n):
    return font(F_ARCH, n)


def tw(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w, max_lines):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and tw(draw, last + "…", fnt) > max_w:
            last = last[:-1]
        lines[-1] = last + "…"
    return lines


def wrap2(draw, text, fnt, widths):
    """Greedy wrap where line i may use widths[min(i, len(widths)-1)]."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        limit = widths[min(len(lines), len(widths) - 1)]
        trial = (cur + " " + wd).strip()
        if tw(draw, trial, fnt) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
            if len(lines) >= len(widths):
                break
    if cur and len(lines) < len(widths):
        lines.append(cur)
    return lines


def fit_line(draw, text, fnt, max_w):
    if tw(draw, text, fnt) <= max_w:
        return text
    while text and tw(draw, text + "…", fnt) > max_w:
        text = text[:-1]
    return text + "…"


# ---------------------------------------------------------------- stories ---
# grid tuples: (num, region, topic, src, head, deck, kind)
grid = [
    (1, "SOUTHEAST ASIA", "THE HAGUE — COURT RULING", "Guardian / NYT wire",
     "ICJ Rules Myanmar Guilty of Genocide",
     "The World Court ruled Myanmar's 2017 campaign against the Rohingya was genocide; more than 700,000 people fled.",
     "gavel"),
    (2, "EUROPE", "KYIV, UKRAINE — WAR · RESCUE", "BBC",
     "Kyiv Boy, 7, Pulled Alive From Rubble",
     "6 dead; boy freed in Kyiv.",
     "rubble"),
    (3, "EUROPE", "CLIMATE SUMMIT — TALKS END", "BBC/AP",
     "COP31 Ends Without a Deal",
     "Draft of 23 Nov omits fossil fuels.",
     "factory"),
    (4, "MIDDLE EAST", "BAHRAIN — WAR · CLAIM", "AP/AFP",
     "IRGC Claims Patriot Radars Hit",
     "A Tehran claim; not US-confirmed.",
     "radar"),
    (5, "MIDDLE EAST", "HORMUZ — WAR · SHIPPING", "AP live",
     "Tankers Burn in Hormuz Strait",
     "Iran–US war widens into the Gulf.",
     "tanker"),
    (6, "EUROPE", "KYIV REGION — WAR · MISSING", "JagranJosh",
     "14 Missing, Zelenskiy Says",
     "Zelenskiy: 14 lost in Kyiv.",
     "drone"),
    (7, "EUROPE", "FINLAND — SHIPPING · FIRE", "BBC",
     "Russian Cargo Ship Still Burns",
     "Ablaze off Finland, day 2; afloat.",
     "ship"),
    (8, "NORTH AMERICA", "WASHINGTON — POLITICS", "BBC",
     "Democrats Take House 258–173",
     "Biggest House win since 1992.",
     "capitol"),
    (9, "SOUTH ASIA", "WELLINGTON — CRICKET · TEST", "ObserverVoice",
     "India Record 720/9 at Wellington",
     "Highest Test total in NZ.",
     "cricket"),
    (10, "GLOBAL", "GLOBAL MARKETS — GOLD", "ObserverVoice",
     "Gold Slides to $3,538",
     "Down $2,000 from the $5,595 record of 2026.",
     "gold"),
    (11, "NORTH AMERICA", "IOWA, USA — SAFETY ORDER", "BBC",
     "Army to Detonate Iowa Explosives",
     "The US Army defies a court order.",
     "bomb"),
    (12, "NORTH AMERICA", "WASHINGTON — CYBER · PROBE", "AP wire",
     "FBI Probes Justice Database Hack",
     "Agents probe Justice Dept. hack.",
     "database"),
    (13, "EUROPE", "TURIN — TENNIS · FINAL", "BBC",
     "Alcaraz Wins First ATP Title",
     "Beat Zverev in the Turin final.",
     "trophy"),
]

PINS = [(40, 10), (29, 5), (28, 8), (33, 10), (34, 10), (29, 6), (28, 4),
        (10, 7), (50, 17), (26, 9), (8, 7), (11, 7), (26, 6)]

NUMS = [
    ("258–173", "US House · card 8"),
    ("720/9d", "India record · card 9"),
    ("14", "missing, Kyiv · card 6"),
    ("$3,538", "gold / ounce · card 10"),
    ("700,000+", "Rohingya fled · card 1"),
    ("65.9%", "IndiGo share · story 38"),
]

TL = [
    ("00:02Z", "UN killer-AI talks deal"),
    ("02:00Z", "Albanese on COP31"),
    ("MORNING", "ICJ Myanmar ruling"),
    ("MIDDAY", "Kyiv boy rescued"),
    ("AFTERNOON", "House 258–173 confirmed"),
    ("EVENING", "Alcaraz takes ATP title"),
]

BRIEFS_L = [
    "Houthi missile on Saudi intercepted",
    "Swimmer crosses Hormuz Strait",
    "UN to keep talking on killer AI",
    "US releases more UFO footage",
    "PM Albanese slams COP31 result",
    "Russia-bound ship towed off Finland",
    "Blast at Benghazi: suspected drone",
    "UK–EU reset: Burnham 'landmark'",
    "Thousands march in Lisbon",
    "Myanmar junta: ASEAN ruling unfair",
    "Ex-rebels trapped in Cameroon",
    "Escaped lion alarms Turkish town",
    "Nepal PM Shah talks with PM Modi",
    "India, Bulgaria talk IMEC, Black Sea",
]
BRIEFS_R = [
    "Guru Nanak Jayanti celebrated",
    "UP air-raid drills in 75 districts",
    "Factory fire UPDATE: 7 found, 50 lost",
    "Wellington day 5: India chase win",
    "India win ODI series in NZ 3–2",
    "Anupama defends IBSF snooker crown",
    "World Chess Championship grips fans",
    "MP Wadkute dies in Delhi",
    "Kota pilgrim bus tragedy: 9 dead",
    "Tata Steel sale: Rs 28,000 crore",
    "IndiGo at 65.9%; SpiceJet audit call",
    "IFFI Goa hosts BRICS roundtable",
    "Modi opens AI centre at IIT Patna",
]

dc = ("Xi–Trump–Putin summit, 19 Nov · Russian missiles in Poland, 20 Nov · "
      "Paolo Bulgari died, reported 22 Nov · 24 civilians killed in South Sudan, 22 Nov · "
      "Bolsonaro stable in ICU in Brasilia, 22 Nov · South Korea education minister quits, 22 Nov · "
      "Indonesia candy-factory fire AS AN EVENT, 22 Nov")

REGION_COUNTS = [
    ("SOUTH ASIA", 14), ("EUROPE", 9), ("MIDDLE EAST", 4),
    ("NORTH AMERICA", 4), ("SOUTHEAST ASIA", 3), ("GLOBAL", 3),
    ("AFRICA", 2), ("ASIA-PACIFIC", 1),
]

MAP_ROWS = [
    "                                                        ",
    "      #####  ##           #############  ####           ",
    "    ######### #         #######################  ##     ",
    "   ##########          ###################### ######    ",
    "    ########            ################    #####       ",
    "     ######              ##############      ###        ",
    "      ####    #           ############                  ",
    "       ##    ###           ##########       ##          ",
    "            #####           ########       ####         ",
    "           #######           ######        ######       ",
    "           ########           ####          ####        ",
    "            ######            ##            ###         ",
    "             ####                           ##    ##    ",
    "             ###                                        ",
    "              ##                                        ",
]


# ---------------------------------------------------------------- drawing ---
def icon(draw, kind, x, y, s, col):
    if kind == "gavel":
        draw.rectangle([x + s * .18, y + s * .62, x + s * .82, y + s * .72], fill=col)
        draw.line([x + s * .3, y + s * .55, x + s * .62, y + s * .22], fill=col, width=max(2, s // 9))
        draw.rectangle([x + s * .52, y + s * .12, x + s * .74, y + s * .3], outline=col, width=max(2, s // 10))
    elif kind == "rubble":
        draw.polygon([(x + 2, y + s - 3), (x + s * .4, y + s * .3), (x + s * .62, y + s - 3)], outline=col, width=2)
        draw.polygon([(x + s * .45, y + s - 3), (x + s * .72, y + s * .45), (x + s - 2, y + s - 3)], outline=col, width=2)
        draw.line([x + s * .8, y + 4, x + s * .8, y + s * .4], fill=col, width=2)
        draw.line([x + s * .8, y + s * .4, x + s * .6, y + s * .55], fill=col, width=2)
    elif kind == "factory":
        draw.rectangle([x + 3, y + s * .45, x + s - 3, y + s - 3], outline=col, width=2)
        draw.rectangle([x + s * .15, y + s * .15, x + s * .3, y + s * .45], outline=col, width=2)
        for i in range(3):
            cx = x + s * (.45 + .16 * i)
            draw.ellipse([cx, y + 2, cx + s * .12, y + s * .14], fill=col)
    elif kind == "radar":
        draw.line([x + s * .5, y + s - 3, x + s * .5, y + s * .45], fill=col, width=2)
        draw.arc([x + s * .18, y + s * .05, x + s * .82, y + s * .6], 200, 340, fill=col, width=2)
        draw.arc([x + s * .1, y + s * .02, x + s * .9, y + s * .66], 200, 340, fill=col, width=1)
        draw.ellipse([x + s * .44, y + s * .3, x + s * .56, y + s * .44], fill=col)
    elif kind == "tanker":
        draw.polygon([(x + 2, y + s * .62), (x + s - 2, y + s * .62), (x + s * .85, y + s - 3), (x + s * .15, y + s - 3)], fill=col)
        draw.rectangle([x + s * .4, y + s * .42, x + s * .6, y + s * .62], fill=col)
        draw.polygon([(x + s * .5, y + s * .08), (x + s * .38, y + s * .4), (x + s * .62, y + s * .4)], fill=(214, 90, 20))
    elif kind == "drone":
        for cx, cy in [(x + s * .2, y + s * .2), (x + s * .8, y + s * .2), (x + s * .2, y + s * .8), (x + s * .8, y + s * .8)]:
            draw.ellipse([cx - s * .1, cy - s * .07, cx + s * .1, cy + s * .07], outline=col, width=2)
        draw.rectangle([x + s * .38, y + s * .4, x + s * .62, y + s * .6], fill=col)
        draw.line([x + s * .25, y + s * .25, x + s * .42, y + s * .42], fill=col, width=2)
        draw.line([x + s * .75, y + s * .25, x + s * .58, y + s * .42], fill=col, width=2)
        draw.line([x + s * .25, y + s * .75, x + s * .42, y + s * .58], fill=col, width=2)
        draw.line([x + s * .75, y + s * .75, x + s * .58, y + s * .58], fill=col, width=2)
    elif kind == "ship":
        draw.polygon([(x + 2, y + s * .6), (x + s - 2, y + s * .6), (x + s * .82, y + s - 3), (x + s * .18, y + s - 3)], fill=col)
        draw.rectangle([x + s * .3, y + s * .38, x + s * .55, y + s * .6], fill=col)
        draw.polygon([(x + s * .62, y + s * .05), (x + s * .5, y + s * .38), (x + s * .74, y + s * .38)], fill=(214, 90, 20))
    elif kind == "capitol":
        draw.polygon([(x + s * .5, y + 4), (x + s * .15, y + s * .35), (x + s * .85, y + s * .35)], fill=col)
        for i in range(4):
            cx = x + s * (.2 + .17 * i)
            draw.rectangle([cx, y + s * .4, cx + s * .07, y + s * .78], fill=col)
        draw.rectangle([x + 3, y + s * .82, x + s - 3, y + s * .9], fill=col)
    elif kind == "cricket":
        draw.line([x + s * .3, y + s * .85, x + s * .55, y + s * .2], fill=col, width=max(2, s // 8))
        draw.rectangle([x + s * .48, y + s * .12, x + s * .66, y + s * .34], fill=col)
        draw.ellipse([x + s * .68, y + s * .62, x + s * .88, y + s * .82], fill=(166, 38, 57))
    elif kind == "gold":
        for ox, oy in [(0.12, 0.55), (0.42, 0.55), (0.27, 0.28)]:
            draw.polygon([(x + s * ox, y + s * (oy + .18)), (x + s * (ox + .1), y + s * oy),
                          (x + s * (ox + .36), y + s * oy), (x + s * (ox + .46), y + s * (oy + .18))], fill=(198, 148, 10))
    elif kind == "bomb":
        draw.ellipse([x + s * .25, y + s * .3, x + s * .8, y + s * .88], fill=col)
        draw.line([x + s * .52, y + s * .3, x + s * .68, y + s * .12], fill=col, width=2)
        for dx, dy in [(.78, .06), (.9, .16), (.7, .2)]:
            draw.line([x + s * .8, y + s * .1, x + s * dx, y + s * dy], fill=(214, 90, 20), width=2)
    elif kind == "database":
        draw.ellipse([x + s * .2, y + s * .08, x + s * .8, y + s * .3], outline=col, width=2)
        draw.line([x + s * .2, y + s * .08, x + s * .2, y + s * .85], fill=col, width=2)
        draw.line([x + s * .8, y + s * .08, x + s * .8, y + s * .85], fill=col, width=2)
        draw.arc([x + s * .2, y + s * .62, x + s * .8, y + s * .85], 0, 180, fill=col, width=2)
        draw.arc([x + s * .2, y + s * .35, x + s * .8, y + s * .58], 0, 180, fill=col, width=2)
    elif kind == "trophy":
        draw.rectangle([x + s * .34, y + s * .12, x + s * .66, y + s * .45], fill=col)
        draw.arc([x + s * .12, y + s * .14, x + s * .36, y + s * .4], 90, 270, fill=col, width=2)
        draw.arc([x + s * .64, y + s * .14, x + s * .88, y + s * .4], 270, 90, fill=col, width=2)
        draw.rectangle([x + s * .46, y + s * .45, x + s * .54, y + s * .68], fill=col)
        draw.rectangle([x + s * .32, y + s * .68, x + s * .68, y + s * .8], fill=col)


def chip(draw, x, y, label):
    fnt = fb(11)
    wdt = tw(draw, label, fnt) + 12
    draw.rectangle([x, y, x + wdt, y + 15], fill=CHIP_COLORS[label])
    draw.text((x + 6, y + 2), label, font=fnt, fill=WHITE)
    return wdt


def lead(draw, c, x, y, wdt, hgt, flip=False):
    num, region, topic, src, head, deck, kind = c
    chip_lab = CHIPS[num]
    rcol = REGIONS[region]
    draw.rectangle([x, y, x + wdt, y + hgt], fill=WHITE, outline=INK, width=1)
    draw.rectangle([x, y, x + wdt, y + 4], fill=rcol)
    thumb_w = 240
    if flip:
        draw.rectangle([x + wdt - thumb_w, y + 5, x + wdt - 1, y + hgt - 1], fill=IVORY_DARK)
        icon(draw, kind, x + wdt - thumb_w + (thumb_w - 84) // 2, y + (hgt - 84) // 2, 84, INK)
        tx = x + 10
        tw_max = wdt - thumb_w - 20
    else:
        draw.rectangle([x + 1, y + 5, x + thumb_w, y + hgt - 1], fill=IVORY_DARK)
        icon(draw, kind, x + (thumb_w - 84) // 2 + 2, y + (hgt - 84) // 2, 84, INK)
        tx = x + thumb_w + 10
        tw_max = wdt - thumb_w - 18
    bf = fb(19)
    draw.rectangle([x + 5, y + 8, x + 31, y + 32], fill=INK)
    ns = str(num)
    draw.text((x + 18 - tw(draw, ns, bf) / 2, y + 10), ns, font=bf, fill=(255, 220, 90))
    hf = fb(12)
    cf = fb(11)
    cw = tw(draw, chip_lab, cf) + 12
    chip_x = x + wdt - cw - 6 if not flip else tx + tw_max - cw + 10
    draw.text((tx, y + 8), fit_line(draw, topic, hf, tw_max - cw - 6), font=hf, fill=rcol)
    chip(draw, chip_x, y + 7, chip_lab)
    tf = fb(36)
    ly = y + 25
    for ln in wrap(draw, head, tf, tw_max, 2):
        draw.text((tx, ly), ln, font=tf, fill=INK)
        ly += 38
    ff = fr(16)
    fy = ly + 1
    for ln in wrap(draw, deck, ff, tw_max, 2):
        draw.text((tx, fy), ln, font=ff, fill=INK_SOFT)
        fy += 18
    sf = font(F_ARCH, 10)
    stxt = "Source: " + src
    sx = x + wdt - tw(draw, stxt, sf) - 7 if not flip else tx
    draw.text((sx, y + hgt - 14), stxt, font=sf, fill=(110, 96, 128))


def mini(draw, c, x, y, wdt, hgt):
    num, region, topic, src, head, deck, kind = c
    chip_lab = CHIPS[num]
    rcol = REGIONS[region]
    draw.rectangle([x, y, x + wdt, y + hgt], fill=WHITE, outline=INK, width=1)
    draw.rectangle([x, y, x + wdt, y + 4], fill=rcol)
    sf = font(F_ARCH, 10)
    stxt = "Source: " + src
    src_w = tw(draw, stxt, sf)
    cf = fb(11)
    cw = tw(draw, chip_lab, cf) + 12
    bf = fb(14)
    draw.rectangle([x + 6, y + 7, x + 28, y + 29], fill=INK)
    ns = str(num)
    draw.text((x + 17 - tw(draw, ns, bf) / 2, y + 9), ns, font=bf, fill=(255, 220, 90))
    icon(draw, kind, x + 33, y + 6, 24, INK)
    hf = fb(11)
    tx = x + 62
    head = fit_line(draw, topic, hf, wdt - 70 - cw - 6)
    draw.text((tx, y + 9), head, font=hf, fill=rcol)
    chip(draw, x + wdt - cw - 6, y + 7, chip_lab)
    tf = fb(28)
    tx2 = x + 8
    tw2 = wdt - 16
    lines = wrap(draw, head, tf, tw2, 2)
    ly = y + 33
    for ln in lines:
        draw.text((tx2, ly), ln, font=tf, fill=INK)
        ly += 29
    ff = fr(15)
    if len(lines) >= 2:
        widths = [tw2 - src_w - 10]
    else:
        widths = [tw2, tw2 - src_w - 10]
    fy = ly + 1
    for ln in wrap2(draw, deck, ff, widths):
        draw.text((tx2, fy), ln, font=ff, fill=INK_SOFT)
        fy += 17
    draw.text((x + wdt - src_w - 7, y + hgt - 14), stxt, font=sf, fill=(110, 96, 128))


def header_block(draw):
    bf = fb(13)
    draw.text((MARGIN, 5), "THE WIDE LEDGER", font=bf, fill=INK)
    kick = "40 STORIES · 8 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    draw.text((W - MARGIN - tw(draw, kick, bf), 5), kick, font=bf, fill=INK)
    draw.line([MARGIN, 26, W - MARGIN, 26], fill=INK, width=2)
    nf = font(F_BLACK, 32)
    name = "THE WIDE LEDGER"
    draw.text(((W - tw(draw, name, nf)) / 2, 30), name, font=nf, fill=INK)
    df = font(F_BLACK, 72)
    date = "Monday 23 November 2026"
    draw.text(((W - tw(draw, date, df)) / 2, 62), date, font=df, fill=INK)
    sf = fr(15)
    sub = "ICJ: Myanmar guilty of genocide  ·  Kyiv boy pulled alive from rubble  ·  COP31 ends with no deal"
    draw.text(((W - tw(draw, sub, sf)) / 2, 142), sub, font=sf, fill=RED)
    draw.line([MARGIN, 164, W - MARGIN, 164], fill=MUSTARD, width=3)
    rf = fb(12)
    x, y = MARGIN, 170
    for rname, cnt in REGION_COUNTS:
        label = "%s %d" % (rname, cnt)
        wdt = tw(draw, label, rf) + 14
        draw.rectangle([x, y, x + wdt, y + 17], fill=REGIONS[rname])
        draw.text((x + 7, y + 2), label, font=rf, fill=WHITE)
        x += wdt + 6
    tf = fb(12)
    tf2 = fr(12)
    x, y = MARGIN, 192
    draw.text((x, y), "THE DAY, UTC:", font=tf, fill=INK)
    x += tw(draw, "THE DAY, UTC:", tf) + 8
    for tstamp, ev in TL:
        draw.text((x, y), tstamp + " ", font=tf, fill=RED)
        x += tw(draw, tstamp + " ", tf)
        draw.text((x, y), ev, font=tf2, fill=INK_SOFT)
        x += tw(draw, ev, tf2) + 14
    draw.line([MARGIN, 212, W - MARGIN, 212], fill=INK, width=1)


def numbers_box(draw, x, y, wdt, hgt):
    draw.rectangle([x, y, x + wdt, y + hgt], fill=INK)
    hf = fb(13)
    draw.text((x + 10, y + 6), "THE DAY IN NUMBERS", font=hf, fill=(255, 220, 90))
    nf = fb(26)
    lf = fr(9)
    colw = (wdt - 20) // 2
    for i, (big, lab) in enumerate(NUMS):
        cx = x + 10 + (i % 2) * colw
        cy = y + 21 + (i // 2) * 26
        draw.text((cx, cy), big, font=nf, fill=WHITE)
        draw.text((cx + 3, cy + 22), lab, font=lf, fill=(216, 205, 235))


def draw_dotted_map(draw, x, y, wdt, hgt):
    draw.rectangle([x, y, x + wdt, y + hgt], fill=WHITE, outline=INK, width=1)
    hf = fb(12)
    draw.text((x + 8, y + 5), "WHERE IT HAPPENED — pins = story numbers", font=hf, fill=INK)
    cols = len(MAP_ROWS[0])
    rows = len(MAP_ROWS)
    gx0, gy0 = x + 10, y + 24
    cell_w = (wdt - 20) / cols
    cell_h = (hgt - 48) / rows
    for r, row in enumerate(MAP_ROWS):
        for cc, ch in enumerate(row):
            if ch == "#":
                cx = gx0 + cc * cell_w
                cy = gy0 + r * cell_h
                draw.ellipse([cx, cy, cx + 2.4, cy + 2.4], fill=(150, 138, 170))
    pf = fb(8)
    for c, (px_, py_) in zip(grid, PINS):
        px = gx0 + px_ * cell_w
        py = gy0 + py_ * cell_h
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=MUSTARD, outline=INK, width=1)
        ns = str(c[0])
        draw.text((px - tw(draw, ns, pf) / 2, py - 4), ns, font=pf, fill=INK)
    lf = fr(10)
    draw.text((x + 8, y + hgt - 14), "Dots mark land; pins mark the stories.", font=lf, fill=INK_SOFT)


def datecheck_box(draw, x, y, wdt, hgt):
    draw.rectangle([x, y, x + wdt, y + hgt], fill=(250, 238, 238), outline=RED, width=2)
    hf = fb(13)
    draw.text((x + 10, y + 6), "DATE CHECK — NOT 23 NOV, NOT NEWS HERE", font=hf, fill=RED)
    bf = fr(11)
    ly = y + 25
    for item in [s.strip() for s in dc.split("·")]:
        draw.text((x + 10, ly), "✕ " + fit_line(draw, item, bf, wdt - 24), font=bf, fill=(120, 30, 44))
        ly += 11


def also_block(draw, y):
    hf = fb(13)
    draw.text((MARGIN, y), "ALSO ON MONDAY 23 NOVEMBER", font=hf, fill=INK)
    draw.line([MARGIN, y + 17, W - MARGIN, y + 17], fill=MUSTARD, width=2)
    bf = fsr(13)
    briefs = BRIEFS_L + BRIEFS_R
    colw = (W - 2 * MARGIN - 18) // 4
    per_col = 7
    for i, title in enumerate(briefs):
        cx = MARGIN + (i // per_col) * (colw + 6)
        cy = y + 23 + round((i % per_col) * 12.5)
        draw.text((cx, cy), fit_line(draw, "%d · %s" % (14 + i, title), bf, colw), font=bf, fill=INK_SOFT)


def footer_block(draw, y):
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    ff = fr(12)
    l1 = ("HOW SURE: REPORTED = reported by the named source · CLAIM = one side's account, labelled as such · "
          "ONGOING = still developing · OFFICIAL / ON RECORD = stated by an authority or on the record.")
    l2 = "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. · Original drawings."
    draw.text((MARGIN, y + 5), fit_line(draw, l1, ff, W - 2 * MARGIN), font=ff, fill=INK)
    draw.text((MARGIN, y + 21), fit_line(draw, l2, ff, W - 2 * MARGIN), font=ff, fill=INK)


def build(variant):
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)
    header_block(draw)
    third = (W - 2 * MARGIN - 12) // 3
    by = 767
    lead(draw, grid[0], MARGIN, 220, W - 2 * MARGIN, 104, flip=(variant == "B"))
    cw = (W - 2 * MARGIN - 12) // 3
    for i, c in enumerate(grid[1:]):
        cx = MARGIN + (i % 3) * (cw + 6)
        cy = 330 + (i // 3) * (104 + 5)
        mini(draw, c, cx, cy, cw, 104)
    if variant == "A":
        numbers_box(draw, MARGIN, by, third, 106)
        draw_dotted_map(draw, MARGIN + third + 6, by, third, 106)
        datecheck_box(draw, MARGIN + 2 * third + 12, by, third, 106)
    else:
        datecheck_box(draw, MARGIN, by, third, 106)
        draw_dotted_map(draw, MARGIN + third + 6, by, third, 106)
        numbers_box(draw, MARGIN + 2 * third + 12, by, third, 106)
    also_block(draw, 879)
    footer_block(draw, 982)
    return img


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-akun12/entry.png"
    img = build(which)
    # Flat palette page: quantize to 256 colours (no dither) — same picture,
    # far fewer bytes; on an exact judge tie the smaller file wins.
    img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
    print("wrote", out)
