# Vorlagen: Map und Entwicklungsprotokoll

Lesen, bevor die erste Map (v1) oder das Entwicklungsprotokoll angelegt wird. Folgeversionen entstehen per `amap.py new-version` aus der Vorversion und übernehmen die Struktur automatisch.

## Grundsätze

- YAML-Frontmatter für Metadaten, Überschriften-Hierarchie für die Ebenen (in Obsidian einklappbar), Tags für Job-Dimensionen und Änderungsstatus (filterbar).
- Block-IDs (`^p01-007`) **immer am Zeilenende** des Datenpunkts – `amap.py` erkennt Datenpunkte daran. Verlinkbar per `[[datei#^p01-007]]`.
- Datenpunkt-Zeile: `- <Inhalt> — <Person> · <Transkript>, <Fundstelle>[ · neu] ^<id>`. Der Gedankenstrich `—` trennt Inhalt und Quelle.
- Typen: wörtliches Zitat in `„…“` ohne Präfix; sonst `(Paraphrase)`, `(Beobachtung)` oder `(Team-Notiz)` am Anfang.
- Insight-Überschriften beginnen mit der ID: `## I09 „…“` (bzw. `###`/`####` unter L2/L3).
- Liegen die Transkripte als Dateien im Vault, Quellen als Wikilink setzen (`[[transkript_<projekt>_T01]]`).
- Ohne L2/L3: L1 als `##`. Mit L2: L2 `##`, L1 `###`. Mit L3: L3 `##`, L2 `###`, L1 `####`.

## Map

```markdown
---
title: Affinity Map – <Projekt>
version: 3
step: add            # start | add | recluster | qs | miro
lens: bottom-up
previous: "[[affinity-map_<projekt>_v2]]"
date: YYYY-MM-DD
transcripts: [T01, T02, T03]
participants: [P01, P02, P03]
added_in_this_step: T03 (P03)
research_question: "<Forschungsfrage>"
datapoints: 61
voc_clusters: 12
qs: bestanden        # bestanden | nicht bestanden | offen
tags: [ux-research, affinity-map, jtbd]
---

# Affinity Map – <Projekt>

> [!info] Kontext
> Forschungsfrage, eingearbeitete Interviews, Besonderheiten.

## Überblick

<!-- mit `amap.py stats` erzeugen, nicht von Hand zählen -->
| ID | Insight | Jobs | Datenpunkte | Personen | Status |
|---|---|---|---|---|---|
| I01 | Ich möchte … | funktional, emotional | 5 | P01, P03 | bestätigt |
| I09 | Immer wenn ich … | sozial | 3 | P03 | neu, Einzelstimme |

**Job-Verteilung** (Mehrfachzuordnung möglich): funktional 7 · sozial 4 · emotional 6
**Häufige Kombinationen:** funktional+emotional 3 · funktional+sozial 2

> [!note] Änderungen in v3 (Transkript T03)
> 2 neue, 3 neu geschnittene, 4 bestätigte Insights. Details: [[map-entwicklung_<projekt>#v3 – Transkript T03]]

---

## Thema: <L3-Headline>

### „<L2-Insight in Ich-Form>“

#### I09 „<L1-Insight in Ich-Form>“
#job/sozial #neu
> [!tip] Neu in v3
> Entstanden durch P03.

> [!quote] Voice of the Customer
> Ein bis zwei Sätze, was dieser Insight bedeutet – bei Mehrfachzuordnung: wie die Dimensionen zusammenhängen.

- „Wörtliches Zitat …“ — P03 · T03, 00:12:40 · neu ^p03-007
- (Paraphrase) Beschreibt, dass … — P01 · T01, Z. 112 ^p01-021

#### I12 „<neu geschnittener Insight>“
#job/funktional #job/emotional #geaendert
> [!abstract] Geändert in v3
> Vereint Datenpunkte aus I04 (3) und I07 (2); vorher: „<alter Titel I04>“.

- …

---

## Parkplatz
- „…“ — P02 · T02, 00:44:10 ^p02-030

## Lücken & offene Fragen
- …

## Methodische Notizen
- Sprecherzuordnung T03: „Speaker 2“ = P03, Interviewer:in „Speaker 1“ (bestätigt)
- Annahmen, Ausschlüsse, Unsicherheiten beim Clustern

## QS-Bericht v3
- **Geprüft:** 17 neue Datenpunkte (11 Zitate, 6 Paraphrasen), 44 unveränderte per Skript bestätigt; 7 geänderte/neue Insights; alle Zählungen per Skript
- **Methode:** amap.py check + context; separate Prüf-Instanz: ja
- **Zielwert:** P03 17 Datenpunkte bei ca. 38 min Interview – unter Korridor; Begründung: …
- **Befunde & Korrekturen:**
  - Wortlaut abweichend: 1 → auf Original zurückgesetzt (p03-004)
  - Callout-Behauptung unbelegt: 1 → gestrichen (I05)
- **Unsicher:** p03-019 (Transkriptstelle schwer verständlich) #qs/unsicher
- **Ergebnis:** bestanden
```

### Markierungen (nur für den aktuellen Schritt)

| Status | Markierung | Bedeutung |
|---|---|---|
| Neu | `#neu` + `> [!tip] Neu in v<n>` | Insight entstand in diesem Schritt |
| Bestätigt | `#bestaetigt` | Insight ist im Kern gleich und wird jetzt von einer weiteren Person gestützt |
| Neu geschnitten | `#geaendert` + `> [!abstract] Geändert in v<n>` mit Herkunft und altem Titel | Titel, Zuschnitt oder Job-Dimensionen geändert, aufgespalten oder zusammengeführt |
| Widersprochen | `#widerspruch` + `> [!warning] Widerspruch` | Neue Daten widersprechen dem Insight (Callout bleibt dauerhaft) |
| Robust | `#robust` | (re-cluster) Cluster kehrt unter neuer Linse identisch wieder |
| Team | `#team` | (Miro) Änderung durch das Team auf dem Board |
| Neuer Datenpunkt | `· neu` vor der Block-ID | Datenpunkt aus dem aktuellen Transkript |

`amap.py new-version` entfernt alle diese Markierungen außer dem Widerspruch-Callout.

## Entwicklungsprotokoll

```markdown
---
title: Map-Entwicklung – <Projekt>
project: <projekt>
current_version: 3
current_map: "[[affinity-map_<projekt>_v3]]"
versions: [v1, v2, v3]
transcripts: [T01, T02, T03]
updated: YYYY-MM-DD
tags: [ux-research, affinity-map, map-entwicklung]
---

# Map-Entwicklung – <Projekt>

> [!info] Wozu diese Datei
> Beschreibt, wie sich das Verständnis über die Interviews hinweg verschoben hat. Inhalte stehen in der Map, hier steht der Erkenntnisverlauf. Veränderung ist erwünscht – die Map entsteht bottom-up neu aus den Daten.

## Gesamtbild der Entwicklung
*Stand v3 – wird bei jedem Schritt neu geschrieben.*

### Verlauf
<!-- mit `amap.py trend` erzeugen -->
| Version | Anlass | Neue DP | Neu | Bestätigt | Verändert | Widersprochen | Aufgelöst | Jobs (f · s · e) |
|---|---|---|---|---|---|---|---|---|
| [[affinity-map_<projekt>_v1\|v1]] | T01 + T02 | 41 | 8 | – | – | – | – | 6 · 3 · 4 |
| [[affinity-map_<projekt>_v2\|v2]] | T03 (P03) | 17 | 2 | 4 | 3 | 1 | 1 | 8 · 4 · 6 |

### Wie sich das Bild verschoben hat
Drei bis sechs Sätze: Welche Lesart hat sich durch neue Daten verändert, welche Zusammenhänge sind neu sichtbar geworden, welche Themen tauchten erst spät auf, wo hält sich eine Lesart über mehrere Interviews.

### Unverändert seit
- I01 – seit v1 im Kern gleich, in v2 bestätigt

### Neu geschnitten
- I12 – in v2 aus I04 und I07 entstanden

### Spät entstanden
- I09 – erst in v2, Einzelstimme

### Sättigung
Neue Insights pro Transkript: 8 (v1, zwei Transkripte) → 2 → … Vorsichtige Einschätzung …

### Verschiebung der Job-Dimensionen
…

## Schritt-Protokoll
*Chronologisch, nur angehängt.*

### v1 – Transkripte T01 + T02
- **Datum:** YYYY-MM-DD · **Map:** [[affinity-map_<projekt>_v1]]
- **Basis:** 8 Insights, 41 Datenpunkte, Job-Verteilung 6 · 3 · 4, gemeinsam geclustert
- **Einschätzung:** …
- **QS:** bestanden

### v2 – Transkript T03
- **Datum:** YYYY-MM-DD · **Map:** [[affinity-map_<projekt>_v2]] · **Vorversion:** [[affinity-map_<projekt>_v1]]
- **Neu:** I09 „…“ (sozial)
- **Bestätigt:** I01, I03
- **Neu geschnitten:** I12 vereint I04 (3 DP) + I07 (2 DP) – „alt“ → „neu“; I05 um emotionale Dimension ergänzt
- **Widerspruch:** P03 widerspricht I03
- **Aufgelöst / Parkplatz:** I06 aufgelöst, Datenpunkte in I09 und I12; p01-018 vom Parkplatz in I09
- **Job-Verteilung:** soziale Dimension erstmals deutlich belegt
- **Einschätzung:** …
- **QS:** bestanden
```

## Sprecherzuordnung

`amap.py speakers … --save sprecher_<projekt>.json` legt pro Transkript die bestätigte Zuordnung ab (Labels, Interviewer:in, Dauer, Zielwert). Die Datei enthält die Original-Labels, also ggf. Klarnamen – sie gehört wie die Transkripte in einen geschützten Ordner und wird nicht verlinkt oder geteilt.
