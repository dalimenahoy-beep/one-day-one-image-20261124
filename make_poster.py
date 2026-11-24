#!/usr/bin/env python3
"""Draw "The World Gazette" front page for Tuesday 24 November 2026.

Build-time renderer: produces entry.png (1024x1024) next to this file.
The shipped program (main.ts) never draws; it only copies entry.png.
All stories and figures are from 24 Nov 2026 reporting (BBC, The Guardian,
France 24, Al Jazeera, Euronews, Middle East Eye, CNBC, NPR, Yonhap,
via One Turn's daily roundup, cross-checked with other roundups).
"""
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 28
W = PAGE - 2 * MARGIN
PAPER = (247, 243, 233)
INK = (18, 18, 18)
ACCENT = (150, 24, 24)
FAINT = (105, 100, 92)
BOX = (233, 227, 213)
WHITE = (250, 248, 242)
TICKER_BG = (12, 12, 12)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANSB = "DejaVuSans-Bold.ttf"

img = Image.new("RGB", (PAGE, PAGE), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, text, font, width, leading, fill=INK):
    for line in wrap(text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y

def region(x, y, name, width):
    d.text((x, y), name.upper(), font=F(SANSB, 11.5), fill=ACCENT)
    y += 15
    d.line([(x, y), (x + width, y)], fill=INK, width=1)
    return y + 5

def story(x, y, headline, body, width):
    y = text_block(x, y, headline, F(SANSB, 15), width, 18)
    y += 1
    y = text_block(x, y, body, F(SANS, 12), width, 15, fill=(40, 40, 40))
    return y + 11

# ---------- masthead ----------
y = 20
d.text((MARGIN, y), "The World Gazette", font=F(SERIF, 54), fill=INK)
y += 68
d.line([(MARGIN, y), (MARGIN + W, y)], fill=INK, width=3)
y += 6
d.text((MARGIN, y), "Tuesday 24 November 2026", font=F(SANSB, 14), fill=INK)
sub = "One image, the whole day — 83 stories scanned, 12 told"
d.text((MARGIN + W - d.textlength(sub, font=F(SANS, 12)), y + 1), sub,
       font=F(SANS, 12), fill=FAINT)
y += 23
d.line([(MARGIN, y), (MARGIN + W, y)], fill=INK, width=1)
y += 11

# ---------- lead ----------
lead_end = y + 124
d.rectangle([(MARGIN, y), (MARGIN + W, lead_end)], fill=BOX)
lx = MARGIN + 16
ly = y + 10
d.text((lx, ly), "TECHNOLOGY · SANTA CLARA", font=F(SANSB, 11.5), fill=ACCENT)
ly += 19
ly = text_block(lx, ly, "NVIDIA BRINGS BACK HUANG AFTER TRUMP CALL",
                F(SERIF, 27), W - 32, 32)
ly += 2
text_block(lx, ly,
    "Nvidia's board reinstated Jensen Huang as chief executive on Monday, "
    "11 days after he resigned. Trump said he 'convinced' the board. Shares "
    "closed 31% higher, adding about $1 trillion in a day; Congress plans "
    "to question Huang on his China ties.",
    F(SANS, 12.5), W - 32, 16, fill=(40, 40, 40))
y = lead_end + 11

# ---------- columns ----------
col_w = (W - 24) // 2
x1, x2 = MARGIN, MARGIN + col_w + 24
col_top = y

# left column: world, europe, middle east
ly = col_top
ly = region(x1, ly, "World", col_w)
ly = story(x1, ly, "Ukraine sinks Russian corvette off Libya",
    "President Zelensky confirmed seven Ukrainian naval drones sank the "
    "Russian corvette Merkury at Benghazi; a cargo ship was also hit. "
    "The UN mission in Libya called for an independent probe.", col_w)
ly = story(x1, ly, "COP31 climate summit ends without a deal",
    "The UN talks in Antalya ran two days over — the longest in history — "
    "and closed with no agreement. The EU and about 130 parties rejected "
    "a draft that left out a fossil-fuel phase-out.", col_w)
ly = region(x1, ly, "Europe", col_w)
ly = story(x1, ly, "Russian drone enters Polish airspace; NATO sends AWACS",
    "A Russian drone violated Polish airspace days after three cruise "
    "missiles fell in Poland. NATO agreed to send an early-warning "
    "aircraft as Warsaw investigates 'intentional activity'.", col_w)
ly = region(x1, ly, "Middle East", col_w)
ly = story(x1, ly, "Iran says three tankers hit mines in Hormuz",
    "Tehran's Revolutionary Guards said three tankers hit mines in the "
    "Strait of Hormuz under US escort; the claim is unconfirmed. A fifth "
    "of the world's oil passes through the strait.", col_w)
ly = story(x1, ly, "Strikes on Yemen buses and trucks kill about 25",
    "Air strikes hit buses and trucks in Lahj governorate, leaving 25 "
    "dead or missing. Middle East Eye reported the aircraft were Saudi; "
    "the Houthis and Yemen's government blamed each other.", col_w)
left_end = ly

# right column: world (cont.), americas, indonesia, markets & science
ry = col_top
ry = region(x2, ry, "World", col_w)
ry = story(x2, ry, "UK and 13 countries act on ICJ genocide ruling",
    "Britain sanctioned five Myanmar military leaders and recognised the "
    "World Court ruling that Myanmar committed genocide against the "
    "Rohingya; 13 other countries acknowledged it too.", col_w)
ry = region(x2, ry, "Americas", col_w)
ry = story(x2, ry, "Democrats win House by largest margin in decades",
    "Final counts three weeks after the US midterms show Democrats "
    "flipped 47 House seats and could reach 49 — their biggest majority "
    "in decades. Reports put the Senate at 56 to 44.", col_w)
ry = story(x2, ry, "Car bomb hits governor's office in Colombia",
    "A car bomb beside the Meta government building in Villavicencio "
    "injured at least 21 people and cut power. A drone attack on a "
    "Cucuta police station was Colombia's first in a city.", col_w)
ry = region(x2, ry, "Indonesia", col_w)
ry = story(x2, ry, "Factory fire kills 26 in Banten, dozens missing",
    "The death toll from a candy factory fire in Banten province rose "
    "to 26, with about 34 people still missing. Rescuers searched "
    "unstable structures; DNA testing is needed to name victims.", col_w)
ry = region(x2, ry, "Markets & Science", col_w)
ry = story(x2, ry, "Stocks surge as tech rebounds: Nikkei +3.91%",
    "Huang's return lit up markets: the S&P 500 rose 4.73% to 7,237 and "
    "Seoul gained over 6%, while Brent crude held at $86.71, near "
    "three-month lows despite the Hormuz claims.", col_w)
ry = story(x2, ry, "Pakistani astronaut to fly on China's Shenzhou-24",
    "China named the Shenzhou-24 crew: Pakistan Air Force pilot Zeeshan "
    "Ali will be the first foreign astronaut aboard the Tiangong "
    "station. Launch is Wednesday; he will stay about a week.", col_w)
right_end = ry

cols_end = max(left_end, right_end)

# ---------- day in numbers ----------
ny = cols_end + 2
d.line([(MARGIN, ny), (MARGIN + W, ny)], fill=INK, width=1)
ny += 7
d.text((MARGIN, ny), "THE DAY IN NUMBERS", font=F(SANSB, 11.5), fill=ACCENT)
ny += 18
nums = [
    ("+31%", "Nvidia's one-day share jump"),
    ("7", "drones that sank the Merkury"),
    ("130", "parties rejecting COP31 draft"),
    ("47", "House seats flipped to Democrats"),
    ("26", "dead in the Banten factory fire"),
]
cell = W // len(nums)
for i, (big, small) in enumerate(nums):
    cx = MARGIN + i * cell
    d.text((cx, ny), big, font=F(SERIF, 20), fill=INK)
    text_block(cx, ny + 26, small, F(SANS, 10), cell - 10, 12, fill=FAINT)
ny += 54

# ---------- wire ticker ----------
ty = PAGE - 40
d.rectangle([(0, ty), (PAGE, PAGE)], fill=TICKER_BG)
d.text((MARGIN, ty + 7), "THE WIRE", font=F(SANSB, 12), fill=(255, 110, 110))
wire = ("Estonia to close Russia crossings Dec. 1  ·  Nepal PM wins EUR1.4bn India pledge  ·  "
        "CrowdStrike to buy Zscaler for $44bn")
wire_w = d.textlength(wire, font=F(SANS, 11.5))
assert MARGIN + 82 + wire_w <= PAGE - MARGIN, f"wire too wide: {wire_w}"
d.text((MARGIN + 82, ty + 8), wire, font=F(SANS, 11.5), fill=WHITE)

img.save("/home/hatch/workspace/makefun/news-image-20261124-repo/entry.png")
print("left_end:", left_end, "right_end:", right_end,
      "numbers_end:", ny, "ticker_top:", ty)
