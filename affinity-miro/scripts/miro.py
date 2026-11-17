#!/usr/bin/env python3
"""miro.py – Hilfsskript für den Skill affinity-miro.

Überträgt eine Affinity Map (Obsidian-Markdown aus dem Skill affinity-mapping)
in Canvas-Composer-SVG für das Miro-MCP und liest einen Board-Stand zurück.
Nur Python-Standardbibliothek.

Befehle (Details: python miro.py <befehl> -h):
  export   Map → SVG-Datei(en) für canvas_create_from_svg; führt miro_<projekt>.json
  scope    Lesebereich (scope_x/y/width/height) des letzten Exports ausgeben
  diff     Board-SVG (aus canvas_read_as_svg) mit der Map vergleichen →
           Änderungsliste; mit --apply neue Map-Version (step: miro) schreiben

Board-Layout:
  L1 Insight          = Frame "I09" mit blauem Titel-Sticky und gelben Datenpunkten;
                        Orchid (#orchid) = violettes statt blaues Titel-Sticky
  L2 Insight-Cluster  = pinkes Sticky links vor einer Reihe von L1-Frames
  L3 Thema            = grünes Sticky über einem Block von L2-Reihen
  Einzelsignale, Parkplatz, Lücken = eigene Frames; Lücken als graue Stickies
  Datenpunkt-ID (P03-007) steht als letzte Zeile im Sticky.
"""

import argparse
import datetime
import glob
import html
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import OrderedDict

# --------------------------------------------------------------------------
# Layout-Konstanten (Spacing-Skala des Miro-Styleguides)
# --------------------------------------------------------------------------

SW, SH = 350, 228          # breites Sticky
QW, QH = 199, 228          # quadratisches Sticky
GAP, PAD = 20, 32
FRAME_COLS = 2
FRAMES_PER_LINE = 3
ROW_GAP = 160
BLOCK_GAP = 320
FRAME_GAP = 160
SVG_LIMIT = 180000

COLOR = {"dp": "yellow", "team": "orange", "l1": "light_blue", "orchid": "violet", "l2": "light_pink",
         "l3": "light_green", "gap": "gray"}
COLOR_CLASS = {
    "yellow": "dp", "light_yellow": "dp", "orange": "dp",
    "light_blue": "l1", "blue": "l1", "dark_blue": "l1", "cyan": "l1",
    "violet": "l1",                     # Orchid-Titel (L1); Farbe entscheidet über #orchid
    "light_pink": "l2", "pink": "l2",
    "light_green": "l3", "green": "l3", "dark_green": "l3",
    "gray": "gap",
}
NO_L2 = "Ohne Insight-Cluster"
NO_L3 = "Ohne Thema"

DP_ID_RE = re.compile(r"\^((?:p\d+|team)-\d+)\s*$", re.I)
STICKY_ID_RE = re.compile(r"^\s*((?:P\d+|TEAM)-\d+)\s*$", re.I)
INSIGHT_RE = re.compile(r"^(#{2,4})\s+(I\d+)\b\s*(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
TRAILING = ("einzelsignale", "parkplatz", "lücken", "methodische notizen", "qs-bericht")
STEP_TAGS = ("#neu", "#bestaetigt", "#geaendert", "#widerspruch", "#robust", "#team")


# --------------------------------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------------------------------

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[„“”\"»«’‘'‚]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def quoted(t):
    return t if re.match(r"^\s*[„\"]", t) else "„%s“" % t


def clean_title(t):
    t = re.sub(r"\s*#[\w/äöü-]+", "", t).strip()
    t = re.sub(r"^Thema:\s*", "", t)
    return t.strip().strip("„“\"").strip()


def project_of(map_path):
    m = re.match(r"affinity-map_(.+)_v\d+$", os.path.splitext(os.path.basename(map_path))[0])
    return m.group(1) if m else "projekt"


def attr(s):
    """Text für ein XML-Attribut, das Miro als HTML interpretiert."""
    return html.escape(html.escape(s, quote=False), quote=True)


def parse_frontmatter(md):
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m:
        return fm, 0
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith(" "):
            fm[k.strip()] = re.sub(r"\s+#.*$", "", v).strip().strip('"')
    return fm, m.end()


def strip_step_marks(line):
    for tag in STEP_TAGS:
        line = re.sub(r"\s*%s\b(?![/\w])" % re.escape(tag), "", line)
    return re.sub(r"\s*·\s*neu(\s+\^(?:p\d+|team)-\d+\s*)$", r"\1", line)


# --------------------------------------------------------------------------
# Map in Blöcke zerlegen
# --------------------------------------------------------------------------

class MapDoc(object):
    def __init__(self, path):
        self.path = path
        self.md = read(path)
        self.fm, end = parse_frontmatter(self.md)
        self.head = self.md[:end]
        lines = self.md[end:].splitlines()
        self.prefix, self.trailing = [], OrderedDict()
        self.insights = OrderedDict()   # id -> dict(title, extra[], dps[], l2, l3, level)
        self.dp_lines = OrderedDict()   # id -> Zeile
        self.parkplatz = []             # dp ids
        self.einzelsignale = []         # dp ids
        self.gaps = []                  # Lücken-Zeilen (Text)
        self.l1_level = None
        for line in lines:
            mi = INSIGHT_RE.match(line)
            if mi:
                self.l1_level = len(mi.group(1))
                break
        self._parse(lines)

    def _parse(self, lines):
        region = "prefix"
        cur, l2, l3, tsec = None, None, None, None
        lvl = self.l1_level or 2
        for line in lines:
            mi = INSIGHT_RE.match(line)
            mh = HEADING_RE.match(line)
            if mh and not mi:
                level, text = len(mh.group(1)), mh.group(2).strip()
                low = text.lower()
                if level == 2 and low.startswith(TRAILING):
                    region, tsec, cur = "trailing", text, None
                    self.trailing[tsec] = []
                    continue
                if level == 2 and low.startswith(("überblick",)):
                    region = "prefix"
                    self.prefix.append(line)
                    continue
                if region in ("prefix", "groups") and level < lvl and level >= 2:
                    region, cur = "groups", None
                    if lvl == 4 and level == 2:
                        l3, l2 = clean_title(text), None
                    elif (lvl == 4 and level == 3) or (lvl == 3 and level == 2):
                        l2 = clean_title(text)
                    continue
            if mi:
                region = "groups"
                cur = mi.group(2)
                self.insights[cur] = {"title": clean_title(mi.group(3)), "heading_rest": mi.group(3),
                                      "extra": [], "dps": [], "l2": l2, "l3": l3,
                                      "orchid": "#orchid" in mi.group(3)}
                continue
            mdp = DP_ID_RE.search(line)
            if mdp and line.lstrip().startswith("-"):
                dpid = mdp.group(1).lower()
                self.dp_lines[dpid] = line
                if region == "groups" and cur:
                    self.insights[cur]["dps"].append(dpid)
                elif region == "trailing" and tsec.lower().startswith("einzelsignale"):
                    self.einzelsignale.append(dpid)
                elif region == "trailing" and tsec.lower().startswith("parkplatz"):
                    self.parkplatz.append(dpid)
                else:
                    self.parkplatz.append(dpid)
                continue
            if region == "prefix":
                self.prefix.append(line)
            elif region == "groups":
                if cur:
                    self.insights[cur]["extra"].append(line)
                    if re.search(r"#orchid\b", line) and not line.startswith(">"):
                        self.insights[cur]["orchid"] = True
            elif region == "trailing":
                self.trailing[tsec].append(line)
                if tsec.lower().startswith("lücken") and line.lstrip().startswith("-"):
                    self.gaps.append(line.lstrip()[1:].strip())

    def dp_content(self, dpid):
        line = self.dp_lines[dpid]
        body = DP_ID_RE.sub("", line).strip()
        body = re.sub(r"^\s*-\s*", "", body)
        return body.split(" — ")[0].strip()

    def dp_source(self, dpid):
        line = DP_ID_RE.sub("", self.dp_lines[dpid])
        return line.split(" — ", 1)[1].strip() if " — " in line else ""

    def has_l2(self):
        return any(i["l2"] for i in self.insights.values())

    def has_l3(self):
        return any(i["l3"] for i in self.insights.values())


# --------------------------------------------------------------------------
# Befehl: export
# --------------------------------------------------------------------------

def sticky(x, y, w, h, color, content, sid=None):
    return '<rect%s data-type="sticky" x="%d" y="%d" width="%d" height="%d" data-color="%s" data-content="%s" />' % (
        (' id="%s"' % sid) if sid else "", x, y, w, h, color, content)


def dp_sticky_content(doc, dpid):
    text = doc.dp_content(dpid)
    return attr(text) + "&lt;br&gt;&lt;br&gt;" + dpid.upper()


def frame_size(n_items, cols, with_title):
    rows = (n_items + cols - 1) // cols + 1           # +1 leere Reihe als Ablagefläche
    h = PAD + (SH + 32 if with_title else 0) + rows * (SH + GAP) - GAP + PAD
    w = PAD * 2 + cols * SW + (cols - 1) * GAP
    return w, h


def insight_frame(doc, iid, ins, fx, fy):
    w, h = frame_size(len(ins["dps"]), FRAME_COLS, True)
    out = ['<g id="f_%s" transform="translate(%d,%d)" data-frame="%s">' % (iid, fx, fy, iid),
           '<rect data-type="frame" x="0" y="0" width="%d" height="%d" fill="#ffffff" data-title="%s" />' % (w, h, iid),
           sticky(PAD, PAD, SW, SH, COLOR["orchid" if ins["orchid"] else "l1"], attr(ins["title"]))]
    y0 = PAD + SH + 32
    for k, dpid in enumerate(ins["dps"]):
        r, c = divmod(k, FRAME_COLS)
        color = COLOR["team"] if dpid.startswith("team") else COLOR["dp"]
        out.append(sticky(PAD + c * (SW + GAP), y0 + r * (SH + GAP), SW, SH, color, dp_sticky_content(doc, dpid)))
    out.append("</g>")
    return out, w, h


def simple_frame(title, fid, items, cols, fx, fy):
    """items: Liste (farbe, content)."""
    w, h = frame_size(len(items), cols, False)
    out = ['<g id="%s" transform="translate(%d,%d)" data-frame="%s">' % (fid, fx, fy, html.escape(title, quote=True)),
           '<rect data-type="frame" x="0" y="0" width="%d" height="%d" fill="#ffffff" data-title="%s" />' % (w, h, html.escape(title, quote=True))]
    for k, (color, content) in enumerate(items):
        r, c = divmod(k, cols)
        out.append(sticky(PAD + c * (SW + GAP), PAD + r * (SH + GAP), SW, SH, color, content))
    out.append("</g>")
    return out, w, h


def cmd_export(a):
    doc = MapDoc(a.map)
    proj = project_of(a.map)
    version = doc.fm.get("version", "?")
    map_name = os.path.splitext(os.path.basename(a.map))[0]
    sync_path = a.sync or os.path.join(os.path.dirname(os.path.abspath(a.map)), "miro_%s.json" % proj)
    sync = json.loads(read(sync_path)) if os.path.exists(sync_path) else {"board_url": None, "exports": [], "reads": []}
    if a.board_url:
        sync["board_url"] = a.board_url
    if not sync.get("board_url"):
        sys.exit("Board-URL fehlt: beim ersten Export --board-url angeben.")

    if a.x0 is not None:
        x0, y0 = a.x0, a.y0 or 0
    elif sync["exports"]:
        bx, by, bw, bh = sync["exports"][-1]["bbox"]
        x0, y0 = bx + bw + 640, by
    else:
        x0, y0 = 0, 0

    modules = []   # (svg-zeilen) je Modul, für Aufteilung in mehrere Dateien
    today = datetime.date.today().isoformat()
    legend = ("<b>%s</b><br/>Stand: %s · exportiert %s<br/>"
              "gelb = Datenpunkt · orange = Team-Notiz · blau = Insight · violett = Orchid (Insight einer Person, "
              "bewusst behalten) · pink = Insight-Cluster · "
              "grün = Thema · grau = Lücke<br/>"
              "IDs (z. B. P03-007, I09) bitte nicht löschen oder ändern. Zettel verschieben, Titel umformulieren, "
              "neue Frames und neue Zettel ohne ID sind willkommen.") % (
        html.escape(doc.fm.get("title", "Affinity Map")), html.escape(map_name), today)
    modules.append(['<textArea x="%d" y="%d" width="1600" font-size="22" font-family="noto_sans">%s</textArea>' % (
        x0, y0, legend)])

    has_l2, has_l3 = doc.has_l2(), doc.has_l3()
    # Gruppieren in Anzeige-Reihenfolge
    blocks = OrderedDict()
    for iid, ins in doc.insights.items():
        l3 = (ins["l3"] or NO_L3) if has_l3 else None
        l2 = (ins["l2"] or NO_L2) if has_l2 else None
        blocks.setdefault(l3, OrderedDict()).setdefault(l2, []).append(iid)

    y = y0 + 320
    max_x = x0 + 1600
    for l3, rows in blocks.items():
        if l3 is not None:
            modules.append([sticky(x0, y, SW, SH, COLOR["l3"], attr(l3))])
            y += SH + 64
        for l2, iids in rows.items():
            fx0 = x0
            if l2 is not None:
                modules.append([sticky(x0, y, QW, QH, COLOR["l2"], attr(l2))])
                fx0 = x0 + QW + 64
            for start in range(0, len(iids), FRAMES_PER_LINE):
                fx, line_h = fx0, 0
                for iid in iids[start:start + FRAMES_PER_LINE]:
                    svg, w, h = insight_frame(doc, iid, doc.insights[iid], fx, y + 48)
                    modules.append(svg)
                    fx += w + FRAME_GAP
                    line_h = max(line_h, h + 48)
                    max_x = max(max_x, fx)
                y += line_h + ROW_GAP
        y += BLOCK_GAP - ROW_GAP

    # Einzelsignale + Parkplatz + Lücken
    def dp_items(ids):
        return [(COLOR["team"] if d.startswith("team") else COLOR["dp"], dp_sticky_content(doc, d)) for d in ids]
    svg0, w0, h0 = simple_frame("Einzelsignale", "f_einzelsignale", dp_items(doc.einzelsignale), 4, x0, y + 48)
    modules.append(svg0)
    xp = x0 + w0 + FRAME_GAP
    svg, w, h = simple_frame("Parkplatz", "f_parkplatz", dp_items(doc.parkplatz), 4, xp, y + 48)
    modules.append(svg)
    gaps = [(COLOR["gap"], attr(g)) for g in doc.gaps]
    svg2, w2, h2 = simple_frame("Lücken & offene Fragen", "f_luecken", gaps, 2, xp + w + FRAME_GAP, y + 48)
    modules.append(svg2)
    max_x = max(max_x, xp + w + FRAME_GAP + w2)
    y_end = y + 48 + max(h0, h, h2)
    bbox = [x0, y0, max_x - x0, y_end - y0]

    # In Dateien aufteilen (Limit des MCP-Aufrufs)
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.map))
    os.makedirs(out_dir, exist_ok=True)
    parts, cur, size = [], [], 0
    for m in modules:
        chunk = "\n".join(m)
        if cur and size + len(chunk) > SVG_LIMIT:
            parts.append(cur)
            cur, size = [], 0
        cur.append(chunk)
        size += len(chunk) + 1
    if cur:
        parts.append(cur)
    files = []
    for k, p in enumerate(parts, 1):
        fn = os.path.join(out_dir, "miro-export_%s_v%s_teil%d.svg" % (proj, version, k))
        with open(fn, "w", encoding="utf-8") as f:
            f.write("<svg>\n" + "\n".join(p) + "\n</svg>\n")
        files.append(fn)

    sync["exports"].append({"version": version, "map": map_name, "date": today,
                            "origin": [x0, y0], "bbox": bbox, "files": [os.path.basename(f) for f in files]})
    with open(sync_path, "w", encoding="utf-8") as f:
        json.dump(sync, f, ensure_ascii=False, indent=2)

    n_dp = len(doc.dp_lines)
    print("Export v%s: %d Insights, %d Datenpunkte, %d Lücken → %d Datei(en)" % (
        version, len(doc.insights), n_dp, len(doc.gaps), len(files)))
    for f in files:
        print("  " + f)
    print("Bereich auf dem Board: x=%d y=%d Breite=%d Höhe=%d" % tuple(bbox))
    print("Sync-Datei: %s" % sync_path)
    print("Nächster Schritt: jede Datei unverändert mit canvas_create_from_svg an %s senden." % sync["board_url"])


# --------------------------------------------------------------------------
# Befehl: scope
# --------------------------------------------------------------------------

def cmd_scope(a):
    sync = json.loads(read(a.sync))
    if not sync.get("exports"):
        sys.exit("Noch kein Export in %s." % a.sync)
    e = sync["exports"][-1]
    x, y, w, h = e["bbox"]
    m = a.margin
    print(json.dumps({"miro_url": sync["board_url"], "scope_x": x - m, "scope_y": y - m,
                      "scope_width": w + 2 * m, "scope_height": h + 2 * m,
                      "map_version": e["version"], "map": e["map"]}, ensure_ascii=False, indent=2))


# --------------------------------------------------------------------------
# Board-SVG lesen
# --------------------------------------------------------------------------

def load_svg_text(path):
    raw = read(path).strip()
    if raw.startswith("{") or raw.startswith("["):
        data = json.loads(raw)

        def find(o):
            if isinstance(o, str) and "<svg" in o:
                return o
            if isinstance(o, dict):
                o = list(o.values())
            if isinstance(o, list):
                for v in o:
                    r = find(v)
                    if r:
                        return r
            return None
        raw = find(data) or ""
    i = raw.find("<svg")
    j = raw.rfind("</svg>")
    if i < 0 or j < 0:
        sys.exit("Keine <svg> im Board-Stand gefunden.")
    raw = raw[i:j + 6]
    raw = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", raw, count=0)
    return raw


def sticky_text(content):
    t = re.sub(r"<br\s*/?>", "\n", content or "", flags=re.I)
    t = re.sub(r"</p>\s*<p>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    lines = [l.strip() for l in t.split("\n")]
    lines = [l for l in lines if l]
    sid = None
    if lines and STICKY_ID_RE.match(lines[-1]):
        sid = STICKY_ID_RE.match(lines[-1]).group(1).lower()
        lines = lines[:-1]
    return " ".join(lines).strip(), sid


def parse_translate(t):
    m = re.search(r"translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)", t or "")
    return (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)


def abs_box(el, ox, oy):
    rb = el.get("data-rendered-bounds")
    if rb and rb != "unmeasured":
        x, y, w, h = [float(v) for v in rb.split()]
        return x, y, w, h
    return (float(el.get("x", 0)) + ox, float(el.get("y", 0)) + oy,
            float(el.get("width", 0)), float(el.get("height", 0)))


def parse_board(svg_text):
    root = ET.fromstring(svg_text)
    frames, loose = [], []

    def walk(node, ox, oy, frame):
        for el in node:
            tag = el.tag.split("}")[-1]
            if tag == "g":
                dx, dy = parse_translate(el.get("transform"))
                if el.get("data-frame") is not None or el.find("./rect[@data-type='frame']") is not None:
                    rect = el.find("./rect[@data-type='frame']")
                    fx, fy = ox + dx, oy + dy
                    fr = {"title": (el.get("data-frame") or (rect.get("data-title") if rect is not None else "") or "").strip(),
                          "x": fx, "y": fy,
                          "w": float(rect.get("width", 0)) if rect is not None else 0,
                          "h": float(rect.get("height", 0)) if rect is not None else 0,
                          "stickies": []}
                    frames.append(fr)
                    walk(el, fx, fy, fr)
                else:
                    walk(el, ox + dx, oy + dy, frame)
            elif tag == "rect" and el.get("data-type") == "sticky":
                text, sid = sticky_text(el.get("data-content", ""))
                x, y, w, h = abs_box(el, ox, oy)
                st = {"text": text, "id": sid, "color": el.get("data-color", ""),
                      "cls": COLOR_CLASS.get(el.get("data-color", ""), "other"),
                      "x": x, "y": y, "w": w, "h": h,
                      "tags": [t.strip() for t in (el.get("data-tags") or "").split(",") if t.strip()]}
                (frame["stickies"] if frame is not None else loose).append(st)
    walk(root, 0.0, 0.0, None)
    return frames, loose


# --------------------------------------------------------------------------
# Befehl: diff
# --------------------------------------------------------------------------

def transcript_hits(text, transcripts):
    """Sucht einen Sticky-Text als Zitat in den Transkripten → [(tid, zeile)]."""
    quotes = re.findall(r"„(.+?)“", text) or re.findall(r"\"(.+?)\"", text) or [text]
    hits = []
    for tid, t in transcripts.items():
        ok = True
        first_line = None
        for q in quotes:
            for seg in re.split(r"\[[^\]]*\]", q):
                seg = norm(seg).strip(" .,;:…!?-–")
                if len(seg) < 4:
                    continue
                if seg not in t["norm"]:
                    ok = False
                    break
                if first_line is None:
                    for i, l in enumerate(t["lines"], 1):
                        if seg[:40] in norm(l):
                            first_line = i
                            break
            if not ok:
                break
        if ok:
            hits.append((tid, first_line, line_timestamp(t["lines"], first_line)))
    return hits


TS_RE = re.compile(r"\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?")


def line_timestamp(lines, n):
    """Zeitstempel der Zeile n oder der nächsten Zeile davor (Folgezeilen eines Redebeitrags)."""
    if not n:
        return None
    for i in range(n - 1, -1, -1):
        m = TS_RE.match(lines[i].strip())
        if m:
            ts = m.group(1)
            return ts if ts.count(":") == 2 else "00:" + ts
    return None


def max_insight_id(map_path, exclude=None):
    """Höchste vergebene Insight-ID über alle Versionen – ohne die Zieldatei von --apply."""
    d = os.path.dirname(os.path.abspath(map_path))
    proj = project_of(map_path)
    skip = os.path.abspath(exclude) if exclude else None
    mx = 0
    for p in glob.glob(os.path.join(d, "affinity-map_%s_v*.md" % glob.escape(proj))) + [map_path]:
        if skip and os.path.abspath(p) == skip:
            continue
        for m in re.finditer(r"\bI(\d+)\b", read(p)):
            mx = max(mx, int(m.group(1)))
    return mx


def cmd_diff(a):
    doc = MapDoc(a.map)
    frames, loose = parse_board(load_svg_text(a.board))
    version = int(doc.fm.get("version", "0") or 0)
    new_v = version + 1
    transcripts = {}
    for p in a.transcripts or []:
        m = re.search(r"T(\d+)", os.path.basename(p), re.I)
        tid = "T%02d" % int(m.group(1)) if m else os.path.basename(p)
        raw = read(p)
        transcripts[tid] = {"norm": norm(raw), "lines": raw.splitlines()}
    t2p = {}
    for dpid in doc.dp_lines:
        ms = re.search(r"—\s*(P\d+)\s*·\s*(T\d+)", doc.dp_lines[dpid])
        if ms:
            t2p[ms.group(2)] = ms.group(1)

    warn, notes = [], []

    # --- Board-Version prüfen
    if a.sync and os.path.exists(a.sync):
        sync = json.loads(read(a.sync))
        if sync.get("exports"):
            bv = str(sync["exports"][-1]["version"])
            if bv != str(version):
                warn.append("Board-Stand basiert auf v%s, Map ist v%s – Änderungen könnten kollidieren." % (bv, version))

    # --- Frames klassifizieren
    l2s = sorted([s for s in loose if s["cls"] == "l2"], key=lambda s: s["y"])
    l3s = sorted([s for s in loose if s["cls"] == "l3"], key=lambda s: s["y"])
    next_id = max_insight_id(a.map, a.apply) + 1
    board_ins = OrderedDict()
    pk_board, es_board, gap_board, loose_dp = [], [], [], []
    seen_ids = {}

    for fr in sorted(frames, key=lambda f: (f["y"], f["x"])):
        low = fr["title"].lower()
        if low.startswith("parkplatz"):
            pk_board.extend(fr["stickies"])
            continue
        if low.startswith("einzelsignale"):
            es_board.extend(fr["stickies"])
            continue
        if low.startswith("lücken") or low.startswith("luecken"):
            gap_board.extend(fr["stickies"])
            continue
        mi = re.match(r"^\s*(I\d+)\b", fr["title"])
        iid = mi.group(1) if mi and mi.group(1) in doc.insights else None
        if mi and not iid:
            warn.append("Frame „%s“ nennt eine unbekannte ID – als neuer Insight behandelt." % fr["title"])
        if iid in board_ins:
            warn.append("Frame-ID %s doppelt – zweiter Frame als neuer Insight behandelt." % iid)
            iid = None
        if not iid:
            iid = "I%02d" % next_id
            next_id += 1
            is_new = True
        else:
            is_new = False
        titles = sorted([s for s in fr["stickies"] if s["cls"] == "l1"], key=lambda s: (s["y"], s["x"]))
        title = titles[0]["text"] if titles else re.sub(r"^\s*I\d+\s*", "", fr["title"]).strip() or "(ohne Titel)"
        if len(titles) > 1:
            warn.append("%s: mehrere blaue/violette Titel-Stickies – oberstes verwendet, weitere als Team-Notiz." % iid)
        orchid = bool(titles) and titles[0]["color"] == COLOR["orchid"]
        items = [s for s in fr["stickies"] if s not in titles[:1]]
        # L2/L3 räumlich
        l3 = None
        for s in l3s:
            if s["y"] <= fr["y"] + 50:
                l3 = s
        l2 = None
        for s in l2s:
            if s["y"] <= fr["y"] + 50 and s["x"] < fr["x"] and (l3 is None or s["y"] >= l3["y"]):
                l2 = s
        if l2s and l2 is None:
            warn.append("%s: keinem pinken Insight-Cluster eindeutig zuzuordnen." % iid)
        frame_label = fr["title"] if is_new and fr["title"] and not re.match(r"^\s*I\d+\s*$", fr["title"]) else None
        board_ins[iid] = {"title": title, "new": is_new, "items": items, "frame": fr, "frame_label": frame_label,
                          "orchid": orchid,
                          "l2": l2["text"] if l2 else None, "l3": l3["text"] if l3 else None}

    loose_dp = [s for s in loose if s["cls"] not in ("l2", "l3")]

    # --- Datenpunkte zuordnen
    placement = {}          # dpid -> iid | "parkplatz"
    team_new = []           # (ziel, text, vorschlag)
    edited = []
    gaps_new = []

    def take(st, target):
        if st["id"]:
            dpid = st["id"]
            if dpid not in doc.dp_lines:
                warn.append("Sticky mit unbekannter ID %s – als Team-Notiz behandelt." % dpid.upper())
                team_new.append((target, st["text"], None))
                return
            if dpid in seen_ids:
                warn.append("%s liegt doppelt auf dem Board (%s und %s) – erste Position verwendet." % (
                    dpid.upper(), seen_ids[dpid], target))
                return
            seen_ids[dpid] = target
            placement[dpid] = target
            if norm(st["text"]) != norm(doc.dp_content(dpid)):
                edited.append((dpid, st["text"]))
        elif st["text"]:
            hits = transcript_hits(st["text"], transcripts) if transcripts else []
            team_new.append((target, st["text"], hits[0] if len(hits) == 1 else (hits or None)))

    for iid, bi in board_ins.items():
        for st in sorted(bi["items"], key=lambda s: (s["y"], s["x"])):
            take(st, iid)
    for st in sorted(es_board, key=lambda s: (s["y"], s["x"])):
        take(st, "einzelsignale")
    for st in sorted(pk_board, key=lambda s: (s["y"], s["x"])):
        take(st, "parkplatz")
    for st in loose_dp:
        if st["id"] or st["text"]:
            warn.append("Sticky außerhalb aller Frames: „%s“ – auf den Parkplatz gelegt." % st["text"][:60])
            take(st, "parkplatz")
    known_gaps = {norm(g) for g in doc.gaps}
    for st in gap_board:
        if st["text"] and norm(st["text"]) not in known_gaps:
            gaps_new.append(st["text"])

    missing = [d for d in doc.dp_lines if d not in placement]
    for d in missing:
        placement[d] = "parkplatz"

    # --- Änderungen gegenüber Map bestimmen
    old_of = {}
    for iid, ins in doc.insights.items():
        for d in ins["dps"]:
            old_of[d] = iid
    for d in doc.parkplatz:
        old_of[d] = "parkplatz"
    for d in doc.einzelsignale:
        old_of[d] = "einzelsignale"
    moved = [(d, old_of.get(d), t) for d, t in placement.items() if old_of.get(d) != t and d not in missing]
    renamed = [(iid, doc.insights[iid]["title"], bi["title"]) for iid, bi in board_ins.items()
               if not bi["new"] and norm(bi["title"]) != norm(doc.insights[iid]["title"])]
    new_ins = [iid for iid, bi in board_ins.items() if bi["new"]]
    orchid_set = [iid for iid, bi in board_ins.items() if not bi["new"] and bi["orchid"] and not doc.insights[iid]["orchid"]]
    orchid_unset = [iid for iid, bi in board_ins.items() if not bi["new"] and not bi["orchid"] and doc.insights[iid]["orchid"]]
    members = {iid: [d for d, t in placement.items() if t == iid] for iid in board_ins}
    dissolved = [iid for iid in doc.insights if iid not in board_ins or not members.get(iid)]
    regroup = []
    for iid, bi in board_ins.items():
        if bi["new"]:
            continue
        o = doc.insights[iid]
        if (doc.has_l2() or l2s) and norm(o["l2"] or "") != norm(bi["l2"] or ""):
            regroup.append((iid, "L2", o["l2"], bi["l2"]))
        if (doc.has_l3() or l3s) and norm(o["l3"] or "") != norm(bi["l3"] or ""):
            regroup.append((iid, "L3", o["l3"], bi["l3"]))

    # --- Bericht
    def where(t):
        return {"parkplatz": "Parkplatz", "einzelsignale": "Einzelsignale"}.get(t, t or "–")
    print("## Änderungen auf dem Board (Basis: %s → neue Version v%d)\n" % (os.path.basename(a.map), new_v))
    sec = [
        ("Verschobene Datenpunkte", ["%s: %s → %s" % (d.upper(), where(o), where(t)) for d, o, t in moved]),
        ("Umformulierte Titel", ["%s: „%s“ → „%s“" % x for x in renamed]),
        ("Orchid gesetzt (Titel-Sticky violett gefärbt)", ["%s „%s“" % (i, board_ins[i]["title"]) for i in orchid_set]),
        ("Orchid entfernt (Titel-Sticky nicht mehr violett)", ["%s „%s“" % (i, board_ins[i]["title"]) for i in orchid_unset]),
        ("Neue Insights (vom Team gebildet)", ["%s „%s“ mit %d Zettel(n)%s%s%s" % (
            i, board_ins[i]["title"], len(members[i]) + sum(1 for t, _, _ in team_new if t == i),
            " · Orchid" if board_ins[i]["orchid"] else "",
            " · Frame „%s“" % board_ins[i]["frame_label"] if board_ins[i]["frame_label"] else "",
            "".join(" · %s: „%s“" % (lv, board_ins[i][k]) for lv, k in (("L3", "l3"), ("L2", "l2")) if board_ins[i][k]))
            for i in new_ins]),
        ("Aufgelöste Insights", ["%s „%s“%s" % (i, doc.insights[i]["title"],
                                                " (Frame noch auf dem Board, ohne Datenpunkte)" if i in board_ins else "")
                                 for i in dissolved]),
        ("Neu zugeordnet (L2/L3 nach Board-Lage)", ["%s %s: „%s“ → „%s“" % (i, lv, o or "–", n or "–") for i, lv, o, n in regroup]),
        ("Neue Zettel ohne ID", []),
        ("Zitattext auf dem Board verändert (Original bleibt)", ["%s: Board „%s“" % (d.upper(), t[:80]) for d, t in edited]),
        ("Vom Board entfernt (→ Parkplatz)", [d.upper() for d in missing]),
        ("Neue Lücken / Fragen", gaps_new),
    ]
    for target, text, hit in team_new:
        if isinstance(hit, tuple):
            pid = t2p.get(hit[0], "?")
            sec[7][1].append("in %s: %s – im Transkript %s gefunden (%s, vermutlich %s) → Datenpunkt" % (
                where(target), quoted(text[:80]), hit[0], hit[2] or "Z. %s" % hit[1], pid))
        elif isinstance(hit, list):
            sec[7][1].append("in %s: %s – in mehreren Transkripten gefunden (%s) → Rückfrage" % (
                where(target), quoted(text[:80]), ", ".join(h[0] for h in hit)))
        else:
            sec[7][1].append("in %s: %s → Team-Notiz" % (where(target), quoted(text[:80])))
    total = 0
    for title, items in sec:
        if items:
            print("### %s (%d)" % (title, len(items)))
            for i in items:
                print("- " + i)
            print()
            total += len(items)
    if not total:
        print("Keine Änderungen gegenüber der Map gefunden.\n")
    for w in warn:
        print("> Hinweis: " + w)

    if not a.apply:
        return
    if os.path.exists(a.apply) and not a.force:
        sys.exit("%s existiert bereits – nichts überschrieben (ggf. --force)." % a.apply)

    # --- neue Version schreiben
    proj = project_of(a.map)
    prev_name = os.path.splitext(os.path.basename(a.map))[0]
    head = doc.head
    head = re.sub(r"(?m)^version:.*$", "version: %d" % new_v, head)
    head = re.sub(r"(?m)^previous:.*$", 'previous: "[[%s]]"' % prev_name, head)
    head = re.sub(r"(?m)^step:.*?(\s+#.*)?$", lambda m: "step: miro%s" % (m.group(1) or ""), head)
    head = re.sub(r"(?m)^qs:.*$", "qs: offen", head)
    head = re.sub(r"(?m)^added_in_this_step:.*$", "added_in_this_step: Miro-Board", head)

    team_n = max([int(m.group(1)) for m in (re.match(r"team-(\d+)", d) for d in doc.dp_lines) if m] + [0])
    person_n = {}
    for d in doc.dp_lines:
        m = re.match(r"p(\d+)-(\d+)", d)
        if m:
            person_n[m.group(1)] = max(person_n.get(m.group(1), 0), int(m.group(2)))
    new_lines = {}          # Ziel -> [Zeilen]
    for target, text, hit in team_new:
        if isinstance(hit, tuple) and t2p.get(hit[0]):
            pid = t2p[hit[0]]
            num = pid[1:]
            person_n[num] = person_n.get(num, 0) + 1
            dpid = "p%s-%03d" % (num, person_n[num])
            q = text if re.search(r"„.+“", text) else "„%s“" % text.strip("\"")
            line = "- %s — %s · %s, %s · neu ^%s" % (q, pid, hit[0], hit[2] or "Z. %s" % hit[1], dpid)
        else:
            team_n += 1
            line = "- (Team-Notiz) %s — Team · Miro v%d · neu ^team-%03d" % (text, new_v, team_n)
        new_lines.setdefault(target, []).append(line)

    has_l2 = any(bi["l2"] and bi["l2"] != NO_L2 for bi in board_ins.values())
    has_l3 = any(bi["l3"] and bi["l3"] != NO_L3 for bi in board_ins.values())
    l1h = "#" * (2 + has_l2 + has_l3)
    moved_in = {}
    moved_out = {}
    for d, o, t in moved:
        moved_in.setdefault(t, []).append((d, o))
        moved_out.setdefault(o, []).append((d, t))

    body = []
    prefix = [l for l in doc.prefix]
    # Änderungs-Callout der Vorversion entfernen
    out_prefix, skip = [], False
    for l in prefix:
        if re.match(r"^>\s*\[!note\]\s*Änderungen in", l):
            skip = True
            continue
        if skip and l.startswith(">"):
            continue
        skip = False
        out_prefix.append(l)
    while out_prefix and (not out_prefix[-1].strip() or out_prefix[-1].strip() == "---"):
        out_prefix.pop()
    body.extend(out_prefix)
    body.append("")
    body.append("> [!note] Änderungen in v%d (Miro-Board)" % new_v)
    body.append("> %d verschobene Datenpunkte, %d umformulierte Titel, %d neue und %d aufgelöste Insights, %d neue Zettel, "
                "%d Orchid-Änderungen. Details: [[map-entwicklung_%s#v%d – Miro]]" % (
                    len(moved), len(renamed), len(new_ins), len(dissolved), len(team_new),
                    len(orchid_set) + len(orchid_unset), proj, new_v))
    body.append("")
    body.append("---")

    cur_l3, cur_l2 = object(), object()
    for iid, bi in board_ins.items():
        if not members.get(iid) and not new_lines.get(iid):
            continue
        l3 = bi["l3"] if has_l3 else None
        l2 = bi["l2"] if has_l2 else None
        if has_l3 and l3 != cur_l3:
            body += ["", "## Thema: %s" % ((l3 if l3 and l3 != NO_L3 else NO_L3))]
            cur_l3, cur_l2 = l3, object()
        if has_l2 and l2 != cur_l2:
            body += ["", "%s „%s“" % ("#" * (2 + has_l3), l2 if l2 and l2 != NO_L2 else NO_L2)]
            cur_l2 = l2
        changed = iid in moved_in or iid in moved_out or iid in new_lines
        if bi["new"]:
            label = " Frame-Titel auf dem Board: „%s“." % bi["frame_label"] if bi["frame_label"] else ""
            body += ["", "%s %s „%s“" % (l1h, iid, bi["title"]),
                     "#job/offen%s #team #neu" % (" #orchid" if bi["orchid"] else ""),
                     "> [!tip] Neu in v%d" % new_v,
                     "> Vom Team auf dem Miro-Board gebildet.%s Job-Dimensionen und VoC-Text noch festlegen." % label, ""]
            if bi["orchid"]:
                body += ["> [!example] Orchid", "> Vom Team auf dem Board als Orchid markiert (violett). "
                         "Kriterien und Begründung noch ergänzen.", ""]
        else:
            o = doc.insights[iid]
            title = bi["title"] if (iid, o["title"], bi["title"]) in renamed else o["title"]
            rest = o["heading_rest"]
            m_tags = " ".join(t for t in re.findall(r"#[\w/äöü-]+", rest)
                              if not (t == "#orchid" and iid in orchid_unset))
            body += ["", ("%s %s „%s“ %s" % (l1h, iid, title, m_tags)).rstrip()]
            extra = [strip_step_marks(l) for l in o["extra"] if l.strip() != "---"]
            # Schritt-Callouts der Vorversion entfernen; Orchid-Callout nur, wenn das Team den Orchid entfernt hat
            cleaned, skip = [], False
            for l in extra:
                if re.match(r"^>\s*\[!(tip|abstract)\]\s*(Neu in|Geändert in)\b", l) or (
                        iid in orchid_unset and re.match(r"^>\s*\[!example\]\s*Orchid", l)):
                    skip = True
                    continue
                if skip and l.startswith(">"):
                    continue
                skip = False
                cleaned.append(l)
            while cleaned and not cleaned[0].strip():
                cleaned.pop(0)
            while cleaned and not cleaned[-1].strip():
                cleaned.pop()
            renamed_here = (iid, o["title"], bi["title"]) in renamed
            orchid_here = iid in orchid_set or iid in orchid_unset
            changed = changed or orchid_here
            if cleaned and re.search(r"#job/", cleaned[0]):
                tagline = cleaned.pop(0)
            else:
                tagline = ""
            if iid in orchid_unset:
                tagline = re.sub(r"\s*#orchid\b", "", tagline)
            if iid in orchid_set and "#orchid" not in tagline:
                tagline = (tagline + " #orchid").strip()
            if renamed_here or changed:
                tagline = (tagline + " #team" + (" #geaendert" if renamed_here else "")).strip()
            if tagline:
                body.append(tagline)
            if renamed_here or changed:
                info = []
                if renamed_here:
                    info.append("Titel vom Team umformuliert; vorher: „%s“" % o["title"])
                if iid in moved_in:
                    info.append("hinzu: " + ", ".join("%s (aus %s)" % (d.upper(), where(f)) for d, f in moved_in[iid]))
                if iid in moved_out:
                    info.append("weg: " + ", ".join("%s (nach %s)" % (d.upper(), where(t)) for d, t in moved_out[iid]))
                if iid in new_lines:
                    info.append("%d neue Zettel vom Board" % len(new_lines[iid]))
                if iid in orchid_set:
                    info.append("vom Team als Orchid markiert")
                if iid in orchid_unset:
                    info.append("Orchid-Status vom Team entfernt")
                body += ["> [!abstract] Geändert in v%d (Miro)" % new_v, "> " + "; ".join(info) + "."]
                if iid in orchid_set:
                    body += ["", "> [!example] Orchid", "> Vom Team auf dem Board als Orchid markiert (violett). "
                             "Kriterien und Begründung noch ergänzen."]
            if cleaned:
                body += [""] + cleaned
            body.append("")
        for d in members.get(iid, []):
            body.append(strip_step_marks(doc.dp_lines[d]))
        body += new_lines.get(iid, [])

    method_notes = []
    for i in dissolved:
        o = doc.insights[i]
        tags = " ".join(re.findall(r"#job/[\w/äöü-]+", " ".join([o["heading_rest"]] + o["extra"])))
        where_to = ", ".join("%s → %s" % (d.upper(), where(t)) for d, t in moved_out.get(i, []))
        method_notes.append("- %s „%s“%s auf dem Miro-Board aufgelöst (v%d)%s." % (
            i, o["title"], " (%s)" % tags if tags else "", new_v, ": " + where_to if where_to else ""))
    method_notes += ["- %s wurde auf dem Miro-Board entfernt (v%d) und liegt auf dem Parkplatz." % (d.upper(), new_v)
                     for d in missing]
    method_notes += ["- %s: Text auf dem Board verändert („%s“); Originalwortlaut beibehalten." % (d.upper(), t[:80])
                     for d, t in edited]

    es_lines = [strip_step_marks(doc.dp_lines[d]) for d, t in placement.items() if t == "einzelsignale"]
    es_lines += new_lines.get("einzelsignale", [])
    body += ["", "---"]
    if es_lines or doc.einzelsignale:
        body += ["", "## Einzelsignale"] + es_lines
    body += ["", "## Parkplatz"]
    for d, t in placement.items():
        if t == "parkplatz":
            body.append(strip_step_marks(doc.dp_lines[d]))
    body += new_lines.get("parkplatz", [])

    for sec_title, lines in doc.trailing.items():
        low = sec_title.lower()
        if low.startswith(("parkplatz", "einzelsignale", "qs-bericht")):
            continue
        content = [l for l in lines if not DP_ID_RE.search(l)]
        while content and not content[-1].strip():
            content.pop()
        body += ["", "## " + sec_title] + content
        if low.startswith("lücken"):
            body += ["- (Team, Miro v%d) %s" % (new_v, g) for g in gaps_new]
        if low.startswith("methodische notizen"):
            body += method_notes
    if gaps_new and not any(k.lower().startswith("lücken") for k in doc.trailing):
        body += ["", "## Lücken & offene Fragen"] + ["- (Team, Miro v%d) %s" % (new_v, g) for g in gaps_new]
    if method_notes and not any(k.lower().startswith("methodische") for k in doc.trailing):
        body += ["", "## Methodische Notizen"] + method_notes

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)).strip() + "\n"
    n_dp = len(placement) + len(team_new)
    n_ins = sum(1 for iid in board_ins if members.get(iid) or new_lines.get(iid))
    head = re.sub(r"(?m)^datapoints:.*$", "datapoints: %d" % n_dp, head)
    head = re.sub(r"(?m)^voc_clusters:.*$", "voc_clusters: %d" % n_ins, head)
    with open(a.apply, "w", encoding="utf-8") as f:
        f.write(head + "\n" + text)
    print("\nNeue Version geschrieben: %s" % a.apply)
    print("Offen: Überblick mit 'amap.py stats' erneuern, Job-Dimensionen für #job/offen festlegen, "
          "QS (amap.py check --previous %s), Protokolleintrag „v%d – Miro“." % (os.path.basename(a.map), new_v))

    if a.sync and os.path.exists(a.sync):
        sync = json.loads(read(a.sync))
        sync.setdefault("reads", []).append({"date": datetime.date.today().isoformat(),
                                             "base": prev_name, "result": os.path.basename(a.apply)})
        with open(a.sync, "w", encoding="utf-8") as f:
            json.dump(sync, f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("export", help="Map → Canvas-Composer-SVG")
    s.add_argument("map")
    s.add_argument("--board-url", help="Miro-Board-URL (beim ersten Export Pflicht)")
    s.add_argument("--sync", help="Sync-Datei (Standard: miro_<projekt>.json neben der Map)")
    s.add_argument("--out-dir", help="Ordner für die SVG-Dateien (Standard: neben der Map)")
    s.add_argument("--x0", type=int, help="linke Kante (Standard: rechts neben dem letzten Export)")
    s.add_argument("--y0", type=int)
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("scope", help="Lesebereich des letzten Exports")
    s.add_argument("sync")
    s.add_argument("--margin", type=int, default=600)
    s.set_defaults(func=cmd_scope)

    s = sub.add_parser("diff", help="Board-Stand mit Map vergleichen, optional neue Version schreiben")
    s.add_argument("map", help="Map-Version, die zuletzt exportiert wurde")
    s.add_argument("board", help="Ergebnis von canvas_read_as_svg (SVG oder JSON mit SVG)")
    s.add_argument("--transcripts", nargs="*", default=[], help="Transkripte, um neue Zitat-Zettel zu finden")
    s.add_argument("--sync")
    s.add_argument("--apply", metavar="NEUE_MAP", help="neue Map-Version schreiben")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_diff)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
