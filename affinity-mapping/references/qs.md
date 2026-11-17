# Qualitätssicherung (QS) – Details

Ziel: Jede Dateneinheit ist auf das Transkript zurückführbar, und die Map enthält keine Halluzinationen – weder erfundene Zitate noch Details, Zahlen, Wertungen oder Schlussfolgerungen, die das Material nicht trägt.

Diese Datei ist auch die Arbeitsanweisung für die Prüf-Instanz.

## Arbeitsteilung

| Wer | Was |
|---|---|
| `amap.py check` | A1 Zitatabgleich, Sprecherprüfung der Zitate, komplette Ebene C, Abgleich mit Vorversion, Zielwert-Hinweis |
| `amap.py context` | Transkript-Ausschnitte rund um jede Fundstelle für A2 |
| Prüf-Instanz oder eigener Durchgang | A2 für neue/geänderte Datenpunkte, Ebene B für neue/geänderte Verdichtungen, Klärung aller Skript-Befunde |

### Ablauf

```bash
S=<pfad-zum-skill>/scripts/amap.py
python3 $S check   affinity-map_<p>_v<n>.md --transcripts transkript_<p>_T*.txt \
                   --speakers sprecher_<p>.json --previous affinity-map_<p>_v<n-1>.md
python3 $S context affinity-map_<p>_v<n>.md --transcripts transkript_<p>_T*.txt \
                   --only-new affinity-map_<p>_v<n-1>.md > qs-kontext_v<n>.md
```

- Bei v1 bzw. dem Befehl „QS“ einzeln `--previous`/`--only-new` weglassen → alle Datenpunkte werden geprüft.
- `--previous` überspringt Datenpunkte, deren Zeile gegenüber der Vorversion **wortgleich** ist – sie wurden bereits geprüft. Jede Veränderung an einem alten Datenpunkt meldet das Skript als Fehler.
- Exit-Code 1 = offene Fehler. Jeder Fehler wird geklärt, Warnungen werden bewertet, Hinweise im QS-Bericht berücksichtigt.

### Prüf-Instanz

Wenn ein Agent-/Subagent-Tool verfügbar ist, prüft eine **separate Instanz ohne den Arbeitskontext der Erstellung**. Sie erhält nur:
1. diese Datei,
2. die neue Map-Version,
3. die Skript-Ausgabe von `check`,
4. `qs-kontext_v<n>.md` (Ausschnitte) – nicht die ganzen Transkripte. Nur wenn ein Ausschnitt meldet „Fundstelle nicht automatisch auffindbar“, liest sie die betreffende Stelle im Transkript gezielt nach.

Sie liefert eine Befundliste (ID, Art, Beleg, Korrekturvorschlag), korrigiert aber nicht selbst. A2 ist überwiegend Abgleich und darf auf einem günstigeren Modell laufen; Ebene B (Deutung) bleibt beim Hauptmodell oder einem gleichwertigen.

Ohne Subagent-Tool prüft das ausführende Modell selbst – in einem eigenen Durchgang nach Fertigstellung, jede Stelle gegen den Ausschnitt nachlesend, nie aus dem Gedächtnis.

Kann die Umgebung keinen Code ausführen: Zitate manuell Wort für Wort abgleichen, Zählungen manuell prüfen und im QS-Bericht vermerken: „ohne Skript, manuell“.

## Ebene A – Datenpunkte (L0)

**A1 Zitatabgleich** – macht das Skript. Erlaubte Abweichungen: `[…]` für Auslassungen, `[Ersetzung]` für Pseudonymisierung, Anführungszeichen, Groß-/Kleinschreibung, Leerraum. Sonst muss jedes Segment wortgleich im Transkript stehen.

**A2 Prüfung pro neuem oder geändertem Datenpunkt:**
- **Existenz:** Die Aussage steht so im Transkript.
- **Sprecher:in:** Die Aussage stammt von der angegebenen Person – nicht von Interviewenden oder einer anderen Person. Das Skript prüft Zitate anhand der bestätigten Sprecherzuordnung; Paraphrasen prüft die Prüf-Instanz. Bei offensichtlichem Diarisierungsfehler im Transkript Datenpunkt ausschließen und in den methodischen Notizen begründen.
- **Fundstelle:** Zeitstempel, Zeile oder Abschnitt § führt zur richtigen Stelle.
- **Paraphrasentreue:** Die Paraphrase fügt nichts hinzu. Jede Zahl, jeder Name, jede Zeitangabe, jede Wertung und jede Kausalbeziehung („weil“, „deshalb“) steht im Transkript. Abschwächungen („gefühlt“, „wahrscheinlich“, „ich glaube“) bleiben erhalten.
- **Klammerzusätze:** Kontext in runden Klammern ist belegt und ändert die Bedeutung nicht.
- **Sinntreue im Kontext:** keine Verwendung gegen den Zusammenhang (Ironie, Verneinung im Nachsatz, hypothetische Aussage).
- **Atomarität:** genau eine Aussage pro Datenpunkt.

**Zielwert:** Meldet das Skript eine Abweichung vom Zielwert (1 min ≈ 1 Datenpunkt, ±30 %), im QS-Bericht kurz begründen – z. B. viel Smalltalk, sehr dichte Passagen – oder prüfen, ob zu grob zusammengefasst bzw. zu fein zerlegt wurde, und nachextrahieren. **Nie Datenpunkte erzeugen oder zusammenlegen, nur um die Zahl zu treffen.**

## Ebene B – Verdichtungen (L1–L3, Callouts, Überblick)

Geprüft werden alle Insights, die in diesem Schritt neu, verändert, bestätigt oder widersprochen sind, sowie alle, deren Datenpunkte sich geändert haben. Bei re-cluster: alle.

- **Titel:** durch die Datenpunkte seines Clusters gedeckt – keine Aussage, die erst ein anderer Cluster oder Vorwissen liefert.
- **Callout-Texte:** Jede Sachbehauptung ist durch einen Datenpunkt belegt. Deutungen sind als Deutung formuliert („wirkt“, „deutet darauf hin“).
- **Job-Dimensionen:** jede vergebene Dimension durch mindestens einen konkreten Datenpunkt gestützt.
- **Orchids:** Die genannten Kriterien (a–d) sind durch die Datenpunkte belegt und die Begründung ist nachvollziehbar. Wirkt ein Orchid nur laut, nicht wertvoll, als Befund melden (Vorschlag: in Einzelsignale). Umgekehrt prüfen: Wurde bei Monoclustern wirklich versucht, sie in einen Cluster mit mehreren Origins einzuordnen, ohne den Titel zu überdehnen?
- **Einzelsignale:** Gibt es dort Datenpunkte, die inzwischen von einer zweiten Person gestützt werden und in einen Cluster gehören?
- **Herkunftsvermerke** („vereint I04 + I07“) stimmen mit den tatsächlich gewanderten Datenpunkten überein.
- **Team-Änderungen** (`#team`, aus Miro): Titel, Zuordnungen und neue Insights des Teams nicht zurücksetzen und nicht inhaltlich bewerten – die Deutungshoheit liegt beim Team. Die QS prüft hier nur Mechanik (IDs, Zitate, Zählungen).
- **Kontext, Lücken, Notizen:** Angaben über Personen und Organisation stehen im Transkript oder wurden von der Nutzer:in genannt.

## Ebene C – Struktur und Konsistenz

Erledigt `amap.py check` vollständig: eindeutige IDs, Block-ID passt zur Person, jeder Datenpunkt genau einmal (Cluster, Einzelsignale oder Parkplatz), keine verlorenen oder veränderten Datenpunkte gegenüber der Vorversion, Zählungen in Frontmatter, Überblick und Job-Verteilung, Insights ohne Job-Dimension oder ohne Datenpunkte, Hinweis bei sehr großen Clustern.

Origin-Regel (Origin = Interviewperson, Team zählt nicht):
- **Fehler:** Monocluster ohne `#orchid` (sobald mindestens zwei Personen in der Map sind); Orchid ohne `> [!example] Orchid`-Callout.
- **Warnung:** Orchid, der inzwischen von mehreren Personen gestützt wird (Status entfernen, `#bestaetigt`); mehr als etwa 15 % Orchids; Monocluster mit `#team` (vom Team gebildet – nicht zurücksetzen, nur im Bericht nennen).

Manuell zusätzlich:
- **Pseudonymisierung:** keine Klarnamen von Personen, Firmen oder Orten im gesamten Dokument.
- **Entwicklungsprotokoll:** Verlaufstabelle per `amap.py trend` erzeugt; jede Aussage im neuen Eintrag ist durch den Vergleich mit der Vorversion belegt; frühere Einträge unverändert.

## Umgang mit Befunden

- **Korrigieren, nicht kaschieren:** Zitate auf den Originalwortlaut zurücksetzen; unbelegte Details streichen; Fundstellen korrigieren; Tabellen neu mit `amap.py stats` erzeugen.
- **Nicht belegbare Datenpunkte entfernen.** Fehlt dadurch einem Cluster die Grundlage, Cluster auflösen oder Titel abschwächen.
- **Nie eine Lücke durch neue, wiederum unbelegte Formulierungen „reparieren“.**
- Nach Korrekturen `amap.py check` erneut laufen lassen.
- Nicht klärbare Grenzfälle mit `#qs/unsicher` markieren und im Bericht nennen.

## QS-Bericht

Am Ende der Map der Abschnitt **„QS-Bericht v<n>“** (Vorlage in `templates.md`), im Chat eine Kurzfassung:
- geprüfte Datenpunkte (neu / per Skript als unverändert bestätigt), Prüfmethode, separate Prüf-Instanz ja/nein
- Zielwert-Abgleich mit Begründung bei Abweichung
- Befunde nach Art und wie sie behoben wurden
- verbleibende `#qs/unsicher`-Stellen
- Ergebnis: **bestanden** (keine offenen Befunde außer markierten Unsicherheiten) oder **nicht bestanden** (dann nicht ausliefern, sondern erst korrigieren)

## Befehl „QS“ einzeln

Alle Datenpunkte und alle Insights prüfen (ohne `--previous`). Befunde korrigieren und als neue Version speichern (`amap.py new-version … --step qs`) – die geprüfte Version bleibt unverändert – und einen Eintrag „QS“ im Entwicklungsprotokoll anhängen, wenn sich Insights verändert haben. Ohne Befunde nur den Bericht im Chat ausgeben, keine neue Version.
