#!/usr/bin/env python3
"""Render the front page for 'Saturday 21 November 2026 — The World in One Page'.

Draws a dense broadsheet front page (1024x1024 PNG) with PIL: masthead, stat strip,
region bar, 3 lead stories with flat vector illustrations, 10 pictured stories,
a world map with numbered pins, 22 more one-line stories, a DATE CHECK box and a
sources footer. Every story is one of the 35 dated stories of Saturday 21 November
2026 (see SOURCES.md for the list and the top-20 consensus it follows).

Run:  python3 tools/render.py   (writes entry.png next to main.ts)
Requires: Pillow + Liberation/DejaVu fonts (standard on this machine).
The committed entry.png is what main.ts copies to /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# --- palette: cream paper, ink navy, brick red, teal accent -----------------
PAPER = (247, 241, 227)
INK = (27, 42, 74)
RED = (179, 53, 43)
RED_DK = (140, 36, 28)
TEAL = (14, 124, 123)
CREAM2 = (238, 231, 214)
GREY = (107, 107, 107)
LINE = (27, 42, 74)
SKY = (191, 227, 224)
GOLD = (245, 166, 35)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading, max_lines=None):
    """Draw wrapped text; returns y after the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, x, y, label, fill):
    """Small status badge (CONFIRMED / OFFICIAL / REPORTED / CLAIM)."""
    f = font(SANS_B, 9)
    w = draw.textlength(label, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- illustration helpers (flat vector style, drawn in code) ---------------
def draw_globe_thermo(d, x, y, w, h):
    """COP31 panel: globe + thermometer + clock on pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=(213, 236, 232))
    cx, cy, r = x + 62, y + 62, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 205),
              outline=(27, 42, 74), width=2)
    d.ellipse([cx - 22, cy - 26, cx - 2, cy - 6], fill=(110, 190, 120))
    d.ellipse([cx - 4, cy + 8, cx + 20, cy + 28], fill=(110, 190, 120))
    d.ellipse([cx + 12, cy - 22, cx + 26, cy - 8], fill=(110, 190, 120))
    # thermometer
    tx = x + 148
    d.rounded_rectangle([tx, y + 18, tx + 14, y + 88], radius=7,
                        fill=(255, 255, 255), outline=(179, 53, 43), width=2)
    d.ellipse([tx - 6, y + 82, tx + 20, y + 104], fill=(179, 53, 43))
    d.rectangle([tx + 4, y + 34, tx + 10, y + 88], fill=(179, 53, 43))
    # clock
    ccx, ccy, cr = x + 232, y + 58, 30
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(255, 255, 255),
              outline=(27, 42, 74), width=2)
    d.line([(ccx, ccy), (ccx, ccy - 20)], fill=(27, 42, 74), width=3)
    d.line([(ccx, ccy), (ccx + 14, ccy + 6)], fill=(27, 42, 74), width=3)


def draw_riyadh_night(d, x, y, w, h):
    """Riyadh panel: night skyline, missile trails, starbursts."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 52))
    d.ellipse([x + w - 52, y + 12, x + w - 26, y + 38], fill=(247, 241, 227))
    import math
    for bx, bw, bh in [(0, 46, 58), (52, 34, 84), (92, 52, 66), (150, 30, 92),
                       (186, 44, 60), (236, 36, 78), (278, 30, 54)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(27, 42, 74))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 4, 12):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(245, 166, 35))
    # missile trails: dotted arcs
    for (x0, y0, x1, y1, n) in [(30, 96, 150, 18, 14), (150, 100, 260, 26, 14)]:
        for i in range(n + 1):
            t = i / n
            px = x + x0 + (x1 - x0) * t
            py = y + y0 + (y1 - y0) * t - 26 * math.sin(math.pi * t)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(245, 166, 35))
    for (sx, sy) in [(150, 18), (260, 26)]:
        for k in range(8):
            a = math.pi * k / 4
            d.line([(x + sx, y + sy),
                    (x + sx + 11 * math.cos(a), y + sy + 11 * math.sin(a))],
                   fill=(245, 166, 35), width=2)


def draw_peru_quake(d, x, y, w, h):
    """Peru panel: Andes, seismograph line, houses."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    d.polygon([(x, y + h), (x + 70, y + 26), (x + 140, y + h)], fill=(120, 110, 96))
    d.polygon([(x + 100, y + h), (x + 200, y + 12), (x + 300, y + h)],
              fill=(90, 82, 72))
    d.polygon([(x + 186, y + 12), (x + 200, y + 26), (x + 214, y + 12)],
              fill=(247, 241, 227))
    # seismograph
    pts = [(x + 8, y + 62), (x + 40, y + 62), (x + 52, y + 44), (x + 64, y + 82),
           (x + 76, y + 52), (x + 88, y + 72), (x + 110, y + 62), (x + 150, y + 62),
           (x + 164, y + 40), (x + 178, y + 84), (x + 192, y + 58), (x + 210, y + 62),
           (x + 250, y + 62), (x + 264, y + 46), (x + 278, y + 78), (x + 300, y + 62)]
    d.line(pts, fill=(179, 53, 43), width=3)
    # houses
    for hx in (x + 18, x + 246):
        d.rectangle([hx, y + h - 26, hx + 34, y + h - 8], fill=(247, 241, 227),
                    outline=(27, 42, 74), width=1)
        d.polygon([(hx - 3, y + h - 26), (hx + 17, y + h - 38), (hx + 37, y + h - 26)],
                  fill=(179, 53, 43))

# --- small illustration bands for the 10 pictured stories -------------------
def mini_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 58, 110))
    d.rectangle([x, y, x + w, y + 12], fill=(245, 196, 66))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(245, 196, 66))
    d.line([(x, y + h - 14), (x + w, y + h - 14)], fill=(27, 42, 74), width=2)
    for px in (x + 40, x + 95, x + 150):
        d.line([(px, y + 12), (px, y + h - 14)], fill=(27, 42, 74), width=2)
    d.line([(x + 40, y + 12), (x + 150, y + h - 14)], fill=(27, 42, 74), width=1)


def mini_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 226))
    d.line([(x, y + h - 12), (x + w, y + h - 12)], fill=(14, 124, 123), width=3)
    d.ellipse([x + w // 2 - 16, y + 8, x + w // 2 + 16, y + 24], fill=(27, 42, 74))
    d.line([(x + w // 2 - 26, y + 16), (x + w // 2 + 26, y + 16)], fill=(27, 42, 74),
           width=3)
    d.ellipse([x + w // 2 - 30, y + 12, x + w // 2 - 22, y + 20], fill=(27, 42, 74))
    d.ellipse([x + w // 2 + 22, y + 12, x + w // 2 + 30, y + 20], fill=(27, 42, 74))


def mini_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 241, 227))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(179, 53, 43))
    for a in (0, 60, 120):
        import math
        rx, ry = 34, 13
        pts = []
        for t in range(0, 361, 10):
            r = math.radians(t)
            px = cx + rx * math.cos(r) * math.cos(math.radians(a)) - \
                ry * math.sin(r) * math.sin(math.radians(a))
            py = cy + rx * math.cos(r) * math.sin(math.radians(a)) + \
                ry * math.sin(r) * math.cos(math.radians(a))
            pts.append((px, py))
        d.line(pts, fill=(27, 42, 74), width=1)


def mini_percent(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    d.text((x + 14, y + 2), "%", font=font(SERIF_B, 34), fill=(245, 166, 35))
    d.rectangle([x + w - 70, y + 8, x + w - 12, y + 18], fill=(179, 53, 43))
    d.rectangle([x + w - 70, y + 22, x + w - 12, y + 32], fill=(247, 241, 227))


def mini_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 241, 227))
    d.rectangle([x + 16, y + 8, x + 76, y + h - 8], fill=(222, 41, 16))
    for sy in (y + 14, y + 24, y + 34):
        d.ellipse([x + 40, sy, x + 52, sy + 6], fill=(255, 222, 0))
    d.rectangle([x + 100, y + 8, x + 160, y + h - 8], fill=(255, 255, 255),
                outline=(27, 42, 74), width=1)
    d.ellipse([x + 118, y + 14, x + 142, y + h - 14], fill=(222, 41, 16))


def mini_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 226))
    d.polygon([(x + 30, y + h // 2), (x + 150, y + 8), (x + 168, y + h // 2 - 2),
               (x + 150, y + h - 12), (x + 60, y + h // 2 + 8)],
              fill=(247, 241, 227), outline=(27, 42, 74))
    d.polygon([(x + 80, y + h // 2 - 4), (x + 100, y + 2), (x + 112, y + h // 2 - 4)],
              fill=(27, 42, 74))


def mini_ai(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 124, 123))
    d.rectangle([x + 12, y + 8, x + 52, y + h - 8], fill=(0, 47, 108))
    d.rectangle([x + 60, y + 8, x + 100, y + h - 8], fill=(222, 41, 16))
    d.text((x + 112, y + 6), "AI", font=font(SANS_B, 28), fill=(255, 255, 255))


def mini_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    d.ellipse([x + 14, y + 4, x + 46, y + 36], fill=(245, 166, 35))
    d.text((x + 22, y + 8), "B", font=font(SANS_B, 22), fill=(255, 255, 255))
    d.line([(x + 60, y + 10), (x + 90, y + 22), (x + 120, y + 14), (x + 150, y + 30),
            (x + 178, y + 26)], fill=(179, 53, 43), width=3)


def mini_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 241, 227))
    for r in range(2):
        for c in range(9):
            if (r + c) % 2 == 0:
                d.rectangle([x + 12 + c * 10, y + 6 + r * 10,
                             x + 22 + c * 10, y + 16 + r * 10], fill=(27, 42, 74))
    d.polygon([(x + 110, y + 28), (x + 170, y + 28), (x + 178, y + 36),
               (x + 110, y + 36)], fill=(179, 53, 43))
    d.ellipse([x + 120, y + 34, x + 132, y + 44], fill=(27, 42, 74))
    d.ellipse([x + 158, y + 34, x + 170, y + 44], fill=(27, 42, 74))


def mini_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 79))
    d.polygon([(x + 60, y + 6), (x + 74, y + 6), (x + 96, y + 34), (x + 82, y + 38)],
              fill=(222, 184, 135), outline=(27, 42, 74))
    d.ellipse([x + 130, y + 10, x + 146, y + 26], fill=(179, 53, 43))


MINIS = [mini_bridge, mini_drone, mini_atom, mini_percent, mini_flags,
         mini_plane, mini_ai, mini_bitcoin, mini_f1, mini_cricket]


# --- simplified world map ---------------------------------------------------
# Rough continent polygons in a 330x132 box (x, y offsets relative to panel).
CONTINENTS = [
    # North America
    [(28, 18), (88, 10), (112, 22), (104, 44), (86, 58), (62, 62), (40, 48), (26, 32)],
    # South America
    [(82, 72), (112, 70), (118, 88), (104, 112), (92, 118), (84, 96)],
    # Europe
    [(158, 12), (188, 8), (200, 20), (192, 34), (172, 36), (158, 26)],
    # Africa
    [(162, 44), (196, 40), (212, 56), (204, 86), (186, 96), (168, 78), (158, 58)],
    # Asia
    [(204, 8), (296, 8), (312, 30), (300, 56), (272, 72), (238, 66), (214, 44)],
    # Oceania
    [(288, 88), (318, 86), (322, 104), (296, 108)],
]
# (number, x, y) pins for the 13 pictured stories
PINS = [(1, 178, 26), (2, 224, 46), (3, 96, 94), (4, 184, 20), (5, 232, 42),
        (6, 228, 34), (7, 66, 32), (8, 282, 28), (9, 292, 58), (10, 302, 100),
        (11, 76, 38), (12, 56, 40), (13, 314, 106)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(213, 228, 232))
    for poly in CONTINENTS:
        d.polygon([(x + px, y + py) for px, py in poly], fill=(232, 213, 176),
                  outline=(180, 168, 140))
    for num, px, py in PINS:
        d.ellipse([x + px - 8, y + py - 8, x + px + 8, y + py + 8],
                  fill=(179, 53, 43), outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9)
        tw = d.textlength(str(num), font=f)
        d.text((x + px - tw / 2, y + py - 5), str(num), font=f, fill=(255, 255, 255))

# --- the 35 dated stories ----------------------------------------------------
STATS = [
    ("13", "DAY OF COP31, MEANT TO CLOSE ON DAY 12"),
    ("5", "MISSILES SHOT DOWN OVER RIYADH AND JIZAN"),
    ("6.7", "MAGNITUDE OF THE PERU QUAKE"),
    ("146", "PEOPLE SAFE AFTER THE DAVAO EMERGENCY LANDING"),
    ("$58,983", "BITCOIN EARLY SATURDAY, DOWN 3.9% IN A DAY"),
    ("124*", "K L RAHUL'S SCORE AT TEA IN WELLINGTON"),
]
REGIONS = [("EUROPE", 4, (27, 42, 74)), ("ASIA", 10, (179, 53, 43)),
           ("MIDDLE EAST", 5, (192, 122, 26)), ("AFRICA", 1, (46, 125, 79)),
           ("AMERICAS", 11, (14, 124, 123)), ("OCEANIA", 3, (74, 127, 165)),
           ("GLOBAL", 1, (107, 107, 107))]

LEADS = [
    dict(kicker="COP31: OVERTIME", loc="1 · ANTALYA, TÜRKIYE · CLIMATE",
         head="Climate summit runs into Saturday with no deal",
         body="COP31 missed its Friday close. A draft with no mention of fossil fuels "
              "split nearly 200 countries; a third text is promised. (AFP, Al Jazeera)",
         src="Ongoing · AFP, Al Jazeera", badge=("CONFIRMED", (46, 125, 79)),
         art=draw_globe_thermo),
    dict(kicker="SAUDI: MISSILES", loc="2 · RIYADH · JIZAN · WAR",
         head="Five Houthi missiles shot down over Saudi Arabia",
         body="The Saudi-led coalition said three were destroyed over Riyadh before "
              "dawn and two over Jizan, a day after it bombed Hodeidah port. "
              "(AFP, Dawn)",
         src="Coalition's count · AFP", badge=("CONFIRMED", (46, 125, 79)),
         art=draw_riyadh_night),
    dict(kicker="PERU: QUAKE 6.7", loc="3 · JUNÍN, PERU · EARTHQUAKE",
         head="Magnitude 6.7 earthquake shakes central Peru",
         body="The deep quake near Carhuamayo was felt in Lima and along the coast. "
              "Peru's institute reported no deaths, damage or tsunami risk. "
              "(USGS, Gestión)",
         src="USGS · IGP", badge=("OFFICIAL", (38, 58, 110)),
         art=draw_peru_quake),
]

MIDS = [
    dict(tag="KYIV: WARNING", loc="4 · KYIV · WAR",
         head="Zelensky: Crimea bridge “will not stay”",
         body="He warns of more double-tap strikes. (NBC)",
         badge=("REPORTED", (192, 122, 26))),
    dict(tag="HORMUZ: DRONE", loc="5 · STRAIT OF HORMUZ · WAR",
         head="Iran says it shot down a US drone",
         body="No confirmation from Washington. (IRIB)",
         badge=("REPORTED", (192, 122, 26))),
    dict(tag="IRAN: URANIUM", loc="6 · TEHRAN · DIPLOMACY",
         head="Iran: uranium stock stays in the country",
         body="Minister still seeks a “fair solution”. (ToI)",
         badge=("OFFICIAL", (38, 58, 110))),
    dict(tag="TRUMP: AI TAX", loc="7 · WASHINGTON · TECHNOLOGY",
         head="Trump vows tax on data centres abroad",
         body="“Tremendous” penalty; no details yet. (ABC)",
         badge=("REPORTED", (192, 122, 26))),
    dict(tag="CHINA–JAPAN", loc="8 · BEIJING · DIPLOMACY",
         head="China tells Japan to “correct” Taiwan words",
         body="Tokyo says its stance is unchanged. (Ministry, AFP)",
         badge=("OFFICIAL", (38, 58, 110))),
    dict(tag="DAVAO: 146 SAFE", loc="9 · DAVAO · AVIATION",
         head="Jet lands safely after engine fire alert",
         body="Air Niugini 767 diverts after midnight. (Airline, AP)",
         badge=("OFFICIAL", (38, 58, 110))),
    dict(tag="CANBERRA: AI", loc="10 · CANBERRA · DIPLOMACY",
         head="Australia and China agree AI talks",
         body="Albanese ends an 11-day trip. (ABC)",
         badge=("OFFICIAL", (38, 58, 110))),
    dict(tag="BITCOIN: $58,983", loc="11 · WORLD · MARKETS",
         head="Bitcoin trades below $59,000 on Saturday",
         body="Down 3.9% in 24 hours; ether $1,625. (CoinGecko)",
         badge=("CONFIRMED", (46, 125, 79))),
    dict(tag="RUSSELL: P1", loc="12 · LAS VEGAS · FORMULA 1",
         head="Russell fastest in final Las Vegas practice",
         body="1:34.041 in a damp, messy session. (Formula 1)",
         badge=("OFFICIAL", (38, 58, 110))),
    dict(tag="RAHUL: 124*", loc="13 · WELLINGTON · CRICKET",
         head="Rahul hits a century against New Zealand",
         body="India 344 for 2 at tea, replying to 368. (AFP)",
         badge=("CONFIRMED", (46, 125, 79))),
]

ALSO = [
    (14, "Kryvyi Rih: Double strike kills 2, injures 42", "Kyiv Independent"),
    (15, "Copenhagen: Russian attaché expelled over a plot", "Al Jazeera"),
    (16, "Antalya: EU warns COP31 risks a “fossil summit”", "AFP"),
    (17, "Antalya: Panama threatens to block the climate text", "Al Jazeera"),
    (18, "Antalya: Indonesia’s PLN signs clean-power deals", "Antara"),
    (19, "Yemen: Houthis threaten Jeddah, Red Sea ports", "Al Jazeera"),
    (20, "Washington: Vance: Iran strikes were Trump’s call", "Reuters"),
    (21, "Washington: Lawmaker threatens SpaceX’s funding", "CNN"),
    (22, "Texas: Execution of a man of 70 takes 63 minutes", "ABC"),
    (23, "Los Angeles: Jury convicts man of starting Palisades fire", "ABC"),
    (24, "Missouri: Judge approves $7.25bn Roundup settlement", "AFP"),
    (25, "Vancouver: Canada rests defence in youth climate trial", "AFP"),
    (26, "Pyongyang: Kim tours factories, no Trump talks", "AFP"),
    (27, "Sejong: Freight train derails; no one hurt", "Korea Herald"),
    (28, "Taipei: Budget and cash payout passed", "Taipei Times"),
    (29, "Bangkok: Six-point plan on arsenic in two rivers", "The Nation"),
    (30, "New Delhi: Pakistan minister joins SCO forum in India", "Dawn"),
    (31, "Eastern India: Rain alerts as Akvan’s remnants move inland", "ETV"),
    (32, "Myanmar: Rights groups urge sanctions after court ruling", "AP"),
    (33, "Port Louis: African rating agency talks to 15 states", "Al Jazeera"),
    (34, "Melbourne: Cummins keeps the Australian captaincy", "ABC"),
    (35, "Las Vegas: Verstappen sent to stewards after contact", "Autosport"),
]

DATE_CHECK = ("DATE CHECK — Left out as Friday 20 November’s news: Wall Street’s fall "
              "into correction · the Russian barrage that hit Kyiv’s bridges · the missile "
              "that landed in Poland · the UK–EU deal · Cyclone Akvan’s landfall. Older "
              "still: Voyager 1’s light-day (18 Nov). Not confirmed when drawn, so not "
              "shown: BepiColombo in Mercury orbit · a final COP31 text.")

# --- page layout --------------------------------------------------------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24                      # side margin
    CW = W - 2 * MX              # content width = 976

    # kicker row
    d.text((MX, 12), "ONE DAY · EVERY CONTINENT · EVERY STORY DATED",
           font=font(SANS_B, 13), fill=RED)
    r = "35 STORIES · 7 REGIONS"
    d.text((W - MX - d.textlength(r, font=font(SANS_B, 13)), 12), r,
           font=font(SANS_B, 13), fill=INK)
    hline(d, MX, W - MX, 32, width=2)

    # masthead
    title = "Saturday 21 November 2026"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 38), title, font=tf, fill=INK)
    sub = ("COP31 runs into overtime · Five missiles shot down over Saudi Arabia · "
           "Strong quake shakes Peru")
    sf = font(SERIF_I, 17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 108), sub, font=sf, fill=INK)
    hline(d, MX, W - MX, 132, width=2)
    hline(d, MX, W - MX, 136, width=1)

    # stat strip: 6 cells
    y0, y1 = 142, 200
    cell = CW // 6
    for i, (num, cap) in enumerate(STATS):
        x = MX + i * cell
        if i:
            d.line([(x, y0 + 4), (x, y1 - 4)], fill=RED, width=2)
        nf = font(SANS_B, 30)
        d.text((x + 8, y0), num, font=nf, fill=RED)
        text_block(d, x + 8, y0 + 34, cap, font(SANS_B, 9), INK, cell - 14, 11,
                   max_lines=2)
    hline(d, MX, W - MX, y1, width=1)

    # region bar: equal segments (narrow proportional ones clipped labels)
    y0, y1 = 206, 226
    seg = CW // 7
    for i, (name, count, color) in enumerate(REGIONS):
        x = MX + i * seg
        d.rectangle([x, y0, x + seg - 1, y1], fill=color)
        lab = f"{name} {count}"
        f = font(SANS_B, 11)
        d.text((x + 6, y0 + 4), lab, font=f, fill=(255, 255, 255))
    hline(d, MX, W - MX, y1 + 4, width=1)

    # lead row: 3 columns, fixed internal positions so nothing collides
    y0 = 238
    colw = (CW - 24) // 3
    for i, lead in enumerate(LEADS):
        x = MX + i * (colw + 12)
        lead["art"](d, x, y0, colw, 104)
        # kicker bar
        d.rectangle([x, y0 + 104, x + colw, y0 + 126], fill=RED)
        d.text((x + 8, y0 + 109), lead["kicker"], font=font(SANS_B, 13),
               fill=(255, 255, 255))
        d.text((x, y0 + 132), lead["loc"], font=font(SANS_B, 10), fill=RED)
        text_block(d, x, y0 + 146, lead["head"], font(SERIF_B, 21), INK, colw,
                   23, max_lines=2)
        text_block(d, x, y0 + 194, lead["body"], font(SANS, 12), INK, colw, 15,
                   max_lines=3)
        d.text((x, y0 + 242), lead["src"], font=font(SANS, 9), fill=GREY)
        bl, bc = lead["badge"]
        badge(d, x + colw - 78, y0 + 241, bl, bc)

    # mid rows: 2 rows x 5, fixed internals, badge pinned to cell bottom
    y0 = 504
    midw = (CW - 4 * 10) // 5
    midh = 140
    for row in range(2):
        for col in range(5):
            m = MIDS[row * 5 + col]
            x = MX + col * (midw + 10)
            y = y0 + row * (midh + 8)
            MINIS[row * 5 + col](d, x, y, midw, 40)
            d.rectangle([x, y + 40, x + midw, y + 55], fill=INK)
            d.text((x + 6, y + 43), m["tag"], font=font(SANS_B, 10),
                   fill=(255, 255, 255))
            d.text((x, y + 58), m["loc"], font=font(SANS_B, 9), fill=RED)
            text_block(d, x, y + 70, m["head"], font(SERIF_B, 13), INK, midw,
                       14, max_lines=2)
            text_block(d, x, y + 100, m["body"], font(SANS, 10), INK, midw,
                       11, max_lines=2)
            bl, bc = m["badge"]
            badge(d, x + midw - 62, y + 124, bl, bc)

    # map + also-list row
    y0 = 806
    map_w = 330
    d.text((MX, y0), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    d.text((MX + 350, y0), "ALSO ON SATURDAY 21 NOVEMBER 2026 — 22 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    y0 += 16
    draw_map(d, MX, y0, map_w, 120)
    d.text((MX, y0 + 124), "Each number is the story with that number on this page.",
           font=font(SANS, 9), fill=GREY)
    # also list, 2 columns of 11
    lx = MX + 350
    colw2 = (W - MX - lx - 10) // 2
    f_item = font(SANS, 10)
    f_num = font(SANS_B, 10)
    for ci in range(2):
        for ri in range(11):
            num, head, src = ALSO[ci * 11 + ri]
            yy = y0 + ri * 12
            d.text((lx + ci * (colw2 + 10), yy), str(num), font=f_num, fill=RED)
            d.text((lx + ci * (colw2 + 10) + 18, yy), head, font=f_item, fill=INK)
            tw = d.textlength(head, font=f_item)
            d.text((lx + ci * (colw2 + 10) + 18 + tw + 3, yy), f"({src})",
                   font=font(SANS, 8), fill=GREY)

    # date check box
    y0 = 960
    d.rounded_rectangle([MX, y0, W - MX, y0 + 40], radius=3,
                        outline=RED, width=2)
    text_block(d, MX + 8, y0 + 4, DATE_CHECK, font(SANS, 10), INK, CW - 16, 12,
               max_lines=3)

    # footer
    foot = ("Every story here happened, or was first reported, on Saturday 21 November "
            "2026. Sources named beside each story · Original drawings.")
    ff = font(SANS, 9)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y0 + 44), foot, font=ff,
           fill=GREY)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}  {W}x{H}  {size} bytes  ({size / 1024:.0f} KiB)")
    assert size <= 1024 * 1024, "entry.png exceeds the 1 MiB gate"
    return out


if __name__ == "__main__":
    render()
