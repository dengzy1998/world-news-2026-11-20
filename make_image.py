#!/usr/bin/env python3
"""Draw the front page of FRIDAY'S WORLD for 20 November 2026.

A single 1024x1024 newspaper page, drawn entirely with Pillow shapes and
text: masthead, a lead story on the Iran decision, a big cyclone picture
story, a Ukraine talks story, and four smaller picture stories. The
drawing is fully deterministic -- running it twice writes identical bytes.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (178, 32, 44)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
GREY = (90, 90, 86)
LIGHT_LINE = (180, 172, 150)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines = []
    current = ""
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


def para(draw, text, fnt, x, y, max_width, leading, fill=INK):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def double_rule(draw, x0, x1, y, fill=INK):
    rule(draw, x0, x1, y, 3, fill)
    rule(draw, x0, x1, y + 5, 1, fill)


def kicker(draw, x, y, text, fill=RED, size=14):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + size + 6


def headline(draw, text, fnt, x, y, max_width, leading):
    return para(draw, text, fnt, x, y, max_width, leading)


def draw_masthead(draw):
    title = font(SERIF_B, 64)
    tw = draw.textlength("FRIDAY'S WORLD", font=title)
    draw.text(((W - tw) / 2, 30), "FRIDAY'S WORLD", font=title, fill=INK)
    tag = font(SERIF, 16)
    tag_text = "The world in one page"
    tw = draw.textlength(tag_text, font=tag)
    draw.text(((W - tw) / 2, 104), tag_text, font=tag, fill=GREY)
    double_rule(draw, 26, 998, 128)
    left = font(SANS_B, 17)
    draw.text((28, 140), "FRIDAY 20 NOVEMBER 2026", font=left, fill=INK)
    right = font(SANS, 14)
    rt = "SEVEN STORIES  •  ONE DAY"
    tw = draw.textlength(rt, font=right)
    draw.text((998 - tw, 142), rt, font=right, fill=GREY)
    double_rule(draw, 26, 998, 166)


def draw_calendar(draw, x0, y0, x1, y1):
    """A desk-calendar page for January 2027 with the 1st circled."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.rounded_rectangle([x0, y0, x1, y0 + 34], radius=10, fill=NAVY)
    draw.rectangle([x0, y0 + 22, x1, y0 + 34], fill=NAVY)
    head = font(SANS_B, 16)
    ht = "JANUARY 2027"
    tw = draw.textlength(ht, font=head)
    draw.text(((x0 + x1 - tw) / 2, y0 + 7), ht, font=head, fill=(255, 255, 255))
    day_f = font(SANS_B, 12)
    num_f = font(SANS, 13)
    cols = ["M", "T", "W", "T", "F", "S", "S"]
    cw = (x1 - x0 - 16) / 7
    for i, d in enumerate(cols):
        cx = x0 + 8 + i * cw + cw / 2
        tw = draw.textlength(d, font=day_f)
        draw.text((cx - tw / 2, y0 + 40), d, font=day_f, fill=GREY)
    # 1 January 2027 is a Friday: first row holds 1 (Fri) and 2 (Sat), 3 (Sun).
    days = [None, None, None, None, 1, 2, 3]
    for r in range(5):
        for c in range(7):
            idx = r * 7 + c
            if idx < len(days):
                n = days[idx]
            else:
                n = idx - 3
            if n is None or n > 31:
                continue
            cx = x0 + 8 + c * cw + cw / 2
            cy = y0 + 58 + r * 16
            s = str(n)
            tw = draw.textlength(s, font=num_f)
            draw.text((cx - tw / 2, cy), s, font=num_f, fill=INK)
            if n == 1:
                draw.ellipse([cx - 13, cy - 3, cx + 13, cy + 16],
                             outline=RED, width=3)


def draw_lead(draw):
    y = kicker(draw, 28, 178, "WASHINGTON  —  THE WHITE HOUSE")
    y = headline(draw, "TRUMP PUTS IRAN DECISION OFF TO 2027",
                 font(SERIF_B, 37), 28, y, 560, 44)
    sub = ("\"We'll see what happens after January 1,\" Trump tells "
           "Fox News — pushing any decision on Iran into next year.")
    para(draw, sub, font(SERIF, 16), 28, y + 8, 560, 22, fill=(60, 60, 60))
    draw_calendar(draw, 620, 178, 996, 322)
    rule(draw, 26, 998, 336, 2)

def draw_cyclone(draw, x0, y0, x1, y1):
    """Severe Cyclone Akvan spiralling over the Bay of Bengal toward Odisha."""
    # Sea: horizontal bands, deep to pale.
    sea_top = (46, 109, 164)
    sea_bot = (126, 179, 213)
    bands = 12
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(sea_top[j] + (sea_bot[j] - sea_top[j]) * t)
                    for j in range(3))
        yy0 = y0 + (y1 - y0) * i // bands
        yy1 = y0 + (y1 - y0) * (i + 1) // bands
        draw.rectangle([x0, yy0, x1, yy1], fill=col)
    # Land: India's east coast on the right, a simple diagonal shoreline.
    coast = [(x1, y0), (x1, y1), (x1 - 118, y1), (x1 - 138, y1 - 90),
             (x1 - 108, y1 - 170), (x1 - 128, y0)]
    draw.polygon(coast, fill=(217, 195, 154))
    draw.polygon([(x1 - 138, y1 - 90), (x1 - 108, y1 - 170), (x1 - 128, y0),
                  (x1, y0), (x1, y1 - 46), (x1 - 118, y1 - 46)],
                 fill=(150, 178, 120))
    # Spiral arms around the eye, left of centre, kept inside the box.
    cx, cy = x0 + 185, y0 + 128
    for r, start, end in [(24, 0, 300), (44, 120, 420), (64, 200, 500),
                          (84, 280, 580), (104, 20, 320), (122, 150, 420)]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, end,
                 fill=(255, 255, 255), width=8)
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16],
                 fill=(255, 255, 255), outline=NAVY, width=2)
    # Landfall arrow from the eye toward Gopalpur on the coast.
    draw.line([(cx + 26, cy + 8), (x1 - 132, y1 - 96)], fill=RED, width=5)
    draw.polygon([(x1 - 132, y1 - 96), (x1 - 154, y1 - 102), (x1 - 140, y1 - 78)],
                 fill=RED)
    lab = font(SANS_B, 14)
    lg = "GOPALPUR"
    tw = draw.textlength(lg, font=lab)
    lx, ly = x1 - 226, y1 - 116
    draw.rectangle([lx - 6, ly - 4, lx + tw + 6, ly + 18],
                   fill=(255, 255, 255), outline=RED, width=2)
    draw.text((lx, ly), lg, font=lab, fill=RED)
    sea = font(SERIF, 15)
    draw.text((x0 + 14, y1 - 30), "Bay of Bengal", font=sea,
              fill=(255, 255, 255))
    tag = font(SANS_B, 13)
    tg = "GUSTS 110 km/h"
    tw = draw.textlength(tg, font=tag)
    draw.rectangle([x0 + 10, y0 + 10, x0 + 22 + tw, y0 + 34], fill=RED)
    draw.text((x0 + 16, y0 + 14), tg, font=tag, fill=(255, 255, 255))


def draw_hero(draw):
    draw_cyclone(draw, 28, 348, 560, 606)
    y = kicker(draw, 580, 348, "INDIA  —  BAY OF BENGAL")
    y = headline(draw, "AKVAN SLAMS INTO ODISHA",
                 font(SERIF_B, 31), 580, y, 418, 38)
    body = ("Severe Cyclone Akvan crosses the coast near Gopalpur "
            "around noon, with sustained winds of 90-100 km/h. "
            "Nearly 300,000 people were moved to 9,341 shelters, "
            "423 rescue teams are on the ground and 69 trains "
            "cancelled.")
    para(draw, body, font(SERIF, 15), 580, y + 10, 418, 21,
         fill=(60, 60, 60))
    rule(draw, 26, 998, 618, 2)


def draw_talks(draw, x0, y0, x1, y1):
    """Three flags over a round negotiating table."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 245))
    # Flag poles and flags: EU, Ukraine, Russia.
    flags = [
        ("EU", (0, 51, 153), None),
        ("UA", (0, 91, 187), (255, 213, 0)),
        ("RU", (255, 255, 255), (0, 57, 166)),
    ]
    fw, fh = 92, 56
    gap = (x1 - x0 - 3 * fw) // 4
    for i, (code, top, bot) in enumerate(flags):
        fx = x0 + gap + i * (fw + gap)
        fy = y0 + 22
        draw.line([(fx + fw // 2, fy + fh), (fx + fw // 2, fy + fh + 30)],
                  fill=INK, width=3)
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
        if code == "EU":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=top)
            for a in range(12):
                ang = math.radians(a * 30 - 90)
                sx = fx + fw // 2 + 26 * math.cos(ang)
                sy = fy + fh // 2 + 16 * math.sin(ang)
                draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                             fill=(255, 213, 0))
        elif code == "UA":
            draw.rectangle([fx, fy, fx + fw, fy + fh // 2], fill=top)
            draw.rectangle([fx, fy + fh // 2, fx + fw, fy + fh], fill=bot)
        else:
            draw.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=top)
            draw.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3],
                           fill=(0, 57, 166))
            draw.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh],
                           fill=(213, 0, 0))
    # Round table with papers.
    draw.ellipse([x0 + 90, y1 - 52, x1 - 90, y1 - 8], fill=(122, 84, 52),
                 outline=INK, width=2)
    draw.rectangle([x0 + 130, y1 - 26, x0 + 190, y1 - 12], fill=(255, 255, 255),
                   outline=GREY)
    draw.rectangle([x1 - 190, y1 - 26, x1 - 130, y1 - 12], fill=(255, 255, 255),
                   outline=GREY)


def draw_ukraine(draw):
    y = kicker(draw, 28, 630, "UKRAINE  —  PEACE TALKS")
    y = headline(draw, "EUROPE READY FOR UKRAINE TALKS",
                 font(SERIF_B, 27), 28, y, 520, 33)
    body = ("Chancellor Merz says Europe expects a seat at new talks "
            "to end the war \"soon\". US envoy Kushner says Russia is "
            "open to NATO-style security guarantees for Kyiv.")
    para(draw, body, font(SERIF, 15), 28, y + 8, 520, 21,
         fill=(60, 60, 60))
    draw_talks(draw, 580, 630, 996, 790)
    rule(draw, 26, 998, 802, 2)

def draw_hayabusa(draw, x0, y0, x1, y1):
    """Hayabusa2 in deep space, its asteroid target out of reach."""
    draw.rectangle([x0, y0, x1, y1], fill=(8, 10, 24))
    rng = random.Random(20261120)
    for _ in range(26):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y1 - 4)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # Asteroid, bottom right.
    ax, ay = x1 - 52, y1 - 34
    draw.polygon([(ax - 34, ay - 6), (ax - 12, ay - 22), (ax + 16, ay - 16),
                  (ax + 34, ay + 2), (ax + 20, ay + 20), (ax - 8, ay + 24),
                  (ax - 30, ay + 12)], fill=(150, 148, 140),
                 outline=(110, 108, 100))
    draw.ellipse([ax - 8, ay - 8, ax + 4, ay + 4], fill=(110, 108, 100))
    draw.ellipse([ax + 10, ay + 6, ax + 18, ay + 14], fill=(110, 108, 100))
    # Probe, top left, with solar panels and a dashed path bending away.
    px, py = x0 + 46, y0 + 30
    draw.rectangle([px - 9, py - 7, px + 9, py + 7], fill=(212, 175, 55),
                   outline=INK)
    draw.rectangle([px - 34, py - 4, px - 11, py + 4], fill=(40, 90, 180),
                   outline=(255, 255, 255))
    draw.rectangle([px + 11, py - 4, px + 34, py + 4], fill=(40, 90, 180),
                   outline=(255, 255, 255))
    draw.line([(px, py - 7), (px, py - 18)], fill=(255, 255, 255), width=2)
    for i in range(6):
        t = i / 5
        dx = int(px + 10 + t * 90)
        dy = int(py + 26 + t * t * 40)
        draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 255, 255))
    lab = font(SANS_B, 12)
    draw.text((x0 + 8, y1 - 18), "2015BM510", font=lab, fill=(255, 255, 255))


def draw_riyadh(draw, x0, y0, x1, y1):
    """Riyadh at dusk: skyline, a tall tower, smoke over the city."""
    for i in range(6):
        t = i / 5
        col = tuple(int((250, 160, 90)[j] + ((90, 60, 120)[j] - (250, 160, 90)[j]) * t)
                    for j in range(3))
        yy0 = y0 + (y1 - y0) * i // 6
        yy1 = y0 + (y1 - y0) * (i + 1) // 6
        draw.rectangle([x0, yy0, x1, yy1], fill=col)
    draw.ellipse([x1 - 46, y0 + 8, x1 - 16, y0 + 38], fill=(255, 214, 140))
    # Skyline.
    base = y1
    for bx, bw, bh in [(0, 34, 34), (38, 26, 48), (68, 30, 28), (102, 24, 40),
                       (170, 30, 30), (204, 26, 44)]:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base],
                       fill=(52, 40, 66))
    # Tall tower with an arched crown, right of centre.
    tx = x0 + 138
    draw.rectangle([tx, y0 + 22, tx + 26, base], fill=(52, 40, 66))
    draw.polygon([(tx, y0 + 22), (tx + 13, y0 + 4), (tx + 26, y0 + 22)],
                 fill=(52, 40, 66))
    draw.rectangle([tx + 8, y0 + 26, tx + 18, y0 + 44], fill=(250, 200, 120))
    # Smoke plume rising from a low building, right of the label.
    for i, (sx, sy, sr) in enumerate([(x0 + 92, y1 - 52, 7),
                                      (x0 + 98, y1 - 66, 9),
                                      (x0 + 106, y1 - 80, 11)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(120, 116, 112))
    lab = font(SANS_B, 12)
    draw.text((x0 + 8, y0 + 8), "RIYADH", font=lab, fill=(255, 255, 255))


def draw_meta(draw, x0, y0, x1, y1):
    """A blue panel with an infinity loop and a green leaf."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=(0, 98, 204))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    inf = font(SANS_B, 52)
    it = "\u221e"
    tw = draw.textlength(it, font=inf)
    draw.text((cx - tw / 2, cy - 30), it, font=inf, fill=(255, 255, 255))
    # Green leaf, bottom right.
    lx, ly = x1 - 34, y1 - 26
    draw.ellipse([lx - 14, ly - 8, lx + 14, ly + 8], fill=(60, 180, 90))
    draw.line([(lx - 14, ly + 8), (lx + 14, ly - 8)], fill=(30, 120, 50),
              width=2)
    lab = font(SANS_B, 13)
    draw.text((x0 + 10, y0 + 8), "2030 ?", font=lab, fill=(255, 255, 255))


def draw_fiona(draw, x0, y0, x1, y1):
    """Fiona the hippo in her pool, a small hat floating nearby."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=(178, 214, 230))
    # Pool water, lower half.
    draw.rectangle([x0, y0 + 52, x1, y1], fill=(90, 160, 200))
    draw.line([(x0, y0 + 52), (x1, y0 + 52)], fill=(255, 255, 255), width=2)
    # Hippo: body and head above the waterline.
    draw.ellipse([x0 + 52, y0 + 34, x0 + 178, y0 + 78], fill=(148, 140, 132))
    draw.ellipse([x0 + 150, y0 + 12, x0 + 214, y0 + 66], fill=(160, 152, 144))
    draw.ellipse([x0 + 158, y0 + 8, x0 + 172, y0 + 22], fill=(160, 152, 144))
    draw.ellipse([x0 + 188, y0 + 8, x0 + 202, y0 + 22], fill=(160, 152, 144))
    draw.ellipse([x0 + 196, y0 + 44, x0 + 214, y0 + 60], fill=(128, 120, 112))
    draw.ellipse([x0 + 164, y0 + 26, x0 + 172, y0 + 34], fill=INK)
    draw.ellipse([x0 + 200, y0 + 48, x0 + 205, y0 + 53], fill=INK)
    draw.ellipse([x0 + 208, y0 + 48, x0 + 213, y0 + 53], fill=INK)
    # The swallowed hat, floating.
    hx, hy = x0 + 22, y0 + 68
    draw.polygon([(hx, hy - 10), (hx + 9, hy - 17), (hx + 18, hy - 10),
                  (hx + 18, hy - 5), (hx, hy - 5)], fill=(120, 72, 20))
    draw.rectangle([hx - 7, hy - 5, hx + 25, hy], fill=(120, 72, 20))


GRID = [
    ("JAPAN'S PROBE LOSES ITS ASTEROID",
     "Engine failure forces Hayabusa2 off course; JAXA retargets it "
     "to asteroid 2015BM510 in 2028.",
     draw_hayabusa),
    ("HOUTHI STRIKE DAMAGES RIYADH TOWER",
     "A tower in the Saudi capital is damaged as new attacks are "
     "reported.",
     draw_riyadh),
    ("META RETHINKS NET ZERO 2030",
     "The company says it is re-evaluating its climate target as "
     "its AI buildout grows.",
     draw_meta),
    ("FIONA THE HIPPO DIES",
     "The zoo favourite dies after vets fail to remove a hat "
     "she swallowed.",
     draw_fiona),
]


def draw_grid(draw):
    col_w = 233
    gap = 8
    y = 812
    for i, (head, cap, painter) in enumerate(GRID):
        x0 = 28 + i * (col_w + gap)
        x1 = x0 + col_w
        painter(draw, x0, y, x1, y + 92)
        hy = para(draw, head, font(SANS_B, 14), x0, y + 100, col_w, 18)
        para(draw, cap, font(SANS, 12), x0, hy + 2, col_w, 16,
             fill=(60, 60, 60))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 12, 1011, 1011], outline=INK, width=2)
    draw.rectangle([18, 18, 1005, 1005], outline=LIGHT_LINE, width=1)
    draw_masthead(draw)
    draw_lead(draw)
    draw_hero(draw)
    draw_ukraine(draw)
    draw_grid(draw)
    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
