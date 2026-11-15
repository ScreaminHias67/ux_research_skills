---
name: "affinity-miro"
description: "Überträgt eine Affinity Map aus dem Skill affinity-mapping per Miro-MCP auf ein Miro-Board und liest Änderungen des Teams (verschobene Zettel, neue Titel, neue Cluster und Notizen) zurück in eine neue Map-Version."
---

# Affinity Map auf Miro

Dieser Skill bringt eine Affinity Map (`affinity-map_<projekt>_v<n>.md`, erstellt mit `affinity-mapping`) auf ein Miro-Board, damit das Team gemeinsam daran weiterarbeiten kann, und liest den Board-Stand anschließend wieder ein. Die Markdown-Map bleibt die Quelle für QS, Entwicklungsprotokoll und `research-summary`; das Board ist der gemeinsame Arbeitsraum.

Befehle:
- **Auf Miro bringen** („exportieren“, „aufs Board“) → Map-Version als neuer Board-Stand
- **Miro einlesen** („zurücklesen“, „Board übernehmen“) → Änderungsliste, nach Bestätigung neue Map-Version (`step: miro`)
- **Board aktualisieren** (nach neuem Transkript) → neue Map-Version als weiterer Stand **rechts neben** dem alten

Voraussetzungen: Miro-MCP verbunden, Python 3, `scripts/miro.py` (nur Standardbibliothek). Für den Rücksync außerdem `affinity-mapping` mit `scripts/amap.py` und `references/qs.md`.

## Board-Layout

| Ebene | Auf dem Board | Farbe |
|---|---|---|
| L0 Datenpunkt | Sticky: Text + letzte Zeile ID (`P03-007`) | gelb |
| Team-Notiz | Sticky mit ID `TEAM-001` | orange |
| L1 Insight | **Frame** mit Titel `I09`, darin blaues Titel-Sticky und die Datenpunkte | blau |
| L2 Insight-Cluster | Sticky links vor einer Reihe von L1-Frames | pink |
| L3 Thema | Sticky über einem Block von L2-Reihen | grün |
| Parkplatz / Lücken | eigene Frames; Lücken als Stickies | gelb / grau |

Eine Legende oben links nennt die Map-Version und die Regeln fürs Team: IDs nicht löschen oder ändern; verschieben, umformulieren, neue Frames und neue Zettel ohne ID sind willkommen.

Datenpunkt → Insight ist über den Frame eindeutig. L2 und L3 werden **räumlich** zugeordnet (Frame gehört zum nächsten pinken bzw. grünen Sticky darüber/links davon). Die Board-Lage gilt; nur wenn sich ein Frame gar keinem pinken Sticky zuordnen lässt, meldet das Skript das.

Tags kann das Miro-MCP nicht setzen. Personen stehen deshalb nur in der ID-Zeile. Tags, die das Team selbst setzt, werden gelesen, aber nicht ausgewertet.

## Datenschutz

Aufs Board kommt nur die **pseudonymisierte Map** – nie Transkripte, die Sprecherzuordnung (`sprecher_<projekt>.json`) oder Klarnamen. Miro ist ein eigener Anbieter: Vor dem ersten Export klären, ob echte Projektdaten dort verarbeitet werden dürfen, und das Board nur mit Beteiligten teilen.

---

## 1. Auf Miro bringen

1. **Map wählen:** neueste Version mit `qs: bestanden`. Ohne bestandene QS darauf hinweisen und erst auf Wunsch fortfahren.
2. **Board klären:** Board-URL erfragen oder anbieten, ein neues Board anzulegen. Ein neues Board nur **nach ausdrücklicher Bestätigung** anlegen (`board_create`).
3. **Platz prüfen** (nur beim ersten Export auf ein nicht leeres Board): `canvas_search` mit `result_mode="overview"`; freie Stelle wählen und als `--x0/--y0` übergeben.
4. **Export erzeugen:**
   ```bash
   python3 <skill>/scripts/miro.py export affinity-map_<p>_v<n>.md --board-url <URL> [--x0 X --y0 Y]
   ```
   Das Skript schreibt `miro-export_<p>_v<n>_teil<k>.svg` (aufgeteilt, falls groß) und die Sync-Datei `miro_<p>.json` (Board-URL, Version, Bereich). Folgeexporte landen automatisch rechts neben dem letzten Stand.
5. **Auf das Board schreiben:** Die MCP-Workflow-Stufe `canvas_get_canvas_composer_skill` (ohne `step`) aufrufen, wie das MCP es verlangt. Die Antwort verweist auf weitere Stufen (`step="design"` bzw. `"edit"`) – diese und die lange Formatbeschreibung (`step="dsl"`) **nicht laden**: Das SVG kommt fertig aus dem Skript, und `canvas_create_from_svg` nimmt es ohne diese Stufen an (getestet). Nur bei einem Formatfehler nachladen. Dann jede Datei **unverändert** per `canvas_create_from_svg` senden (Inhalt der Datei als `svg`). Nichts umformulieren, nichts neu layouten.
6. Meldet das MCP geänderte Größen, nur echte Überlappungen per `canvas_update_from_svg` beheben. Die Legende (Textfeld oben) meldet das MCP fast immer, weil ihre Höhe erst beim Rendern feststeht – sie hat 320 px Abstand nach unten und braucht keine Korrektur.
7. Im Chat: Board-Link (mit `?moveToWidget=` auf die Legende, falls die ID bekannt ist), Map-Version, Zahl der Insights und Datenpunkte.

## 2. Miro einlesen

1. **Bereich bestimmen:** `python3 <skill>/scripts/miro.py scope miro_<p>.json` → `miro_url`, `scope_x/y/width/height`, zugrunde liegende Map-Version.
2. **Board lesen:** einmal `canvas_read_as_svg` mit diesem Bereich. Nicht mehrfach lesen, nicht das ganze Board durchsuchen.
3. **Board-Stand als Datei:** Hat die Umgebung das Ergebnis selbst als Datei abgelegt (bei großen Boards), diesen Pfad verwenden – `miro.py` liest auch das JSON drumherum. Sonst das zurückgegebene `svg` **unverändert** als `miro-read_<p>_<datum>.svg` speichern (Entities wie `&lt;br /&gt;` und `&lt;p&gt;` nicht auflösen; Miro speichert Zeilenumbrüche so, und von Hand bearbeitete Zettel kommen als `<p>…</p>` zurück).
4. **Änderungsliste erzeugen:**
   ```bash
   python3 <skill>/scripts/miro.py diff affinity-map_<p>_v<n>.md miro-read_<p>_<datum>.svg \
       --transcripts transkript_<p>_T*.txt --sync miro_<p>.json
   ```
   `v<n>` ist die Version, die zuletzt exportiert wurde (steht in `scope`). Gibt es inzwischen eine neuere Map-Version, Konflikt melden und klären, bevor weitergemacht wird.
5. **Bestätigen lassen:** Änderungsliste zeigen und einmal als Ganzes per Auswahl bestätigen lassen. **Trust the humans:** Was das Team auf dem Board gebaut hat, gilt – Zuordnungen, Titel und neue Insights nicht inhaltlich hinterfragen. Rückfragen nur bei technischen Unklarheiten, gebündelt: Frame keinem Cluster zuordenbar, neuer Zettel in mehreren Transkripten gefunden, gefundenes Zitat stammt eventuell von Interviewenden.
6. **Neue Version schreiben:** derselbe Befehl mit `--apply affinity-map_<p>_v<n+1>.md`. Danach in der neuen Datei nur gezielt nacharbeiten:
   - Überblick und Job-Verteilung mit `amap.py stats` ersetzen.
   - Für neue Team-Insights (`#job/offen`) Job-Dimensionen aus den Datenpunkten bestimmen und einen kurzen VoC-Text ergänzen – als Vorschlag kennzeichnen. Team-Notizen zählen dabei wie Datenpunkte aus Interviews.
   - Rückfragen-Ergebnisse aus Schritt 5 einarbeiten.
7. **Entwicklungsprotokoll:** Eintrag „v<n+1> – Miro“ anhängen (verschoben, umformuliert, neu gebildet, aufgelöst, neue Zettel, Team-Notizen), Gesamtbild aktualisieren, Verlaufstabelle mit `amap.py trend`.
8. **QS** nach `affinity-mapping/references/qs.md`, mit `amap.py check --previous affinity-map_<p>_v<n>.md --speakers sprecher_<p>.json`. Besonderheit: **Team-Änderungen (`#team`) nicht zurücksetzen und nicht inhaltlich bewerten** – nur Mechanik prüfen.
9. Im Chat: maßgebliche Änderungen und QS-Ergebnis.

### Was mit Team-Änderungen passiert (macht `miro.py diff --apply`)

| Auf dem Board | In der neuen Map-Version |
|---|---|
| Sticky in anderen Frame verschoben | Datenpunkt wandert in den Insight; Insight `#team` + Callout „Geändert in“ mit Herkunft |
| Blauer Titel umformuliert | neuer Titel, `#team #geaendert`, alter Titel im Callout |
| Neuer Frame | neuer Insight mit neuer ID, `#team #neu #job/offen`; Titel aus dem blauen Sticky, Frame-Titel des Teams im Callout; L2/L3 nach Board-Lage |
| Frame leer oder gelöscht | Insight aufgelöst; alter Titel, Jobs und Verbleib der Datenpunkte in den methodischen Notizen |
| Neues Sticky, Text steht im Transkript | Datenpunkt mit neuer ID und Fundstelle mit Zeitstempel (Person aus dem Transkript) |
| Neues Sticky, eigener Text | `(Team-Notiz)` mit ID `team-00x` – gleichwertiger Datenpunkt, Quelle `Team` |
| Text eines Datenpunkt-Stickies geändert | Originalwortlaut bleibt; Hinweis in den methodischen Notizen |
| Sticky gelöscht oder nicht gefunden | Datenpunkt auf den Parkplatz; Hinweis in den methodischen Notizen |
| Neues Sticky im Lücken-Frame | neue Zeile unter „Lücken & offene Fragen“ |
| pinkes/grünes Sticky umformuliert oder verschoben | L2/L3 neu gebildet nach Board-Lage |

Nichts wird auf dem Board gelöscht. Der Skill sendet nie `data-deleted`.

## 3. Board aktualisieren (nach neuem Transkript)

1. Vor dem Einarbeiten eines neuen Transkripts fragt `affinity-mapping`, ob das Board zuerst eingelesen werden soll. Wenn ja: Abschnitt 2.
2. Nach der neuen Map-Version: Abschnitt 1 – der neue Stand erscheint rechts neben dem alten. Der alte bleibt als beschriftete Momentaufnahme stehen; Kommentare dort werden nicht übertragen.
3. Dem Team sagen, dass ab jetzt auf dem neuen Stand gearbeitet wird.

## Grenzen

- Kommentare, Reaktionen und Votes auf dem Board werden nicht ausgewertet.
- Räumliche L2/L3-Zuordnung folgt der Board-Lage. Liegt ein Frame ungünstig, landet er beim nächsten pinken Sticky – das Team korrigiert das auf dem Board, nicht der Skill.
- Der Lesebereich ist der Bereich des letzten Exports plus Rand. Zettel weit außerhalb werden nicht gefunden und als „vom Board entfernt“ gemeldet.

Sprache: Sprache der Map. Im Deutschen geschlechterinklusiv mit Doppelpunkt.
