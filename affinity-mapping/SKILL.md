---
name: "affinity-mapping"
description: "Baut aus UX-Interviewtranskripten schrittweise und emergent eine Affinity Map (Datenpunkte → VoC-Insights → Aggregationen, JTBD) als Obsidian-Markdown; Start mit 1–2 Transkripten, Transkripte hinzufügen, re-cluster, QS."
---

# Affinity Mapping aus Interviewtranskripten

Dieser Skill verdichtet qualitative Interviewdaten **bottom-up** zu Insights. Die Map entsteht mit dem ersten oder den ersten beiden Transkripten und wird mit jedem weiteren Transkript **neu geordnet**: Insights dürfen sich verändern, aufgelöst und neu geschnitten werden – genau dieser emergente Prozess ist der Kern der Methode. Jede Version durchläuft eine **Qualitätssicherung (QS)**, damit jede Dateneinheit auf das Transkript zurückführbar ist. Wie sich das Verständnis verschiebt, hält das **Entwicklungsprotokoll** (`map-entwicklung_<projekt>.md`) fest. Referenzrahmen ist Jobs to be Done nach Clayton Christensen (funktional, sozial, emotional). Ergebnis sind Markdown-Dateien für Obsidian.

Befehle:
- **Map starten:** 1–2 Transkripte → Affinity Map v1
- **Transkript hinzufügen** („add“, „nächstes Transkript“, „einarbeiten“) → neue Version
- **re-cluster** → neue Version mit anderer Linse, ohne neue Daten
- **QS** („prüfen“, „Halluzinationscheck“) → bestehende Version erneut prüfen

Die Übertragung auf ein Miro-Board und das Zurücklesen übernimmt der Skill `affinity-miro`.

## Werkzeuge und Referenzen

- `scripts/amap.py` (Python 3, nur Standardbibliothek) erledigt alles Mechanische: Sprecherprüfung, Zielwert, neue Version anlegen, Zählungen, Tabellen, QS-Skript. **Nie von Hand zählen, wenn das Skript verfügbar ist.** Aufruf: `python3 <skill-ordner>/scripts/amap.py <befehl> -h`.
- `references/templates.md` – Vorlagen für Map und Protokoll, Markierungen. **Lesen vor v1** und vor dem Anlegen des Protokolls.
- `references/qs.md` – QS im Detail und Arbeitsanweisung für die Prüf-Instanz. **Lesen vor jeder QS.**

Ohne Codeausführung: alles manuell nach denselben Regeln, im QS-Bericht vermerken. Ohne Dateizugriff: Map und Protokoll vollständig als Markdown-Codeblock mit Dateinamen ausgeben; die Vorversion muss beim nächsten Schritt wieder bereitgestellt werden.

---

## 1. Die Ebenen

| Ebene | Name | Inhalt | Titelregel |
|---|---|---|---|
| L0 | Datenpunkt | eine atomare Aussage oder Beobachtung | kein Titel – Zitat oder enge Paraphrase + Quelle |
| L1 | Voice of the Customer | Cluster aus Datenpunkten = ein Insight | Ich-Perspektive, als Insight formuliert |
| L2 (optional) | Insight-Cluster | Cluster aus L1 | Ich-Perspektive, übergeordnet |
| L3 (optional) | Thema | Cluster aus L2 | thematische Headline, neutral |

### L0 – Datenpunkte
- **Atomar:** genau eine Aussage, ein Bedürfnis, ein Verhalten, ein Schmerzpunkt oder eine Beobachtung. Lange Passagen aufteilen.
- **Menge:** Faustregel **1 Interviewminute ≈ 1 Datenpunkt**. `amap.py speakers` nennt den Zielwert (aus Zeitstempeln, sonst ca. 900 Zeichen/min deutsch, 750 englisch). Der Zielwert ist eine Orientierung zur Selbstkontrolle, kein Soll: nie zerstückeln oder zusammenziehen, um ihn zu treffen.
- **Rückführbar:** ID und Quellenverweis (Transkript, Person, Zeitstempel oder Zeile; fehlt beides, Gesprächsabschnitt § benennen).
- **Nah am Material:** wörtliches Zitat bevorzugen; Paraphrase nur, wenn das Zitat ohne Kontext unverständlich ist – dann `(Paraphrase)`.
- **Zitierkonventionen:** Auslassungen nur `[…]`; Pseudonymisierung nur in eckigen Klammern (`[UX-Kollegin]`); Kontext nur außerhalb der Anführungszeichen in runden Klammern. Sonst kein Wort verändern, auch keine Fehler korrigieren.
- **Keine Interpretation** auf L0.
- Beobachtungen der Interviewenden (Zögern, Lachen) als `(Beobachtung)`. Aussagen der Interviewenden sind **nie** Datenpunkte.
- `(Team-Notiz)`: Ergänzungen des Teams aus Miro (Typ `^team-001`). Sie sind keine Interviewevidenz und tragen allein keinen Insight.
- **IDs:** `P01-007`, über alle Versionen stabil. Personen pseudonymisiert in Einarbeitungsreihenfolge. Klarnamen, Firmen- und Ortsangaben entfernen oder generalisieren.

### L1 – Voice of the Customer
- **Größe:** Richtwert etwa 2–7 Datenpunkte – eine Orientierung, keine Grenze. Größere Cluster sind in Ordnung, wenn sie sich inhaltlich nicht sinnvoll teilen lassen; ab etwa 10 prüfen, ob sich Unter-Insights zeigen. Ein einzelner, starker Datenpunkt darf ein eigener Cluster sein.
- Nur von einer Person gestützt → `Einzelstimme` (früh normal).
- Jeder Datenpunkt gehört zu **genau einem** Cluster. Was nicht passt, kommt auf den **Parkplatz** – nie erzwingen.
- Titel ist ein **Insight aus Nutzendenperspektive**, kein Thema, keine Lösung: „Ich möchte …, damit …“, „Immer wenn ich …, dann …“, „Ich fühle mich …, wenn …“, „Mir ist wichtig, dass andere …“, „Ich vermeide …, weil …“. Schlecht: „Navigation“, „Probleme mit dem Export“, „Ich möchte einen Button für …“.
- **Insight-ID** (`I01` …): Ein Insight behält seine ID, solange sein **Kern** gleich bleibt (Kernaussage und Großteil der Datenpunkte). Wird er neu geschnitten, bekommt er eine neue ID mit Herkunft über die Datenpunkte („vereint I04 (3 DP) + I07 (2 DP)“). IDs werden nie wiederverwendet.
- Jeder Insight bekommt eine oder mehrere Job-Dimensionen.

### L2 / L3 (optional)
- L2 nur bei echtem übergeordnetem Sinnzusammenhang (Orientierung: ab etwa 8 L1-Clustern, keine feste Schwelle). Job-Dimensionen = Vereinigungsmenge der L1.
- L3 nur bei großen Datensätzen, zur Orientierung.

## 2. Jobs to be Done

- **Funktional:** Was will die Person praktisch erledigen?
- **Sozial:** Wie will sie von anderen wahrgenommen werden, wie wirkt sie auf ihr Umfeld?
- **Emotional:** Wie will sie sich fühlen bzw. was will sie vermeiden zu fühlen?

Regeln: Ein Insight bekommt **alle** Dimensionen, die seine Datenpunkte belegen – keine erzwungene Hauptdimension, nicht „vorsichtshalber“ alle drei. Im VoC-Callout kurz benennen, wie die Dimensionen zusammenhängen. Coverage-Check: aktiv nach allen drei suchen (soziale und emotionale Jobs stecken oft in Nebensätzen und Tonfall); schwache Dimensionen unter „Lücken“ mit Folgefragen benennen – **nie** Insights erfinden, um eine Lücke zu füllen.

---

## 3. Ablauf

### Schritt 0: Sprecherprüfung – vor jeder Verarbeitung, immer
1. Transkript als Datei sichern, falls es in den Chat eingefügt wurde (`transkript_<projekt>_T01.txt`, unverändert).
2. `amap.py speakers <transkript>` ausführen. Die Tabelle (Label, Rollenvorschlag, Redeanteil, Fragen, Beispiel) plus Dauer und Zielwert der Nutzer:in zeigen und **auf Bestätigung warten** – bevorzugt mit klickbaren Auswahloptionen („passt“ / „korrigieren“). Erst danach Datenpunkte extrahieren.
3. Bestätigte Zuordnung speichern: `--save sprecher_<projekt>.json --assign "P03=<Label>" --interviewer "<Label>"`. Die Datei enthält ggf. Klarnamen und bleibt bei den Transkripten.
4. In den methodischen Notizen vermerken (nur Pseudonyme und neutrale Labels).

Bei mehreren Transkripten auf einmal: alle Sprecherprüfungen gesammelt in einer Rückfrage.

### Map starten (v1)
1. 1 oder 2 Transkripte. Bei zwei werden sie **gemeinsam** geclustert (P01, P02 in genannter Reihenfolge, sonst nach Dateiname). Werden mehr als zwei geliefert: v1 aus den ersten beiden, die übrigen danach einzeln einarbeiten; Reihenfolge vorher nennen.
2. Kontext und Forschungsfrage festhalten; fehlt sie, kurz nachfragen oder ableiten und als Annahme kennzeichnen.
3. `references/templates.md` lesen.
4. Datenpunkte extrahieren (L0), Smalltalk und Moderation weglassen.
5. Bottom-up clustern (L1) – nach Bedeutung, nicht nach Leitfaden-Fragen. Titel, Job-Dimensionen, ggf. L2/L3.
6. Map `affinity-map_<projekt>_v1.md` schreiben; Überblick und Job-Verteilung mit `amap.py stats` erzeugen.
7. Checkliste (Abschnitt 6), dann QS (Abschnitt 5).
8. Entwicklungsprotokoll mit Basiseintrag anlegen. Keine Neu-Markierungen in v1.

### Transkript hinzufügen (v<n+1>)

**Grundhaltung:** Die Vorversion ist **Ausgangslage, nicht Maßstab**. Bestehende Cluster haben keinen Bestandsschutz; Wiedererkennbarkeit ist kein Ziel. Jede Änderung und jedes Beibehalten muss sich aus den Daten begründen lassen. So wie ein Team an der Wand neue Zettel dazuhängt und dabei ganze Bereiche umbaut.

1. **Konfliktcheck:** Gibt es ein Miro-Board zu dieser Map, das neuer sein könnte, zuerst fragen, ob es eingelesen werden soll (Skill `affinity-miro`).
2. Schritt 0 (Sprecherprüfung).
3. **Neue Version anlegen:** `amap.py new-version affinity-map_<p>_v<n>.md affinity-map_<p>_v<n+1>.md --step add`. Das kopiert die Vorversion, entfernt die Markierungen des letzten Schritts und den alten QS-Bericht. Die Vorversion bleibt unverändert. Ab hier **nur gezielt editieren**, nie die ganze Map neu schreiben.
4. **Datenpunkte extrahieren** für die neue Person.
5. **Offen neu ordnen:** Neue und bestehende Datenpunkte gleichberechtigt betrachten. Für jeden bestehenden Cluster fragen: Trägt dieser Zuschnitt im Licht der neuen Daten noch, oder zeigt sich ein anderer Sinnzusammenhang? Cluster auflösen, aufspalten, zusammenführen, Datenpunkte umhängen, Titel neu formulieren, Parkplatz neu bewerten, L2/L3 neu bilden – wo die Daten es tragen.
6. **Widersprüche nicht glätten:** `> [!warning] Widerspruch` im Cluster oder als eigener Cluster.
7. **Markieren** (Tabelle in `templates.md`), `amap.py stats` für Überblick und Job-Verteilung, Frontmatter aktualisieren.
8. **Entwicklungsprotokoll** fortschreiben: neuer Schritt-Eintrag (nur anhängen), Gesamtbild neu, Verlaufstabelle mit `amap.py trend`.
9. **QS** (Abschnitt 5).
10. **Im Chat** nur die maßgeblichen Änderungen und das QS-Ergebnis.

### Entwicklungsprotokoll
Eine fortlaufende Datei pro Projekt; Input für `research-summary`. Sie beschreibt **wie sich das Verständnis verschiebt**, nicht die Inhalte. Veränderung ist kein Qualitätsmangel, Unverändertes kein Qualitätsmerkmal – beides wird neutral beschrieben.

1. **Gesamtbild** (bei jedem Schritt neu): Verlaufstabelle; „Wie sich das Bild verschoben hat“ (3–6 Sätze); Unverändert seit; Neu geschnitten; Spät entstanden; Sättigung (Zahl neuer Insights pro Transkript, vorsichtig formuliert); Verschiebung der Job-Dimensionen.
2. **Schritt-Protokoll** (chronologisch, nur anhängen): Version, Datum, Anlass, Links; neu; bestätigt; neu geschnitten mit Herkunft über Datenpunkte; Widersprüche; aufgelöst und Parkplatz-Bewegungen; Job-Verschiebung; Einschätzung in einem Satz; QS-Ergebnis.

Jede Aussage muss durch den Vergleich der Map-Versionen belegbar sein; Deutungen als Deutung formulieren. In der Map steht nur ein Verweis-Callout auf den Protokolleintrag.

## 4. re-cluster

Ziel: neue Version mit **anderen Clustern und neuen Sinnzusammenhängen**, ohne neue Transkripte.

1. `amap.py new-version … --step recluster`; L0 bleibt unverändert (gleiche Datenpunkte, IDs, Block-IDs).
2. **Linse** wählen oder die genannte verwenden, im Frontmatter `lens:` eintragen:
   - **Neu von unten:** ohne Blick auf die bestehende Struktur komplett frisch clustern
   - **Job-Dimension zuerst:** funktional / sozial / emotional + „Dimensionsübergreifend“; mehrfach zugeordnete Insights stehen vollständig an genau einer Stelle, sonst nur als Link
   - **Spannungen & Widersprüche** · **Situation / Auslöser** („Immer wenn …“) · **Journey / Phasen** · **Hürden vs. Antreiber** (Forces of Progress) · **Segmente / Rollen**
   Ohne Vorgabe eine deutlich andere Linse wählen und kurz begründen.
3. Mindestens die Hälfte der L1-Cluster neu zusammensetzen; identisch wiederkehrende als `#robust`.
4. Neue Insight-IDs und Titel nach denselben Regeln, Job-Dimensionen neu bestimmen.
5. Protokoll-Eintrag „re-cluster: <Linse>“ mit Zuordnung alter zu neuen IDs über die Datenpunkte.
6. QS mit Schwerpunkt Ebene B; das Skript prüft, dass kein Datenpunkt verändert wurde, verloren ging oder doppelt ist.

## 5. Qualitätssicherung

Pflicht bei Start, Hinzufügen und re-cluster, vor der Auslieferung. Eine Map, die die QS nicht bestanden hat, wird nicht ausgeliefert. **Details und Befehle: `references/qs.md`.**

Kurzfassung:
- **Skript** (`amap.py check` mit `--previous`): Zitatabgleich und Sprecherprüfung für neue/geänderte Datenpunkte, Unverändertheit der alten, komplette Struktur- und Zählprüfung, Zielwert-Abgleich.
- **Prüf-Instanz** (wenn Subagenten verfügbar, sonst eigener Durchgang): bekommt `qs.md`, die Map, die Skript-Ausgabe und Transkript-Ausschnitte aus `amap.py context --only-new` – nicht die ganzen Transkripte und nicht den Arbeitskontext. Prüft Paraphrasen, Sinntreue und alle neuen oder veränderten Verdichtungen.
- Befunde korrigieren, Skript erneut laufen lassen, QS-Bericht in die Map, Kurzfassung in den Chat.

## 6. Checkliste vor der QS
- Sprecherzuordnung bestätigt?
- Jeder L1-Titel in Ich-Form, Insight statt Thema, ohne Lösung, durch seine Datenpunkte gedeckt?
- Jede Job-Dimension durch Datenpunkte gestützt, Coverage-Check gemacht?
- Zitierkonventionen eingehalten?
- (Folgeschritte) Bestehende Cluster wirklich offen neu bewertet – nicht nur ergänzt? Neue IDs nur bei neuem Kern, Herkunft über Datenpunkte vermerkt?
- Nur aktuelle Änderungen markiert, Vorversion unverändert?
- Überblick und Verlauf per Skript erzeugt, Protokoll fortgeschrieben, Verweis gesetzt?

## 7. Qualitätsprinzipien

- Belegen statt behaupten: jeder Insight und jede Job-Zuordnung aus den Datenpunkten nachvollziehbar.
- Lieber weniger und belegt als mehr und ausgeschmückt.
- Häufigkeit ist nicht Relevanz.
- Emergenz statt Bestandsschutz: Die Map darf sich mit jedem Interview neu ordnen; frühe Insights sind Hypothesen.
- Widersprüche sichtbar lassen, nicht glätten.
- Die Map ist ein Arbeitsstand für das Team, keine Wahrheit – Unsicherheiten offen markieren.

Sprache: Sprache der Transkripte bzw. der Anfrage. Im Deutschen geschlechterinklusiv mit Doppelpunkt (Nutzer:innen).
