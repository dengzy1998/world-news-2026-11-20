#!/usr/bin/env python3
"""Draw v2 of the 20 November 2026 world-news front page.

One 1024x1024 newspaper page carrying 36 sourced stories from Friday
20 November 2026: a huge date masthead with an italic kicker, a region
tab strip whose counts are computed from the story ledger below, a
big-number stat strip, three illustrated lead cards, ten numbered grid
cards with small drawn art strips, a dotted world map with numbered
markers for stories 1-13, a two-column list of 23 further stories, a
DATE CHECK box naming Thursday stories deliberately excluded, and a
footer stating the one-day rule. The three lead illustrations are
AI-generated photo illustrations shipped in assets/ and disclosed in
the footer. Deterministic: running it twice writes identical bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
MX = 14                      # page margin
CW = W - 2 * MX              # content width

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_O = os.path.join(FONT_DIR, "DejaVuSerif.ttf")  # kicker: serif italic stand-in

PAPER = (247, 243, 233)
INK = (24, 24, 24)
RED = (176, 28, 40)
GREY = (92, 90, 84)
LIGHT = (196, 188, 164)
CARD_BG = (252, 250, 244)

REGION_COLOURS = {
    "EUROPE": (31, 58, 95),
    "ASIA-PACIFIC": (13, 110, 102),
    "AMERICAS": (140, 44, 62),
    "MIDEAST": (196, 110, 20),
    "AFRICA": (62, 120, 44),
    "OCEANIA": (96, 62, 140),
    "WORLD": (96, 96, 96),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def para(draw, text, fnt, x, y, max_width, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "...", font=fnt) > max_width:
            last = last[:-1]
        lines[-1] = last.rstrip() + "..."
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, text, fnt, y, fill=INK):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories

LEADS = [
    {
        "n": 1, "region": "ASIA-PACIFIC", "tag": "ODISHA - STORM",
        "img": "lead1_cyclone.jpg",
        "caption": "LANDFALL: 08:30 IST - GOPALPUR",
        "head": "Cyclone Akvan Comes Ashore Near Gopalpur",
        "body": ("Severe Cyclone Akvan made landfall at 08:30 IST, winds "
                 "70-80 km/h gusting to 90. Over 300,000 people were "
                 "moved and 423 rescue teams deployed on the "
                 "Andhra-Odisha coast. (IMD)"),
    },
    {
        "n": 2, "region": "EUROPE", "tag": "KYIV - WAR",
        "img": "lead2_kyiv.jpg",
        "caption": "KYIV: 01:25 LOCAL - 7 WAVES",
        "head": "Kyiv Hit by Seven Waves of Ballistic Missiles",
        "body": ("Russia fired about 30 ballistic missiles at Kyiv "
                 "overnight from 01:25 local, hitting energy and "
                 "transport sites. Fires in three districts; embassies "
                 "damaged; one killed. (UNN)"),
    },
    {
        "n": 3, "region": "WORLD", "tag": "ANTALYA - CLIMATE",
        "img": "lead3_cop.jpg",
        "caption": "ANTALYA - FINAL DAY, NO DEAL",
        "head": "COP31 Reaches Its Final Day With No Deal",
        "body": ("Talks ran into their final day with no deal: finance "
                 "and fossil-fuel wording unresolved, the draft dropped "
                 "the fossil-free phase-out, and a $120bn adaptation "
                 "fund stayed open. (UN News)"),
    },
]

# (number, region, tag, headline, body, art kind)
CARDS = [
    (4, "ASIA-PACIFIC", "SEOUL / TOKYO - MARKETS",
     "AI Sell-Off Sinks Asia Shares",
     "Asia's worst week since 2020: Nikkei -4.1%, KOSPI -4.7%, "
     "SoftBank -16% as AI stocks tumbled. (Reuters)", "chart"),
    (5, "WORLD", "MERCURY - SPACE",
     "BepiColombo Reaches Mercury",
     "ESA-JAXA probe ends its 6bn-mile, 8-year trip; orbit insertion "
     "follows on Saturday. (ESA, BBC)", "planet"),
    (6, "EUROPE", "BRUSSELS - EUROPE",
     "Burnham Holds First EU-UK Reset Summit",
     "Costa and von der Leyen host the new UK PM; closer carbon "
     "links eyed. (EU Council)", "flags"),
    (7, "ASIA-PACIFIC", "TOKYO - ECONOMY",
     "Japan Core Inflation Hits 2.2%",
     "October core CPI up; a BoJ hike eyed; yen at 155.50 to the "
     "dollar. (Reuters)", "rise"),
    (8, "ASIA-PACIFIC", "BEIJING - RATES",
     "China Holds Lending Rates for 18th Month",
     "One-year LPR held at 3.00%, five-year at 3.50%, as expected. "
     "(PBOC)", "bars"),
    (9, "OCEANIA", "WELLINGTON - CRICKET",
     "Phillips Makes History With 118",
     "First NZ batter with centuries in all formats vs India in a "
     "year; NZ 368. (ICC, AP)", "cricket"),
    (10, "AMERICAS", "SAN SALVADOR - POLITICS",
     "Bukele Files to Run for a Third Term",
     "Files for the February 2027 vote; rights groups object. "
     "(AP)", "year"),
    (11, "AFRICA", "SENEGAL - MIGRATION",
     "Migrant Boat Capsizes off Senegal",
     "Four bodies recovered amid a surge in departures. "
     "(Al Jazeera)", "boat"),
    (12, "EUROPE", "ROME - LABOUR",
     "Italy's CGIL Holds 24-Hour General Strike",
     "Unions rally in 100 squares against the 2027 budget. "
     "(CGIL, AFP)", "strike"),
    (13, "EUROPE", "BARCELONA - HEALTH",
     "Pancreatic Cancer Pill Shrinks Tumours 60.7%",
     "Daraxonrasib + chemo beats chemo alone in an early trial. "
     "(Reuters)", "pill"),
]

MORE = [
    (14, "AMERICAS", "Florida: St Johns River hits record 18.3 ft. (AP)"),
    (15, "AMERICAS", "Washington: Senate rejects Iran war-powers bid 51-48. (AP)"),
    (16, "AMERICAS", "Washington: Trump pardons Pete Rose posthumously. (AP)"),
    (17, "WORLD", "Games: GTA VI's first full day on sale. (Sensor Tower)"),
    (18, "MIDEAST", "Hormuz: Tanker afire after striking a mine. (Reuters)"),
    (19, "ASIA-PACIFIC", "Taipei: Taiwan acts to steady sliding stocks. (FSC)"),
    (20, "EUROPE", "Genoa: Drones close airport for four hours. (ANSA)"),
    (21, "AFRICA", "Ethiopia-Eritrea border build-up reported. (Monitors)"),
    (22, "MIDEAST", "Taiz: 'It isn't just fireworks,' families say. (BBC)"),
    (23, "AMERICAS", "Canada: Ottawa courts AI data centres. (Reuters)"),
    (24, "ASIA-PACIFIC", "Seoul: Ruling party moves to impeach top judge. (SBS)"),
    (25, "AMERICAS", "Cincinnati: Hippo Fiona dies after swallowing a hat. (Zoo)"),
    (26, "AMERICAS", "Los Angeles: Hyundai reveals 2027 Elantra. (Hyundai)"),
    (27, "EUROPE", "Turin: ATP Finals groups close. (ATP)"),
    (28, "ASIA-PACIFIC", "Jakarta: Asset-forfeiture bill passes. (Reuters)"),
    (29, "EUROPE", "London: UK, Norway fund 100m+ GBP Ukraine ships. (BBC)"),
    (30, "EUROPE", "Copenhagen: Greenland defence bill approved. (Ritzau)"),
    (31, "EUROPE", "Dublin: Harris seeks a border poll. (RTE)"),
    (32, "ASIA-PACIFIC", "Mumbai: Sensex flat; Nifty 25,199. (NSE)"),
    (33, "OCEANIA", "Sydney: ASX futures fall 1% as yen rises. (ASX)"),
    (34, "ASIA-PACIFIC", "New Delhi: Modi opens SCO civilisations forum. (PTI)"),
    (35, "AMERICAS", "Las Vegas: Mayweather faces felony charges. (Court)"),
    (36, "AMERICAS", "Washington: Trump defers Iran decision to 2027. (Fox News)"),
]

STATS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan"),
    ("~30", "ballistic missiles fired at Kyiv"),
    ("$120bn", "adaptation finance unresolved at COP31"),
    ("-7%", "Asia shares' worst week since 2020"),
    ("118", "Phillips' historic century in Wellington"),
    ("8 yrs", "BepiColombo's voyage to Mercury"),
]

DATE_CHECK_INTRO = ("First reported Thursday 19 Nov, so NOT shown here "
                    "as Friday's news:")
DATE_CHECK = [
    "the Trump-Xi-Putin Shenzhen summit itself",
    "Anthropic's $83 IPO pricing and Nasdaq debut",
    "the ICJ's Rohingya genocide judgment",
    "GTA VI's midnight launch",
    "the $190.4m Van Gogh sale",
    "the Crimean Bridge attack",
]

MARKERS = {
    1: (84.9, 19.3), 2: (30.5, 50.4), 3: (30.7, 36.9), 4: (126.9, 37.5),
    5: (8.6, 49.8), 6: (4.4, 50.9), 7: (139.7, 35.7), 8: (116.4, 39.9),
    9: (174.8, -41.3), 10: (-89.2, 13.7), 11: (-17.4, 14.7),
    12: (12.5, 41.9), 13: (2.2, 41.4),
}

LAND = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-76, 58), (-65, 45), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26),
     (-97, 22), (-94, 18), (-87, 15), (-83, 9), (-79, 9), (-85, 12),
     (-92, 15), (-97, 16), (-105, 20), (-110, 23), (-114, 28), (-117, 33),
     (-122, 37), (-124, 46), (-130, 55), (-152, 60), (-165, 60)],
    [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 82), (-55, 80),
     (-58, 76), (-55, 70), (-53, 64)],
    [(-79, 9), (-71, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-55, -33), (-62, -39),
     (-65, -45), (-67, -52), (-68, -55), (-71, -54), (-73, -46), (-73, -37),
     (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1),
     (-77, 4)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (35, 28),
     (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (48, 5), (42, -2),
     (40, -10), (38, -18), (35, -24), (32, -29), (26, -34), (19, -35),
     (17, -30), (15, -22), (13, -12), (12, -6), (9, -1), (9, 4), (-8, 4),
     (-13, 8), (-17, 15), (-16, 21), (-15, 27), (-10, 31)],
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 49), (2, 51),
     (5, 53), (8, 55), (8, 57), (5, 58), (5, 60), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 59), (26, 62), (22, 65), (25, 68), (32, 66),
     (35, 62), (32, 56), (30, 52), (28, 48), (28, 44), (24, 41), (23, 39),
     (21, 37), (19, 40), (16, 38), (14, 42), (12, 44), (8, 44), (4, 43),
     (2, 42), (0, 39), (-2, 37)],
    [(27, 41), (30, 41), (33, 42), (36, 45), (38, 50), (36, 56), (38, 62),
     (40, 67), (50, 69), (65, 69), (80, 70), (100, 72), (120, 73),
     (140, 72), (160, 70), (178, 66), (178, 63), (170, 60), (161, 58),
     (156, 52), (150, 48), (143, 45), (141, 40), (136, 35), (130, 33),
     (127, 38), (122, 38), (121, 32), (120, 28), (118, 24), (114, 22),
     (110, 20), (108, 13), (106, 8), (104, 3), (101, 6), (99, 9),
     (97, 16), (93, 20), (90, 22), (87, 21), (84, 19), (80, 14), (77, 8),
     (75, 12), (72, 19), (68, 23), (66, 25), (61, 25), (57, 26), (52, 28),
     (50, 29), (48, 30), (51, 24), (55, 24), (58, 22), (59, 22), (55, 17),
     (52, 15), (48, 14), (44, 12), (43, 14), (40, 20), (38, 25), (35, 29),
     (34, 31), (36, 36), (30, 36)],
    [(113, -21), (122, -17), (130, -12), (136, -12), (142, -11), (146, -15),
     (150, -22), (153, -28), (150, -37), (144, -38), (138, -35), (134, -33),
     (129, -32), (124, -33), (118, -35), (115, -33), (113, -26)],
]

BLOBS = [
    (-2, 53, 2.5, 3.5), (138, 37, 4, 3), (101, 0, 6, 2.5), (114, 1, 5, 4),
    (108, -7, 6, 1.5), (120, -2, 3, 3), (136, -4, 8, 3), (122, 13, 3, 5),
    (47, -19, 2.5, 5), (172, -42, 2, 3.5), (25, 35, 2, 1.5),
]


def region_counts():
    counts = {}
    for lead in LEADS:
        counts[lead["region"]] = counts.get(lead["region"], 0) + 1
    for card in CARDS:
        counts[card[1]] = counts.get(card[1], 0) + 1
    for item in MORE:
        counts[item[1]] = counts.get(item[1], 0) + 1
    return counts


def in_land(lon, lat):
    for poly in LAND:
        inside = False
        j = len(poly) - 1
        for i in range(len(poly)):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > lat) != (yj > lat)) and (
                    lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        if inside:
            return True
    for clon, clat, rx, ry in BLOBS:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
            return True
    return False


# ---------------------------------------------------------------- sections

def draw_masthead(draw):
    top = font(SANS_B, 10)
    centred(draw, "THE WORLD IN ONE DAY", top, 15, fill=INK)
    tf = font(SANS_B, 10)
    s = "FRIDAY'S NEWS - ONE PAGE - 36 STORIES"
    tw = draw.textlength(s, font=tf)
    draw.text((MX + CW - tw, 15), s, font=tf, fill=INK)
    title = font(SERIF_B, 44)
    centred(draw, "Friday 20 November 2026", title, 28)
    kick = font(SANS_O, 14)
    centred(draw, "A cyclone comes ashore in India - Missiles rain on "
                  "Kyiv - Climate talks reach their final day", kick, 80,
            fill=RED)
    rule(draw, MX, MX + CW, 102, 3)
    rule(draw, MX, MX + CW, 107, 1)


def draw_region_strip(draw, counts):
    order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA",
             "OCEANIA", "WORLD"]
    y = 113
    gap = 4
    fnt = font(SANS_B, 10)
    labels = ["%s %d" % (name, counts.get(name, 0)) for name in order]
    widths = [draw.textlength(t, font=fnt) + 16 for t in labels]
    x = MX
    for name, label, wdt in zip(order, labels, widths):
        draw.rectangle([x, y, x + wdt, y + 19], fill=REGION_COLOURS[name])
        tw = draw.textlength(label, font=fnt)
        draw.text((x + (wdt - tw) / 2, y + 4), label, font=fnt,
                  fill=(255, 255, 255))
        x += wdt + gap
    line = font(SANS_B, 9)
    s = "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE"
    tw = draw.textlength(s, font=line)
    draw.text((MX + CW - tw, y + 5), s, font=line, fill=GREY)


def draw_stats(draw):
    y = 140
    gap = 6
    bw = (CW - gap * 5) / 6
    big = font(SERIF_B, 21)
    small = font(SANS, 8)
    for i, (num, label) in enumerate(STATS):
        x = MX + i * (bw + gap)
        tw = draw.textlength(num, font=big)
        draw.text((x + (bw - tw) / 2, y), num, font=big, fill=RED)
        lines = wrap(draw, label, small, bw - 6)
        ly = y + 26
        for ln in lines[:2]:
            tw = draw.textlength(ln, font=small)
            draw.text((x + (bw - tw) / 2, ly), ln, font=small, fill=INK)
            ly += 10
    rule(draw, MX, MX + CW, y + 48, 1, fill=LIGHT)


def draw_leads(draw, img):
    y = 196
    gap = 8
    bw = (CW - gap * 2) / 3
    img_h = 98
    for i, lead in enumerate(LEADS):
        x = MX + i * (bw + gap)
        col = REGION_COLOURS[lead["region"]]
        draw.rectangle([x, y, x + bw, y + 234], fill=CARD_BG,
                       outline=LIGHT, width=1)
        draw.rectangle([x, y, x + bw, y + 5], fill=col)
        draw.rectangle([x + 6, y + 10, x + 30, y + 32], fill=RED)
        nf = font(SANS_B, 15)
        s = str(lead["n"])
        tw = draw.textlength(s, font=nf)
        draw.text((x + 18 - tw / 2, y + 12), s, font=nf,
                  fill=(255, 255, 255))
        tf = font(SANS_B, 11)
        draw.text((x + 36, y + 15), lead["tag"], font=tf, fill=col)
        try:
            im = Image.open(os.path.join(ASSETS, lead["img"])).convert("RGB")
            im = im.resize((int(bw) - 12, img_h))
            img.paste(im, (int(x + 6), y + 36))
        except Exception:
            draw.rectangle([x + 6, y + 36, x + bw - 6, y + 36 + img_h],
                           fill=(210, 205, 190))
        draw.rectangle([x + 6, y + 36 + img_h, x + bw - 6, y + 50 + img_h],
                       fill=INK)
        cap = font(SANS_B, 8)
        tw = draw.textlength(lead["caption"], font=cap)
        draw.text((x + 6 + (bw - 12 - tw) / 2, y + 39 + img_h),
                  lead["caption"], font=cap, fill=(255, 255, 255))
        hy = para(draw, lead["head"], font(SERIF_B, 15), x + 6, y + 156,
                  bw - 12, 18, max_lines=2)
        para(draw, lead["body"], font(SANS, 9), x + 6, hy + 2, bw - 12, 12,
             fill=(50, 50, 48), max_lines=4)


def draw_card_art(draw, kind, x0, y0, x1, y1):
    """Small flat art strip for a grid card, drawn with simple shapes."""
    mid = (y0 + y1) / 2
    if kind == "chart":
        draw.rectangle([x0, y0, x1, y1], fill=(24, 24, 32))
        pts = [(x0 + 14, mid - 6), (x0 + 52, mid - 2), (x0 + 90, mid + 3),
               (x0 + 128, mid + 8), (x0 + 166, y1 - 5)]
        draw.line(pts, fill=RED, width=3)
        for px, py in pts:
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    elif kind == "planet":
        draw.rectangle([x0, y0, x1, y1], fill=(10, 10, 26))
        draw.ellipse([x1 - 52, y0 + 3, x1 - 8, y1 - 3], fill=(178, 172, 160))
        draw.ellipse([x0 + 16, mid - 3, x0 + 22, mid + 3],
                     fill=(240, 200, 90))
        draw.arc([x0 + 8, y0 - 8, x1 - 30, y1 + 10], 200, 320,
                 fill=(200, 200, 210), width=2)
    elif kind == "flags":
        draw.rectangle([x0, y0, x1, y1], fill=(24, 48, 96))
        for a in range(8):
            import math
            ang = a * 3.14159 / 4
            sx = x0 + 34 + 15 * math.cos(ang)
            sy = mid + 8 * math.sin(ang)
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 213, 0))
        draw.rectangle([x0 + 78, y0 + 5, x0 + 122, y1 - 5],
                       fill=(255, 255, 255), outline=INK, width=1)
        draw.rectangle([x0 + 97, y0 + 5, x0 + 103, y1 - 5], fill=RED)
        draw.rectangle([x0 + 78, mid - 3, x0 + 122, mid + 3], fill=RED)
        draw.rectangle([x0 + 140, y0 + 5, x0 + 184, y1 - 5],
                       fill=(0, 91, 187))
        draw.rectangle([x0 + 140, mid, x0 + 184, y1 - 5], fill=(255, 213, 0))
    elif kind == "rise":
        draw.rectangle([x0, y0, x1, y1], fill=(240, 238, 228))
        f = font(SANS_B, 13)
        draw.text((x0 + 10, mid - 8), "2.2%", font=f, fill=RED)
        pts = [(x0 + 70, y1 - 6), (x0 + 105, mid + 2), (x0 + 140, mid - 3),
               (x0 + 178, y0 + 5)]
        draw.line(pts, fill=RED, width=3)
    elif kind == "bars":
        draw.rectangle([x0, y0, x1, y1], fill=(120, 22, 30))
        f = font(SANS_B, 11)
        draw.text((x0 + 14, mid - 7), "1-YR  3.00%", font=f,
                  fill=(255, 255, 255))
        draw.text((x0 + 108, mid - 7), "5-YR  3.50%", font=f,
                  fill=(255, 255, 255))
    elif kind == "cricket":
        draw.rectangle([x0, y0, x1, y1], fill=(34, 110, 54))
        f = font(SERIF_B, 17)
        draw.text((x0 + 12, mid - 10), "118", font=f, fill=(255, 255, 255))
        draw.rectangle([x0 + 76, y0 + 4, x0 + 84, y1 - 4],
                       fill=(222, 200, 140))
        draw.ellipse([x0 + 130, mid - 9, x0 + 148, mid + 9], fill=RED)
    elif kind == "year":
        draw.rectangle([x0, y0, x1, y1], fill=(28, 40, 74))
        f = font(SERIF_B, 16)
        s = "2027"
        tw = draw.textlength(s, font=f)
        draw.text(((x0 + x1 - tw) / 2, mid - 9), s, font=f,
                  fill=(255, 255, 255))
    elif kind == "boat":
        draw.rectangle([x0, y0, x1, y1], fill=(40, 100, 150))
        draw.polygon([(x0 + 70, mid + 2), (x0 + 122, mid + 2),
                      (x0 + 112, y1 - 4), (x0 + 80, y1 - 4)],
                     fill=(90, 60, 30))
        draw.polygon([(x0 + 94, mid + 1), (x0 + 94, y0 + 5),
                      (x0 + 110, mid + 1)], fill=(240, 240, 230))
        draw.line([(x0 + 8, y1 - 4), (x0 + 60, y1 - 4)], fill=(255, 255, 255),
                  width=2)
        draw.line([(x0 + 140, y1 - 4), (x0 + 186, y1 - 4)],
                  fill=(255, 255, 255), width=2)
    elif kind == "strike":
        draw.rectangle([x0, y0, x1, y1], fill=(150, 30, 36))
        f = font(SANS_B, 12)
        draw.rectangle([x0 + 18, y0 + 5, x0 + 74, y1 - 5],
                       fill=(255, 255, 255))
        tw = draw.textlength("CGIL", font=f)
        draw.text((x0 + 46 - tw / 2, mid - 7), "CGIL", font=f, fill=RED)
        draw.rectangle([x0 + 118, y0 + 5, x0 + 174, y1 - 5],
                       fill=(255, 255, 255))
        tw = draw.textlength("24H", font=f)
        draw.text((x0 + 146 - tw / 2, mid - 7), "24H", font=f, fill=RED)
    elif kind == "pill":
        draw.rectangle([x0, y0, x1, y1], fill=(238, 236, 230))
        draw.rounded_rectangle([x0 + 52, mid - 9, x0 + 118, mid + 9],
                               radius=9, fill=RED)
        draw.rounded_rectangle([x0 + 85, mid - 9, x0 + 118, mid + 9],
                               radius=9, fill=(245, 245, 245), outline=RED,
                               width=2)
        f = font(SANS_B, 12)
        draw.text((x0 + 132, mid - 7), "60.7%", font=f, fill=RED)


def draw_cards(draw):
    y = 438
    gap = 6
    cols = 5
    bw = (CW - gap * (cols - 1)) / cols
    bh = 106
    hf = font(SERIF_B, 11)
    bf = font(SANS, 8)
    tf = font(SANS_B, 7)
    for idx, (n, region, tag, head, body, art) in enumerate(CARDS):
        r, c = divmod(idx, cols)
        x = MX + c * (bw + gap)
        yy = y + r * (bh + 6)
        col = REGION_COLOURS[region]
        draw.rectangle([x, yy, x + bw, yy + bh], fill=CARD_BG,
                       outline=LIGHT, width=1)
        draw_card_art(draw, art, x + 1, yy + 1, x + bw - 1, yy + 27)
        draw.rectangle([x + 5, yy + 31, x + 21, yy + 45], fill=RED)
        nf = font(SANS_B, 10)
        s = str(n)
        tw = draw.textlength(s, font=nf)
        draw.text((x + 13 - tw / 2, yy + 32), s, font=nf,
                  fill=(255, 255, 255))
        draw.text((x + 25, yy + 34), tag, font=tf, fill=col)
        hy = para(draw, head, hf, x + 5, yy + 48, bw - 10, 13, max_lines=2)
        para(draw, body, bf, x + 5, hy + 1, bw - 10, 10,
             fill=(50, 50, 48), max_lines=3)


def draw_map(draw, x0, y0, x1):
    title = font(SANS_B, 12)
    draw.text((x0, y0), "WHERE IT HAPPENED", font=title, fill=INK)
    my0, my1 = y0 + 18, y0 + 148
    draw.rectangle([x0, my0, x1, my1], fill=(26, 48, 74))
    step = 5
    dot = (214, 222, 228)
    for gx in range(int(x0) + 4, int(x1) - 2, step):
        lon = -180 + (gx - x0) / (x1 - x0) * 360
        for gy in range(int(my0) + 4, int(my1) - 2, step):
            lat = 85 - (gy - my0) / (my1 - my0) * 170
            if in_land(lon, lat):
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=dot)
    mf = font(SANS_B, 8)
    offsets = {5: (10, -12), 6: (-14, -10), 13: (-16, 6), 12: (8, 8),
               3: (10, 8), 2: (6, -14), 7: (12, -4), 4: (-4, -16)}
    for n, (lon, lat) in MARKERS.items():
        gx = x0 + (lon + 180) / 360 * (x1 - x0)
        gy = my0 + (85 - lat) / 170 * (my1 - my0)
        dx, dy = offsets.get(n, (0, 0))
        gx, gy = gx + dx, gy + dy
        draw.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=RED,
                     outline=(255, 255, 255), width=1)
        s = str(n)
        tw = draw.textlength(s, font=mf)
        draw.text((gx - tw / 2, gy - 4), s, font=mf, fill=(255, 255, 255))
    cap = font(SANS, 8)
    para(draw, "Red numbers mark stories 1-13. Positions are approximate. "
               "5 is Mercury, marked at ESA, Darmstadt.", cap, x0, my1 + 5,
         x1 - x0, 10, fill=GREY, max_lines=2)


def draw_more(draw, x0, y0, x1):
    tf = font(SANS_B, 12)
    draw.text((x0, y0), "ALSO ON FRIDAY 20 NOVEMBER - 23 MORE STORIES",
              font=tf, fill=INK)
    rule(draw, x0, x1, y0 + 17, 2)
    fnt = font(SANS, 8)
    nf = font(SANS_B, 8)
    col_w = (x1 - x0 - 14) / 2
    half = (len(MORE) + 1) // 2
    for ci, chunk in enumerate([MORE[:half], MORE[half:]]):
        x = x0 + ci * (col_w + 14)
        yy = y0 + 23
        for n, region, text in chunk:
            draw.text((x, yy), "%d" % n, font=nf, fill=RED)
            para(draw, text, fnt, x + 17, yy, col_w - 17, 10,
                 fill=(40, 40, 38), max_lines=2)
            yy += 12


def draw_date_check(draw):
    y = 862
    draw.rectangle([MX, y, MX + CW, y + 76], fill=(243, 236, 220),
                   outline=RED, width=2)
    tf = font(SANS_B, 12)
    draw.text((MX + 8, y + 7), "DATE CHECK", font=tf, fill=RED)
    body = DATE_CHECK_INTRO + " " + " - ".join(DATE_CHECK) + "."
    para(draw, body, font(SANS, 10), MX + 8, y + 26, CW - 16, 14,
         fill=(50, 48, 44), max_lines=3)


def draw_footer(draw):
    y = 954
    rule(draw, MX, MX + CW, y, 2)
    f1 = font(SANS, 8)
    centred(draw, "Every story here happened, or was first reported, on "
                  "Friday 20 November 2026 in at least one time zone. "
                  "Disputed claims are attributed, not stated as fact.",
            f1, y + 6)
    centred(draw, "Sources: IMD, UNN, UN News, Reuters, ESA, BBC, EU "
                  "Council, PBOC, ICC, AP, AFP, Al Jazeera, CGIL, ANSA, "
                  "FSC, SBS, NSE, ASX, PTI, RTE, Ritzau, UNN and the "
                  "outlets named in each story.", f1, y + 18, fill=GREY)
    centred(draw, "Photos: AI-generated photo illustrations. Compiled "
                  "20 Nov 2026 - one image, one day.", f1, y + 30,
            fill=GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, 1017, 1017], outline=INK, width=2)
    draw.rectangle([10, 10, 1013, 1013], outline=LIGHT, width=1)
    counts = region_counts()
    assert sum(counts.values()) == 36, counts
    draw_masthead(draw)
    draw_region_strip(draw, counts)
    draw_stats(draw)
    draw_leads(draw, img)
    draw = ImageDraw.Draw(img)
    draw_cards(draw)
    draw_map(draw, MX, 668, 344)
    draw_more(draw, 358, 668, MX + CW)
    draw_date_check(draw)
    draw_footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
