#!/usr/bin/env python3
"""Assemble the Arisan Circle demo video from the REAL demo transcript.

Frames are rendered with PIL; every terminal/page frame shows actual output
captured from `bash demo/demo.sh` (local devnet, real transactions).
Output: frames/*.png + concat.txt for ffmpeg.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, "frames")
os.makedirs(FRAMES, exist_ok=True)

W, H = 1280, 720
BG = (11, 15, 20)
PANEL = (17, 22, 29)
TEXT = (230, 237, 243)
MUTED = (148, 163, 184)
GREEN = (126, 224, 163)
BLUE = (108, 182, 255)
CAPBG = (24, 33, 45)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def caption(img, text):
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 64, W, H], fill=CAPBG)
    f = font(SANS, 24)
    tw = d.textlength(text, font=f)
    d.text(((W - tw) / 2, H - 46), text, font=f, fill=TEXT)


def card(title, body_lines, fname, title_size=54, body_size=27, title_color=TEXT):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_t = font(SANSB, title_size)
    tw = d.textlength(title, font=f_t)
    d.text(((W - tw) / 2, 150), title, font=f_t, fill=title_color)
    y = 260
    f_b = font(SANS, body_size)
    for line in body_lines:
        for wl in wrap(d, line, f_b, W - 220):
            lw = d.textlength(wl, font=f_b)
            d.text(((W - lw) / 2, y), wl, font=f_b, fill=MUTED)
            y += body_size + 14
        y += 12
    img.save(os.path.join(FRAMES, fname))
    return img


def terminal(lines, fname, caption_text, title="arisan — local devnet demo (real transactions)"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 30, W - 40, H - 90], radius=14, fill=PANEL)
    d.ellipse([62, 48, 78, 64], fill=(255, 95, 86))
    d.ellipse([88, 48, 104, 64], fill=(255, 189, 46))
    d.ellipse([114, 48, 130, 64], fill=(39, 201, 63))
    d.text((150, 44), title, font=font(MONO, 19), fill=MUTED)
    f = font(MONO, 21)
    y = 92
    for line in lines:
        color = TEXT
        if line.startswith("=="):
            color = BLUE
            fnt = font(MONOB, 21)
        elif line.strip() == "OK!":
            color = GREEN
            fnt = font(MONOB, 21)
        elif "REJECTED" in line:
            color = GREEN
            fnt = font(MONOB, 20)
        else:
            fnt = f
        d.text((64, y), line, font=fnt, fill=color)
        y += 29
    caption(img, caption_text)
    img.save(os.path.join(FRAMES, fname))
    return img


CRE = "g1gmxsclc5g3u7s64yzaw232m9eeden50prh9mdp"
MEM = "g15zvsnvsdnh99ft9h2cr7zuplcqk53c6fk88nnp"

# 1 — title
img = card(
    "Arisan Circle",
    ["The Indonesian rotating savings club (ROSCA),",
     "running entirely on-chain on Gno.land."],
    "f01.png", title_size=72)
d = ImageDraw.Draw(img)
sub = "Gnome Tavern Hackathon  ·  Gno.land"
f = font(SANS, 24)
d.text(((W - d.textlength(sub, font=f)) / 2, 470), sub, font=f, fill=BLUE)
img.save(os.path.join(FRAMES, "f01.png"))

# 2 — problem
card(
    "Saving together, on trust",
    ["In an arisan, everyone chips in a fixed amount each round",
     "and one member takes the whole pot — rotating until all",
     "have received it once.",
     "",
     "Millions across Southeast Asia save this way. Today it runs",
     "on an organizer's honesty, group chats, and memory.",
     "",
     "Arisan Circle puts the whole rotation into a realm:"],
    "f02.png", title_size=44)

# 3..6 — terminal, cumulative
base = [
    "Realm: gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan",
    f"creator: {CRE}",
    f"member2: {MEM}",
    "",
]
steps = [
    ("== CreateCircle(KeluargaBesar, 100000, 2) ==", "OK!"),
    ("== JoinCircle(0) ==", "OK!"),
    ("== StartCircle(0) ==", "OK!"),
    ("== Round 1: Contribute creator ==", "OK!"),
    ("== Round 1: Contribute member2 (payout!) ==", "OK!"),
    ("== Round 2: Contribute creator ==", "OK!"),
    ("== Round 2: Contribute member2 (payout!) ==", "OK!"),
]
terminal(base, "f03.png",
         "Two members, one circle — a local devnet with real coin movement")
terminal(base + [x for s in steps[:3] for x in s], "f04.png",
         "Open a circle (0.1 GNOT per round) — join — start")
terminal(base + [x for s in steps[:5] for x in s], "f05.png",
         "Round 1: the last contribution lands — the pot pays out automatically")
terminal(base + [x for s in steps[:7] for x in s], "f06.png",
         "Round 2: rotation moves to the next member — circle finished")

# 7 — the realm's real Render() output (what gnoweb displays)
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.rounded_rectangle([40, 30, W - 40, H - 90], radius=14, fill=PANEL)
d.ellipse([62, 48, 78, 64], fill=(255, 95, 86))
d.ellipse([88, 48, 104, 64], fill=(255, 189, 46))
d.ellipse([114, 48, 130, 64], fill=(39, 201, 63))
d.text((150, 44), "realm Render() — the page gnoweb serves for circle/0",
       font=font(MONO, 19), fill=MUTED)
page = [
    ("# KeluargaBesar", 30, TEXT, SANSB),
    ("", 14, TEXT, SANS),
    ("Status: finished", 23, GREEN, SANSB),
    (f"Creator: {CRE}", 21, MUTED, MONO),
    ("Contribution: 0.1 GNOT (100000 ugnot) per member, per round", 21, TEXT, SANS),
    ("Pot per round: 0.2 GNOT", 21, TEXT, SANS),
    ("", 14, TEXT, SANS),
    ("Members (in payout order)", 24, TEXT, SANSB),
    (f"1.  {CRE}", 21, MUTED, MONO),
    (f"2.  {MEM}", 21, MUTED, MONO),
    ("", 14, TEXT, SANS),
    ("Payout history", 24, TEXT, SANSB),
    (f"Round 1:  {CRE}", 21, MUTED, MONO),
    (f"Round 2:  {MEM}", 21, MUTED, MONO),
]
y = 96
for text, size, color, fp in page:
    d.text((64, y), text, font=font(fp, size), fill=color)
    y += size + 13
caption(img, "The realm renders its own pages — payout history stays on-chain forever")
img.save(os.path.join(FRAMES, "f07.png"))

# 8 — security
terminal([
    "== Bypass attempt: maketx run script calling CreateCircle ==",
    "",
    "A script tries to open a circle in a user's name:",
    "",
    "REJECTED as designed:",
    "'arisan: must be called directly by a user account'",
    "",
    "Contributions are also verified to the exact coin:",
    "underpay, overpay, or wrong denomination — rejected.",
], "f08.png",
    "Safety: only direct user calls — no contract or script can act for you")

# 9 — close
img = card(
    "No fees. No custodian. No admin key.",
    ["The complete arisan lifecycle, enforced by the realm.",
     "",
     "Code, tests and this demo: github.com/afif-3/arisan-circle",
     "The identical realm deploys on the Onyx testnet —",
     "deployment link in the submission."],
    "f09.png", title_size=40)

# concat list (durations in seconds; total 110s)
plan = [("f01.png", 8), ("f02.png", 14), ("f03.png", 9), ("f04.png", 13),
        ("f05.png", 13), ("f06.png", 13), ("f07.png", 16), ("f08.png", 12),
        ("f09.png", 12)]
with open(os.path.join(HERE, "concat.txt"), "w") as fh:
    for name, dur in plan:
        fh.write(f"file 'frames/{name}'\nduration {dur}\n")
    fh.write(f"file 'frames/{plan[-1][0]}'\n")
print("frames done, total duration:", sum(d for _, d in plan), "s")
