#!/usr/bin/env python3
"""Fetch Port Botany vessel movements from the Port Authority of NSW website and save
the ones at DP World's berths (Brotherson Dock 10, 11 and 12) as vessels.json.
Runs in GitHub Actions every 15 minutes. Uses only the Python standard library."""
import json, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from zoneinfo import ZoneInfo

URL = "https://www.portauthoritynsw.com.au/port-operations/port-botany/port-botany-daily-vessel-movements"
BERTHS = {"BD10", "BD11", "BD12"}
SYD = ZoneInfo("Australia/Sydney")

class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows = []; self.row = None; self.cell = None; self.depth = 0
    def handle_starttag(self, tag, attrs):
        if tag == "tr": self.row = []
        elif tag in ("td", "th") and self.row is not None: self.cell = []
        elif tag == "br" and self.cell is not None: self.cell.append(" ")
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.row is not None and self.cell is not None:
            self.row.append(re.sub(r"\s+", " ", "".join(self.cell)).strip()); self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row: self.rows.append(self.row)
            self.row = None
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)

def when(text, now):
    """'Sun 8 Nov 19:00' -> ISO time in Sydney, picking the year closest to now."""
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})[a-z]*\D+?(\d{1,2}):(\d{2})", text)
    if not m: return None
    day, mon, hh, mm = int(m.group(1)), m.group(2).title(), int(m.group(3)), int(m.group(4))
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if mon not in months: return None
    best = None
    for y in (now.year - 1, now.year, now.year + 1):
        try: d = datetime(y, months.index(mon) + 1, day, hh, mm, tzinfo=SYD)
        except ValueError: continue
        if best is None or abs(d - now) < abs(best - now): best = d
    return best.isoformat() if best else None

def berth(place):
    m = re.search(r"\((BD\d+)\)", place or "")
    return m.group(1) if m else None

def main(out):
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (personal shift app; github.com/shipwreckbay123/pbt-shifts)"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    p = Tables(); p.feed(html)
    now = datetime.now(SYD)
    head = None; moves = []; seen = set()
    for r in p.rows:
        low = [c.lower() for c in r]
        if any("vessel" == c for c in low) and any("arr" in c for c in low):
            head = low; continue
        if not head or len(r) < len(head): continue
        get = lambda name: next((r[i] for i, h in enumerate(head) if name in h), "")
        kind = get("arr").title()
        frm, to = get("from"), get("to")
        b_from, b_to = berth(frm), berth(to)
        if not ((b_from in BERTHS) or (b_to in BERTHS)): continue
        t = when(get("date"), now)
        key = (t, kind, get("vessel"))
        if key in seen: continue   # the site sometimes lists a move twice
        seen.add(key)
        moves.append({
            "time": t, "type": kind, "vessel": get("vessel").title(), "vesselType": get("type"),
            "from": frm, "to": to, "berth": b_from if b_from in BERTHS else b_to,
            "leaving": b_from in BERTHS, "expected": get("expected"), "inPort": get("in port"),
        })
    moves.sort(key=lambda m: m["time"] or "")
    data = {"updated": now.isoformat(), "source": URL, "berths": sorted(BERTHS), "moves": moves, "rowsSeen": len(p.rows)}
    with open(out, "w") as f: json.dump(data, f, indent=1)
    print(f"{len(p.rows)} table rows, {len(moves)} moves at {sorted(BERTHS)}")
    if not head: sys.exit("Couldn't find the movements table - the page layout may have changed")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vessels.json")
