#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news poster for the make.fun bounty.

Reads nothing from the network. Every story below was checked against news
reports of Thursday 19 November 2026 before it was written into the picture:

  1. Trump, Xi and Putin hold their first three-way summit in Shenzhen and
     issue a four-point "Declaration toward Peace" (Reuters, USA Today,
     The Times). The text covers UN reform, refined-fuel supply, state
     immunity and nuclear risk; it does not mention Ukraine, Iran or
     North Korea.
  2. The International Court of Justice rules Myanmar committed genocide
     against the Rohingya in its 2017 crackdown, 9 votes to 6 (CNN, WSJ,
     AP) - the first time in the court's 80-year history it has held a
     state responsible for genocide.
  3. Anthropic debuts on the Nasdaq (ticker ANT): IPO price $83, opened at
     $111.50, closed at $97.17, up 17%, the largest IPO on record at $81bn
     (Motley Fool, Barron's, TradingView, Invezz, Breitbart).
  4. The European Commission proposes a 45 billion euro loan to Ukraine
     (Horizon, 10 Things Global News).
  5. Violence spreads in Bangladesh: Muhammad Yunus's ancestral home is set
     on fire and unrest hits 28 districts (Horizon).
  6. Footer: aid groups score the UN-backed Gaza peace plan 4 out of 26
     (All Voices News); Trump pardons late baseball star Pete Rose for
     tax crimes (LA Post).

Output: entry.png, 1024x1024, under 1 MiB. Run: python3 tools/make_image.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (248, 245, 238)
INK = (25, 25, 25)
NAVY = (22, 50, 79)
NAVY_LIGHT = (215, 222, 232)
RED = (179, 38, 30)
RED_LIGHT = (255, 157, 138)
GOLD = (233, 196, 66)
MUTED = (90, 90, 90)
PANEL = (255, 255, 255)
BORDER = (217, 211, 195)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading):
    """Draw wrapped text; return the y just below the block."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color, anchor="la")
        y += leading
    return y


def draw_bars_up(d, x, y, w, h, color):
    n, gap = 4, 10
    bw = (w - gap * (n - 1)) // n
    heights = [h * 0.35, h * 0.55, h * 0.75, h]
    for i, bh in enumerate(heights):
        bx = x + i * (bw + gap)
        fill = RED if i == n - 1 else color
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=fill)


def draw_gavel(d, x, y, w, h, color):
    # Gavel head (horizontal bar) + handle + sound block.
    d.rounded_rectangle([x + 6, y + 8, x + w - 6, y + 30], radius=6, fill=color)
    d.line([x + w // 2, y + 30, x + w // 2, y + h - 22], fill=color, width=7)
    d.rounded_rectangle([x + 14, y + h - 22, x + w - 14, y + h - 10],
                        radius=4, fill=color)
    d.ellipse([x + w // 2 - 5, y + 14, x + w // 2 + 5, y + 24], fill=RED)


def draw_euro(d, x, y, w, h, color):
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.text((cx, cy), "\u20ac", font=font(BOLD, 52), fill=color, anchor="mm")


def draw_alert(d, x, y, w, h, color):
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h) - 10
    d.polygon([(cx, cy - s // 2), (cx + s // 2, cy + s // 2 - 6),
               (cx - s // 2, cy + s // 2 - 6)], outline=color, width=5)
    d.text((cx, cy + 2), "!", font=font(BOLD, 44), fill=RED, anchor="mm")


def draw_flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=RED)
    for i in (1, 3, 5):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(255, 255, 255))
    cw, ch = int(w * 0.42), int(h * 0.54)
    d.rectangle([x, y, x + cw, y + ch], fill=NAVY)
    d.ellipse([x + cw // 2 - 6, y + ch // 2 - 6,
               x + cw // 2 + 6, y + ch // 2 + 6], fill=(255, 255, 255))


def draw_flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + 10, y + 8, x + 26, y + 24], fill=GOLD)
    for dx, dy in ((34, 10), (42, 20), (38, 32), (28, 34)):
        d.ellipse([x + dx, y + dy, x + dx + 8, y + dy + 8], fill=GOLD)


def draw_flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.text((MARGIN, 38), "THE WORLD IN ONE PICTURE", font=font(BOLD, 27),
           fill=NAVY, anchor="la")
    d.text((MARGIN, 72), "Thursday, 19 November 2026", font=font(SERIF_BOLD, 56),
           fill=INK, anchor="la")
    d.line([MARGIN, 158, MARGIN + CW, 158], fill=INK, width=3)
    d.line([MARGIN, 164, MARGIN + CW, 164], fill=INK, width=1)

    # ---- lead story: the Shenzhen summit ----
    lead = (MARGIN, 180, MARGIN + CW, 420)
    d.rounded_rectangle(lead, radius=8, fill=NAVY)
    tx = MARGIN + 26
    d.text((tx, 198), "SUMMIT IN SHENZHEN", font=font(BOLD, 25),
           fill=RED_LIGHT, anchor="la")
    y = text_block(d, tx, 232, "TRUMP, XI, PUTIN ISSUE PEACE PLEDGE",
                   font(BOLD, 40), (255, 255, 255), 700, 48)
    text_block(d, tx, y + 12,
               "First three-way summit ends with a four-point "
               "\u2018Declaration toward Peace\u2019 \u2014 silent on "
               "Ukraine, Iran and North Korea.",
               font(REG, 23), NAVY_LIGHT, 700, 29)
    # Three flags on the right: United States, China, Russia.
    fw, fh = 110, 56
    fx = MARGIN + CW - fw - 22
    draw_flag_us(d, fx, 198, fw, fh)
    draw_flag_cn(d, fx, 272, fw, fh)
    draw_flag_ru(d, fx, 346, fw, fh)

    # ---- story panels ----
    def panel(x, y, w, h, kicker, headline, summary, icon):
        d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=PANEL,
                            outline=BORDER, width=2)
        icon(d, x + 18, y + 22, 84, 84, NAVY)
        tx = x + 118
        d.text((tx, y + 20), kicker, font=font(BOLD, 20), fill=RED, anchor="la")
        y2 = text_block(d, tx, y + 48, headline, font(BOLD, 28), INK, w - 134, 34)
        text_block(d, tx, y2 + 8, summary, font(REG, 21), (60, 60, 60),
                   w - 134, 26)

    def icon_gavel(d, x, y, w, h, color):
        draw_gavel(d, x + 6, y + 6, w - 12, h - 12, color)

    def icon_bars(d, x, y, w, h, color):
        draw_bars_up(d, x, y + 18, w, h - 30, color)

    def icon_euro(d, x, y, w, h, color):
        draw_euro(d, x + 4, y + 6, w - 8, h - 12, color)

    def icon_alert(d, x, y, w, h, color):
        draw_alert(d, x + 4, y + 6, w - 8, h - 12, color)

    pw, ph, gap = 468, 240, 16
    panel(MARGIN, 432, pw, ph, "JUSTICE \u00b7 THE HAGUE",
          "FIRST STATE FOUND GUILTY OF GENOCIDE",
          "World Court holds Myanmar responsible for the 2017 Rohingya "
          "crackdown, 9\u20136 \u2014 a first in 80 years.",
          icon_gavel)
    panel(MARGIN + pw + gap, 432, pw, ph, "MARKETS \u00b7 NEW YORK",
          "RECORD $81BN IPO DEBUTS",
          "Anthropic opens at $111.50, closes at $97 \u2014 up 17% on its "
          "first day.",
          icon_bars)
    panel(MARGIN, 688, pw, ph, "EUROPE \u00b7 BRUSSELS",
          "EU PROPOSES \u20ac45BN UKRAINE LOAN",
          "European Commission proposes a \u20ac45 billion loan to back Kyiv.",
          icon_euro)
    panel(MARGIN + pw + gap, 688, pw, ph, "BANGLADESH \u00b7 DHAKA",
          "VIOLENCE SPREADS IN BANGLADESH",
          "Yunus\u2019s ancestral home torched as unrest hits 28 districts.",
          icon_alert)

    # ---- footer ----
    f1 = ("ALSO: Gaza aid groups score the peace plan 4 out of 26 \u00b7 "
          "Trump pardons baseball star Pete Rose")
    fw = d.textlength(f1, font=font(REG, 20))
    d.text(((W - fw) / 2, 946), f1, font=font(REG, 20), fill=MUTED, anchor="la")
    f2 = "All events as reported on Thursday, 19 November 2026."
    fw2 = d.textlength(f2, font=font(REG, 17))
    d.text(((W - fw2) / 2, 976), f2, font=font(REG, 17), fill=(140, 140, 140),
           anchor="la")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
