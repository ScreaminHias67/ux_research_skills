#!/usr/bin/env python3
"""amap.py – Hilfsskript für den Skill affinity-mapping.

Übernimmt alles Mechanische, damit das Modell keine Tokens für Zählen,
Tabellen und Strukturprüfung verbraucht. Nur Python-Standardbibliothek.

Befehle (Details: python amap.py <befehl> -h):
  speakers     Sprecher:innen eines Transkripts erkennen, Redeanteile, Dauer,
               Zielwert für Datenpunkte; bestätigte Zuordnung speichern
  new-version  Vorversion kopieren, Markierungen des letzten Schritts entfernen,
               Frontmatter hochzählen (Grundlage für "Kopie + Edits")
  check        QS: Zitatabgleich (A1), Sprecherprüfung der Zitate,
               Struktur und Zählungen (C), Abgleich mit Vorversion
  context      Transkript-Ausschnitte pro Datenpunkt für die Prüf-Instanz
  stats        Überblickstabelle und Job-Verteilung aus der Map erzeugen
  trend        Verlaufstabelle über mehrere Map-Versionen erzeugen
"""

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from collections import Counter, OrderedDict

# --------------------------------------------------------------------------
# Konstanten
# --------------------------------------------------------------------------

CHARS_PER_MINUTE = {"de": 900, "en": 750}
TOLERANCE = 0.30
JOBS = ("funktional", "sozial", "emotional")
STEP_TAGS = ("#neu", "#bestaetigt", "#geaendert", "#widerspruch", "#robust", "#team")

TS_RE = re.compile(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?(?:[.,]\d+)?\b")
DP_ID_RE = re.compile(r"\^((?:p\d+|team)-\d+)\s*$", re.I)
INSIGHT_RE = re.compile(r"^(#{2,4})\s+(I\d+)\b\s*(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

STOP_DE = {"und", "ich", "das", "ist", "nicht", "die", "der", "wir", "auch", "mit", "dann", "also", "aber", "ein", "eine"}
STOP_EN = {"and", "the", "is", "not", "we", "also", "with", "then", "so", "but", "a", "an", "you", "it", "that"}


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


def detect_lang(text):
    words = re.findall(r"[a-zäöüß]+", text.lower())
    de = sum(w in STOP_DE for w in words)
    en = sum(w in STOP_EN for w in words)
    return "en" if en > de else "de"


def ts_seconds(m):
    a, b, c = m.group(1), m.group(2), m.group(3)
    if c is None:
        return int(a) * 60 + int(b)
    return int(a) * 3600 + int(b) * 60 + int(c)


def transcript_id(path):
    m = re.search(r"T(\d+)", os.path.basename(path), re.I)
    return "T%02d" % int(m.group(1)) if m else None


def extract_quotes(line):
    """Liefert wörtliche Zitate einer Zeile (deutsch „…“, sonst “…” oder "…")."""
    q = re.findall(r"„(.+?)“", line)
    if not q:
        q = re.findall(r"“(.+?)”", line)
    if not q:
        q = re.findall(r"\"(.+?)\"", line)
    return q


def quote_segments(quote):
    """Zerlegt ein Zitat an […] und [Ersetzung] in prüfbare Segmente."""
    out = []
    for seg in re.split(r"\[[^\]]*\]", quote):
        seg = norm(seg).strip(" .,;:…!?-–")
        if len(seg) >= 4:
            out.append(seg)
    return out


# --------------------------------------------------------------------------
# Transkript parsen (Sprecherwechsel)
# --------------------------------------------------------------------------

# "Speaker 1: Text", "[00:01:02] Anna: Text", "Anna (00:01:02): Text"
INLINE_RE = re.compile(
    r"^\s*(?:[\[(]?\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?[\])]?\s*[-–]?\s*)?"
    r"([A-Za-zÄÖÜäöüß][\wÄÖÜäöüß .'\-]{0,39}?)\s*"
    r"(?:[\[(]?\d{1,2}:\d{2}(?::\d{2})?[\])]?)?\s*:\s+(.*)$"
)
# Label in eigener Zeile: "Speaker 1  00:03" oder "Anna Müller 0:03:12"
HEADER_RE = re.compile(
    r"^\s*([A-Za-zÄÖÜäöüß][\wÄÖÜäöüß .'\-]{0,39}?)\s+[\[(]?\d{1,2}:\d{2}(?::\d{2})?[\])]?\s*$"
)
# WebVTT: "<v Anna>Text"
VTT_RE = re.compile(r"^\s*<v\s+([^>]{1,40})>(.*)$")


def parse_turns(text):
    """Zerlegt ein Transkript in Redebeiträge [(label, text, zeilennr)].

    Labels, die nur einmal vorkommen, gelten nicht als Sprecher:in (Schutz vor
    Sätzen mit Doppelpunkt). Zeilen ohne Label gehören zum vorherigen Beitrag.
    """
    lines = text.splitlines()
    cand = []
    for i, line in enumerate(lines, 1):
        label, rest = None, None
        for rx in (VTT_RE, HEADER_RE, INLINE_RE):
            m = rx.match(line)
            if m:
                label = m.group(1).strip()
                rest = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else ""
                break
        if label and len(label.split()) <= 4:
            cand.append((i, label, rest))
        else:
            cand.append((i, None, line))

    counts = Counter(c[1] for c in cand if c[1])
    valid = {l for l, n in counts.items() if n >= 2}

    turns = []
    for i, label, rest in cand:
        if label in valid:
            turns.append([label, rest, i])
        elif turns:
            line = lines[i - 1] if label else rest
            if line.strip():
                turns[-1][1] = (turns[-1][1] + " " + line.strip()).strip()
        # Text vor dem ersten Label (Kopfzeilen) wird ignoriert
    return [tuple(t) for t in turns]


def strip_meta(text):
    return TS_RE.sub("", text)


# --------------------------------------------------------------------------
# Befehl: speakers
# --------------------------------------------------------------------------

def cmd_speakers(a):
    text = read(a.transcript)
    turns = parse_turns(text)
    tid = transcript_id(a.transcript) or os.path.basename(a.transcript)
    lang = a.lang or detect_lang(text)
    cpm = CHARS_PER_MINUTE.get(lang, 900)

    # Dauer: Zeitstempel bevorzugt, sonst Zeichenzahl
    stamps = [ts_seconds(m) for m in TS_RE.finditer(text)]
    spoken = "".join(strip_meta(t[1]) for t in turns) if turns else strip_meta(text)
    chars = len(re.sub(r"\s+", " ", spoken))
    if len(stamps) >= 2 and max(stamps) - min(stamps) >= 120:
        minutes = (max(stamps) - min(stamps)) / 60
        source = "Zeitstempel"
    else:
        minutes = chars / cpm
        source = "Zeichen (%d ÷ %d/min, Sprache %s)" % (chars, cpm, lang)
    target = max(1, round(minutes))

    stats = OrderedDict()
    for label, t, ln in turns:
        s = stats.setdefault(label, {"chars": 0, "turns": 0, "questions": 0, "samples": [], "first_line": ln})
        s["chars"] += len(strip_meta(t))
        s["turns"] += 1
        s["questions"] += t.count("?")
        s.setdefault("all", []).append(t)
    for s in stats.values():
        # zwei längste Beiträge als Beispiel
        for t in sorted(s.pop("all"), key=len, reverse=True)[:2]:
            s["samples"].append(t[:90].rstrip() + ("…" if len(t) > 90 else ""))
    total = sum(s["chars"] for s in stats.values()) or 1

    # Rollenvorschlag: Interviewende fragen viel und reden wenig
    for label, s in stats.items():
        share = s["chars"] / total
        qrate = s["questions"] / max(1, s["turns"])
        s["share"] = share
        if share < 0.05:
            s["role"] = "unklar"
        elif qrate >= 0.5 and share < 0.4:
            s["role"] = "Interviewer:in"
        elif share >= 0.4:
            s["role"] = "Interviewte:r"
        else:
            s["role"] = "unklar"

    print("## Sprecherprüfung %s\n" % tid)
    if not stats:
        print("Keine Sprecherlabels erkannt. Bitte Zuordnung manuell klären "
              "(z. B. welche Absätze von wem stammen).\n")
    else:
        print("| Label | Vorschlag | Anteil | Beiträge | Fragen | Beispiel |")
        print("|---|---|---|---|---|---|")
        for label, s in stats.items():
            sample = s["samples"][0] if s["samples"] else ""
            print("| %s | %s | %d %% | %d | %d | „%s“ |" % (
                label, s["role"], round(s["share"] * 100), s["turns"], s["questions"],
                sample.replace("|", "/")))
        print()
        warn = []
        if sum(1 for s in stats.values() if s["role"] == "Interviewte:r") > 1:
            warn.append("mehrere mögliche Interviewte – Gruppeninterview oder Diarisierungsfehler?")
        if not any(s["role"] == "Interviewer:in" for s in stats.values()):
            warn.append("keine Interviewer:in eindeutig erkannt")
        if any(s["role"] == "unklar" for s in stats.values()):
            warn.append("mindestens ein Label unklar")
        for w in warn:
            print("> Hinweis: " + w)
        if warn:
            print()
    print("**Dauer:** ca. %d min (Quelle: %s)  " % (round(minutes), source))
    print("**Zielwert Datenpunkte:** ca. %d (Korridor %d–%d, Faustregel 1 min ≈ 1 Datenpunkt)" % (
        target, round(target * (1 - TOLERANCE)), round(target * (1 + TOLERANCE))))

    if a.save:
        if not a.assign:
            sys.exit("--save braucht --assign (z. B. --assign 'P03=Speaker 2')")
        data = json.loads(read(a.save)) if os.path.exists(a.save) else {}
        entry = {"participants": {}, "interviewer": a.interviewer or [], "minutes": round(minutes, 1),
                 "target_datapoints": target, "file": os.path.basename(a.transcript)}
        for item in a.assign:
            pid, _, labels = item.partition("=")
            entry["participants"][pid.strip().upper()] = [l.strip() for l in labels.split(",")]
        data[tid] = entry
        with open(a.save, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("\nZuordnung gespeichert in %s (%s)." % (a.save, tid))


# --------------------------------------------------------------------------
# Map parsen
# --------------------------------------------------------------------------

def parse_frontmatter(md):
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m:
        return fm, 0
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith(" "):
            v = re.sub(r"\s+#.*$", "", v).strip().strip('"')
            fm[k.strip()] = v
    return fm, m.end()


def parse_map(md):
    """Liefert Frontmatter, Insights, Datenpunkte, Überblickstabelle."""
    fm, _ = parse_frontmatter(md)
    insights = OrderedDict()
    dps = []
    overview = OrderedDict()
    cur, cur_level, section = None, None, None

    for ln, line in enumerate(md.splitlines(), 1):
        mi = INSIGHT_RE.match(line)
        mh = HEADING_RE.match(line)
        if mi:
            cur, cur_level = mi.group(2), len(mi.group(1))
            title = mi.group(3).strip()
            insights[cur] = {"title": title, "line": ln, "jobs": set(), "tags": set(),
                             "dps": [], "text": "", "persons": set()}
            insights[cur]["tags"].update(re.findall(r"#[\w/äöü-]+", title))
            section = "insight"
            continue
        if mh:
            level, htext = len(mh.group(1)), mh.group(2).strip()
            if cur and level <= cur_level:
                cur = None
            if level <= 2:
                low = htext.lower()
                section = ("parkplatz" if low.startswith("parkplatz") else
                           "qs" if low.startswith("qs-bericht") else
                           "overview" if low.startswith("überblick") else
                           "other")
            continue

        if section == "overview":
            mo = re.match(r"^\|\s*(I\d+)\s*\|(.*)\|\s*$", line)
            if mo:
                cols = [c.strip() for c in mo.group(2).split("|")]
                overview[mo.group(1)] = cols

        mdp = DP_ID_RE.search(line)
        if mdp and line.lstrip().startswith("-"):
            dpid = mdp.group(1).lower()
            body = line[:mdp.start()].rstrip()
            mp = re.search(r"—\s*(P\d+|Team)\b", body)
            mt = re.search(r"\b(T\d+)\b", body.split("—")[-1]) if "—" in body else None
            kind = ("team" if dpid.startswith("team") or "(Team-Notiz)" in body else
                    "paraphrase" if "(Paraphrase)" in body else
                    "beobachtung" if "(Beobachtung)" in body else
                    "zitat" if extract_quotes(body) else "unbekannt")
            dp = {"id": dpid, "line": ln, "raw": line, "body": body,
                  "person": mp.group(1).upper() if mp else None,
                  "transcript": mt.group(1).upper() if mt else None,
                  "kind": kind, "new": bool(re.search(r"·\s*neu\s*$", body)),
                  "insight": cur if section == "insight" and cur else None,
                  "parkplatz": section == "parkplatz"}
            dps.append(dp)
            if dp["insight"]:
                insights[cur]["dps"].append(dpid)
                if dp["person"] and dp["person"] != "TEAM":
                    insights[cur]["persons"].add(dp["person"])
            continue

        if cur and section == "insight":
            insights[cur]["text"] += line + "\n"
            for j in re.findall(r"#job/(\w+)", line):
                insights[cur]["jobs"].add(j.lower())
            insights[cur]["tags"].update(t for t in re.findall(r"#[\w/äöü-]+", line) if not t.startswith("#job/"))

    return fm, insights, dps, overview


def job_counts(insights):
    c = Counter()
    combos = Counter()
    for ins in insights.values():
        for j in ins["jobs"]:
            c[j] += 1
        if len(ins["jobs"]) > 1:
            combos["+".join(j for j in JOBS if j in ins["jobs"])] += 1
    return c, combos


def status_of(ins):
    t = ins["tags"]
    for tag, name in (("#neu", "neu"), ("#widerspruch", "widersprochen"), ("#geaendert", "verändert"),
                      ("#bestaetigt", "bestätigt"), ("#robust", "robust"), ("#team", "team")):
        if tag in t:
            return name
    return "–"


# --------------------------------------------------------------------------
# Befehl: stats
# --------------------------------------------------------------------------

def overview_table(insights):
    rows = ["| ID | Insight | Jobs | Datenpunkte | Personen | Status |", "|---|---|---|---|---|---|"]
    for iid, ins in insights.items():
        title = re.sub(r"\s*#[\w/äöü-]+", "", ins["title"]).strip()
        jobs = ", ".join(j for j in JOBS if j in ins["jobs"]) or "–"
        persons = ", ".join(sorted(ins["persons"])) or "–"
        status = status_of(ins)
        if len(ins["persons"]) == 1:
            status = (status + ", Einzelstimme") if status != "–" else "Einzelstimme"
        rows.append("| %s | %s | %s | %d | %s | %s |" % (iid, title, jobs, len(ins["dps"]), persons, status))
    return "\n".join(rows)


def cmd_stats(a):
    fm, insights, dps, _ = parse_map(read(a.map))
    c, combos = job_counts(insights)
    print(overview_table(insights))
    print()
    print("**Job-Verteilung** (Mehrfachzuordnung möglich): " +
          " · ".join("%s %d" % (j, c[j]) for j in JOBS))
    if combos:
        print("**Häufige Kombinationen:** " + " · ".join("%s %d" % kv for kv in combos.most_common()))
    zit = sum(1 for d in dps if d["kind"] == "zitat")
    par = sum(1 for d in dps if d["kind"] == "paraphrase")
    print("\nDatenpunkte gesamt: %d (Zitate %d, Paraphrasen %d, sonstige %d) · Parkplatz: %d · Insights: %d" % (
        len(dps), zit, par, len(dps) - zit - par, sum(d["parkplatz"] for d in dps), len(insights)))


# --------------------------------------------------------------------------
# Befehl: new-version
# --------------------------------------------------------------------------

def cmd_new_version(a):
    if os.path.exists(a.new) and not a.force:
        sys.exit("%s existiert bereits – nichts überschrieben (ggf. --force)." % a.new)
    md = read(a.prev)
    fm, end = parse_frontmatter(md)
    try:
        old_v = int(fm.get("version", "0"))
    except ValueError:
        old_v = 0
    new_v = a.version or old_v + 1
    prev_name = os.path.splitext(os.path.basename(a.prev))[0]

    head, body = md[:end], md[end:]
    head = re.sub(r"(?m)^version:.*$", "version: %d" % new_v, head)
    head = re.sub(r'(?m)^previous:.*$', 'previous: "[[%s]]"' % prev_name, head)
    if a.step:
        head = re.sub(r"(?m)^step:.*?(\s+#.*)?$", lambda m: "step: %s%s" % (a.step, m.group(1) or ""), head)
    head = re.sub(r"(?m)^qs:.*$", "qs: offen", head)

    out, skip_callout, skip_section = [], False, False
    removed = Counter()
    for line in body.splitlines():
        # alten QS-Bericht entfernen (bis zur nächsten ##-Überschrift)
        if re.match(r"^##\s+QS-Bericht", line):
            skip_section = True
            removed["QS-Bericht"] += 1
            continue
        if skip_section:
            if re.match(r"^##\s", line):
                skip_section = False
            else:
                continue
        # Schritt-Callouts entfernen: Neu in, Geändert in, Änderungen in
        if re.match(r"^>\s*\[!(tip|abstract|note)\]\s*(Neu in|Geändert in|Änderungen in)\b", line):
            skip_callout = True
            removed["Schritt-Callout"] += 1
            continue
        if skip_callout:
            if line.startswith(">"):
                continue
            skip_callout = False
            if not line.strip():
                continue
        # Status-Tags und "· neu" entfernen
        new_line = line
        for tag in STEP_TAGS:
            new_line, n = re.subn(r"\s*%s\b(?![/\w])" % re.escape(tag), "", new_line)
            removed[tag] += n
        new_line, n = re.subn(r"\s*·\s*neu(\s+\^(?:p\d+|team)-\d+\s*)$", r"\1", new_line)
        removed["· neu"] += n
        out.append(new_line)

    # Zeilen, die nur aus Tags bestanden und jetzt leer sind, zusammenfassen
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    with open(a.new, "w", encoding="utf-8") as f:
        f.write(head + text.rstrip() + "\n")
    print("Neue Version %d angelegt: %s" % (new_v, a.new))
    print("Entfernt: " + ", ".join("%s %d" % kv for kv in removed.items() if kv[1]) if removed else "Nichts entfernt.")
    print("Jetzt nur noch die Änderungen dieses Schritts per Edit einarbeiten; "
          "Überblick mit 'stats' neu erzeugen.")


# --------------------------------------------------------------------------
# Befehl: check
# --------------------------------------------------------------------------

def load_transcripts(paths):
    tr = {}
    for p in paths or []:
        tid = transcript_id(p) or os.path.basename(p)
        raw = read(p)
        tr[tid] = {"path": p, "raw": raw, "norm": norm(raw), "turns": parse_turns(raw)}
    return tr


def speaker_of_segment(seg, turns):
    labels = set()
    for label, t, _ in turns:
        if seg in norm(t):
            labels.add(label)
    return labels


def cmd_check(a):
    md = read(a.map)
    fm, insights, dps, overview = parse_map(md)
    tr = load_transcripts(a.transcripts)
    spk = json.loads(read(a.speakers)) if a.speakers else {}
    errors, warns, infos = [], [], []

    prev_dps = {}
    if a.previous:
        _, _, pd, _ = parse_map(read(a.previous))
        prev_dps = {d["id"]: d for d in pd}

    def strip_volatile(body):
        return re.sub(r"\s*·\s*neu\s*$", "", body).strip()

    # --- Abgleich mit Vorversion
    cur_ids = {d["id"] for d in dps}
    unchanged = set()
    if prev_dps:
        for pid, pdp in prev_dps.items():
            if pid not in cur_ids:
                errors.append("C  %s aus Vorversion fehlt (verloren oder gelöscht?)" % pid)
        for d in dps:
            p = prev_dps.get(d["id"])
            if p:
                if strip_volatile(p["body"]) == strip_volatile(d["body"]):
                    unchanged.add(d["id"])
                else:
                    errors.append("C  %s gegenüber Vorversion verändert" % d["id"])

    # --- A1 Zitatabgleich + Sprecherprüfung
    checked = 0
    for d in dps:
        if d["kind"] != "zitat" or d["id"] in unchanged:
            continue
        if not tr:
            break
        checked += 1
        t = tr.get(d["transcript"]) if d["transcript"] else None
        pool = [t] if t else list(tr.values())
        if not t and d["transcript"]:
            warns.append("A1 %s verweist auf %s, Transkript nicht übergeben – gegen alle geprüft" % (d["id"], d["transcript"]))
        for q in extract_quotes(d["body"]):
            for seg in quote_segments(q):
                hit = [x for x in pool if seg in x["norm"]]
                if not hit:
                    errors.append("A1 %s Zitat nicht gefunden: „%s“" % (d["id"], seg[:80]))
                    continue
                entry = spk.get(d["transcript"]) if d["transcript"] else None
                if entry and d["person"]:
                    own = set(entry["participants"].get(d["person"], []))
                    inter = set(entry.get("interviewer", []))
                    labels = speaker_of_segment(seg, hit[0]["turns"])
                    if labels and not labels & own:
                        if labels & inter:
                            errors.append("A2 %s Zitat stammt von Interviewer:in (%s), nicht von %s" % (
                                d["id"], ", ".join(sorted(labels)), d["person"]))
                        else:
                            warns.append("A2 %s Zitat bei %s gefunden, erwartet %s" % (
                                d["id"], ", ".join(sorted(labels)), d["person"]))

    # --- C Struktur
    ids = [d["id"] for d in dps]
    for dpid, n in Counter(ids).items():
        if n > 1:
            errors.append("C  %s kommt %d-mal vor" % (dpid, n))
    for d in dps:
        if d["person"] and d["person"] != "TEAM" and not d["id"].startswith(d["person"].lower() + "-"):
            errors.append("C  %s: Block-ID passt nicht zu Person %s" % (d["id"], d["person"]))
        if not d["person"]:
            warns.append("C  %s: keine Person nach „—“ erkennbar" % d["id"])
        if not d["insight"] and not d["parkplatz"]:
            errors.append("C  %s steht weder in einem Insight noch auf dem Parkplatz" % d["id"])
        if d["kind"] == "unbekannt":
            warns.append("C  %s: weder Zitat noch als (Paraphrase)/(Beobachtung)/(Team-Notiz) gekennzeichnet" % d["id"])
    by_person = {}
    for dpid in ids:
        m = re.match(r"p(\d+)-(\d+)", dpid)
        if m:
            by_person.setdefault(m.group(1), set()).add(int(m.group(2)))
    for p, nums in sorted(by_person.items()):
        gaps = sorted(set(range(1, max(nums) + 1)) - nums)
        if gaps:
            infos.append("C  P%s: Nummernlücken %s (ok, wenn Datenpunkte in der QS entfernt wurden)" % (
                p, ", ".join(map(str, gaps[:15])) + (" …" if len(gaps) > 15 else "")))

    # --- C Zählungen gegen Frontmatter und Überblick
    def fm_int(k):
        try:
            return int(fm.get(k, ""))
        except ValueError:
            return None
    if fm_int("datapoints") is not None and fm_int("datapoints") != len(dps):
        errors.append("C  Frontmatter datapoints=%s, tatsächlich %d" % (fm["datapoints"], len(dps)))
    if fm_int("voc_clusters") is not None and fm_int("voc_clusters") != len(insights):
        errors.append("C  Frontmatter voc_clusters=%s, tatsächlich %d" % (fm["voc_clusters"], len(insights)))
    for iid, ins in insights.items():
        if not ins["dps"]:
            errors.append("C  %s hat keine Datenpunkte" % iid)
        if not ins["jobs"]:
            warns.append("C  %s hat keine Job-Dimension" % iid)
        if len(ins["dps"]) >= 10:
            infos.append("   %s hat %d Datenpunkte – zeigen sich Unter-Insights?" % (iid, len(ins["dps"])))
        single = len(ins["persons"]) == 1
        marked = "Einzelstimme" in ins["text"] or "Einzelstimme" in " ".join(overview.get(iid, []))
        if single and not marked:
            warns.append("C  %s nur von %s gestützt, aber nicht als Einzelstimme markiert" % (iid, next(iter(ins["persons"]))))
        if not single and marked:
            warns.append("C  %s als Einzelstimme markiert, aber von %s gestützt" % (iid, ", ".join(sorted(ins["persons"]))))
        row = overview.get(iid)
        if row is None:
            errors.append("C  %s fehlt in der Überblickstabelle" % iid)
        elif len(row) >= 4:
            try:
                if int(row[2]) != len(ins["dps"]):
                    errors.append("C  Überblick %s: %s Datenpunkte, tatsächlich %d" % (iid, row[2], len(ins["dps"])))
            except ValueError:
                pass
            listed = set(re.findall(r"P\d+", row[3]))
            if listed != ins["persons"]:
                errors.append("C  Überblick %s: Personen %s, tatsächlich %s" % (
                    iid, ", ".join(sorted(listed)) or "–", ", ".join(sorted(ins["persons"])) or "–"))
    for iid in overview:
        if iid not in insights:
            errors.append("C  Überblick nennt %s, den es in der Map nicht gibt" % iid)
    c, _ = job_counts(insights)
    mj = re.search(r"Job-Verteilung\*\*[^:]*:\s*(.*)", md)
    if mj:
        for j in JOBS:
            mm = re.search(r"%s\s+(\d+)" % j, mj.group(1))
            if mm and int(mm.group(1)) != c[j]:
                errors.append("C  Job-Verteilung %s=%s, tatsächlich %d" % (j, mm.group(1), c[j]))

    # --- Zielwert Datenpunkte (Reflexion, kein Fehler)
    for tid, entry in spk.items():
        for pid in entry.get("participants", {}):
            n = sum(1 for d in dps if d["person"] == pid)
            tgt = entry.get("target_datapoints")
            if tgt and n and abs(n - tgt) / tgt > TOLERANCE:
                infos.append("   %s (%s): %d Datenpunkte, Zielwert ca. %d (±30 %%) – im QS-Bericht begründen "
                             "(zu grob zusammengefasst? zu fein zerlegt? wenig Substanz?)" % (pid, tid, n, tgt))

    # --- Ausgabe
    print("## QS-Skript: %s\n" % os.path.basename(a.map))
    print("Datenpunkte: %d · Insights: %d · Zitate maschinell geprüft: %d%s" % (
        len(dps), len(insights), checked,
        (" (%d unveränderte aus Vorversion übersprungen)" % len(unchanged)) if unchanged else ""))
    if not tr:
        print("Hinweis: keine Transkripte übergeben – Zitatabgleich (A1) übersprungen.")
    print()
    for title, items in (("Fehler", errors), ("Warnungen", warns), ("Hinweise", infos)):
        print("### %s (%d)" % (title, len(items)))
        for i in items:
            print("- " + i)
        print()
    print("Ergebnis Skript: %s" % ("OFFENE FEHLER" if errors else "keine Fehler"))
    sys.exit(1 if errors else 0)


# --------------------------------------------------------------------------
# Befehl: context
# --------------------------------------------------------------------------

def find_line(raw_lines, seg):
    for i, l in enumerate(raw_lines):
        if seg[:40] in norm(l):
            return i
    return None


def cmd_context(a):
    md = read(a.map)
    _, _, dps, _ = parse_map(md)
    tr = load_transcripts(a.transcripts)
    skip = set()
    if a.only_new:
        _, _, pd, _ = parse_map(read(a.only_new))
        prev = {d["id"]: re.sub(r"\s*·\s*neu\s*$", "", d["body"]).strip() for d in pd}
        skip = {d["id"] for d in dps if prev.get(d["id"]) == re.sub(r"\s*·\s*neu\s*$", "", d["body"]).strip()}
    w = a.window
    out = 0
    for d in dps:
        if d["id"] in skip or d["kind"] == "team":
            continue
        t = tr.get(d["transcript"]) if d["transcript"] else None
        print("### %s (%s)" % (d["id"], d["kind"]))
        print(d["body"].lstrip("- ").strip())
        if not t:
            print("> Transkript %s nicht übergeben\n" % d["transcript"])
            continue
        lines = t["raw"].splitlines()
        idx = None
        quotes = extract_quotes(d["body"])
        for q in quotes:
            segs = quote_segments(q)
            if segs:
                idx = find_line(lines, segs[0])
                if idx is not None:
                    break
        if idx is None:
            mz = re.search(r"Z\.\s*(\d+)", d["body"])
            if mz:
                idx = int(mz.group(1)) - 1
        if idx is None:
            mt = TS_RE.search(d["body"].split("—")[-1])
            if mt:
                want = ts_seconds(mt)
                best = None
                for i, l in enumerate(lines):
                    for m in TS_RE.finditer(l):
                        diff = abs(ts_seconds(m) - want)
                        if best is None or diff < best[0]:
                            best = (diff, i)
                idx = best[1] if best else None
        if idx is None:
            print("> Fundstelle nicht automatisch auffindbar – ganzes Transkript %s prüfen\n" % d["transcript"])
            continue
        lo, hi = max(0, idx - w), min(len(lines), idx + w + 1)
        print("```text")
        for i in range(lo, hi):
            print("%5d  %s" % (i + 1, lines[i]))
        print("```\n")
        out += 1
    print("<!-- %d Ausschnitte, %d unveränderte Datenpunkte übersprungen -->" % (out, len(skip)))


# --------------------------------------------------------------------------
# Befehl: trend
# --------------------------------------------------------------------------

def cmd_trend(a):
    print("| Version | Anlass | Neue DP | Neu | Bestätigt | Verändert | Widersprochen | Aufgelöst | Jobs (f · s · e) |")
    print("|---|---|---|---|---|---|---|---|---|")
    prev_ins = None
    prev_dp = set()
    for path in a.maps:
        fm, ins, dps, _ = parse_map(read(path))
        name = os.path.splitext(os.path.basename(path))[0]
        v = fm.get("version", "?")
        step = fm.get("step", "")
        added = fm.get("added_in_this_step", "") or fm.get("lens", "")
        anlass = added if step in ("start", "add") else "– (%s%s)" % (step, (": " + fm.get("lens", "")) if step == "recluster" else "")
        cur_dp = {d["id"] for d in dps}
        new_dp = len(cur_dp - prev_dp) if prev_ins is not None else len(cur_dp)
        cnt = Counter()
        for i in ins.values():
            s = i["tags"]
            cnt["neu"] += "#neu" in s
            cnt["best"] += "#bestaetigt" in s
            cnt["geae"] += "#geaendert" in s
            cnt["wid"] += "#widerspruch" in s
        aufg = len(set(prev_ins) - set(ins)) if prev_ins is not None else 0
        c, _ = job_counts(ins)
        first = prev_ins is None
        print("| [[%s\\|v%s]] | %s | %d | %s | %s | %s | %s | %s | %d · %d · %d |" % (
            name, v, anlass or "–", new_dp,
            len(ins) if first else cnt["neu"],
            "–" if first else cnt["best"], "–" if first else cnt["geae"],
            "–" if first else cnt["wid"], "–" if first else aufg,
            c["funktional"], c["sozial"], c["emotional"]))
        prev_ins, prev_dp = ins, cur_dp


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("speakers", help="Sprecher:innen, Dauer und Zielwert eines Transkripts")
    s.add_argument("transcript")
    s.add_argument("--lang", choices=["de", "en"], help="Sprache erzwingen (sonst automatisch)")
    s.add_argument("--save", help="JSON-Datei für die bestätigte Zuordnung (z. B. sprecher_<projekt>.json)")
    s.add_argument("--assign", action="append", help="Zuordnung 'P03=Speaker 2' (mehrere Labels mit Komma)")
    s.add_argument("--interviewer", action="append", help="Label der Interviewer:in (mehrfach möglich)")
    s.set_defaults(func=cmd_speakers)

    s = sub.add_parser("new-version", help="Vorversion kopieren und Schritt-Markierungen entfernen")
    s.add_argument("prev")
    s.add_argument("new")
    s.add_argument("--version", type=int)
    s.add_argument("--step", choices=["add", "recluster", "qs", "miro"])
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_new_version)

    s = sub.add_parser("check", help="QS-Skript: Zitate, Sprecher, Struktur, Zählungen")
    s.add_argument("map")
    s.add_argument("--transcripts", nargs="*", default=[])
    s.add_argument("--speakers", help="JSON aus 'speakers --save'")
    s.add_argument("--previous", help="Vorversion: unveränderte Datenpunkte überspringen, Verluste finden")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("context", help="Transkript-Ausschnitte pro Datenpunkt für die Prüf-Instanz")
    s.add_argument("map")
    s.add_argument("--transcripts", nargs="*", default=[])
    s.add_argument("--only-new", metavar="VORVERSION", help="nur neue/geänderte Datenpunkte ausgeben")
    s.add_argument("--window", type=int, default=3, help="Zeilen vor/nach der Fundstelle (Standard 3)")
    s.set_defaults(func=cmd_context)

    s = sub.add_parser("stats", help="Überblickstabelle und Job-Verteilung erzeugen")
    s.add_argument("map")
    s.set_defaults(func=cmd_stats)

    s = sub.add_parser("trend", help="Verlaufstabelle über Map-Versionen erzeugen")
    s.add_argument("maps", nargs="+", help="Map-Versionen in chronologischer Reihenfolge")
    s.set_defaults(func=cmd_trend)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
