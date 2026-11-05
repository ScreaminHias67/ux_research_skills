# Skill: research-summary

Verdichtet eine **finale Affinity Map** und das zugehörige **Entwicklungsprotokoll** (beide aus dem Skill `affinity-mapping`) zu einer kompakten **Research-Summary** mit den wichtigsten Insights. Die Summary ist der Übergabepunkt der Researchergebnisse an Team, Auftraggeber:innen oder einen Workshop.

---

## Grundhaltung: Menschen forschen, der Skill unterstützt

> [!important] Interviews führen immer Menschen
> Die Interviews müssen immer von Menschen geführt werden, die gute Fragen stellen und gut zuhören. Nachfragen, Pausen aushalten, Zwischentöne wahrnehmen und Vertrauen aufbauen kann kein Skill übernehmen – und ohne diese Qualität im Gespräch ist auch die beste Summary wenig wert.

Sinn und Zweck des Skills ist **nicht**, die Auswertung durch Menschen zu ersetzen. Er soll:
- die Aufbereitung **erleichtern**, wenn für ein gemeinsames Affinity Mapping und die Synthese im Team zu wenig Zeit ist
- die **Qualität gegenüber einfachen Transkript-Summaries erhöhen**, weil die Summary auf einer mehrstufig verdichteten, geprüften Map und ihrem dokumentierten Entwicklungsverlauf aufbaut

Die Summary ist ein Entwurf für das Research-Team: Es prüft Auswahl und Gewichtung, ergänzt sie um das eigene Erleben aus den Gesprächen und verantwortet die Übergabe.

---

## Einwilligung & Datenschutz

> [!warning] Aufzeichnung nur mit Einwilligung
> Interviews werden nur aufgezeichnet und transkribiert, wenn alle Gesprächspartner:innen vorher informiert eingewilligt haben – auch in die Auswertung mit KI-Werkzeugen. Die Einwilligung wird dokumentiert und kann jederzeit widerrufen werden.

Bei der Verarbeitung von Transkripten mit KI ist Datenschutz mitzudenken:
- **Informieren:** Vor dem Gespräch transparent machen, wozu aufgezeichnet wird, wer Zugriff hat, ob und mit welchen KI-Werkzeugen ausgewertet wird und wann die Daten gelöscht werden.
- **Freigegebene Werkzeuge nutzen:** Transkripte nur in KI-Tools und Konten verarbeiten, die für solche Daten freigegeben sind (z. B. durch Auftraggeber:in, Datenschutzbeauftragte oder einen Auftragsverarbeitungsvertrag). Vorgaben der Organisation – etwa zu Betriebsrat oder Mitarbeitendenbefragungen – vorab klären.
- **Daten minimieren:** Nur hochladen, was für die Auswertung nötig ist. Klarnamen, Namen Dritter und identifizierende Details möglichst schon vor dem Upload entfernen oder ersetzen. Die Skills pseudonymisieren die Ergebnisse, das hochgeladene Transkript wird aber vollständig verarbeitet.
- **Sensible Inhalte schützen:** Gesundheits-, Personal- oder andere besonders schutzwürdige Informationen nicht unnötig in Maps und Summaries übernehmen.
- **Sicher ablegen und löschen:** Transkripte, Maps und Summaries nur an zugriffsgeschützten Orten speichern und nach Projektende gemäß vereinbarter Fristen löschen.

Dieser Hinweis ersetzt keine Rechtsberatung. Im Zweifel die zuständigen Datenschutzbeauftragten einbeziehen.

---

## Wofür

- Ergebnisse für Menschen aufbereiten, die die Map nicht lesen werden
- Die wichtigsten Insights transparent auswählen und begründen
- Handlungsfelder öffnen, ohne Lösungen vorwegzunehmen
- Die Rückverfolgbarkeit bis zum Zitat im Transkript erhalten

---

## Aufruf

| Wunsch | Beispiel-Prompt |
|---|---|
| Standard-Summary | „/research-summary aus affinity-map_TK_DS_v4.md“ |
| Bestimmte Zielgruppe | „Summary für die Bereichsleitung, eher knapp“ |
| Kurzfassung | „Bitte als One-Pager für Slack“ |
| Workshop-Vorbereitung | „Summary als Vorbereitung für den Workshop in Hamburg“ |
| Aktualisierung | „Summary auf Basis von v5 aktualisieren“ |

Ohne Angabe nutzt der Skill die neueste Map-Version. Die Standard-Zielgruppe ist das Projektteam samt Auftraggeber:innen.

---

## Voraussetzungen

- Eine Affinity Map im Format des Skills `affinity-mapping`.
- Das **Entwicklungsprotokoll** `map-entwicklung_<projekt>.md` im selben Ordner. Es liefert Stabilität, Verlauf und Sättigung der Insights. Fehlt es, entsteht die Summary nur aus der Map, ohne den Abschnitt zur Entwicklung.
- **QS bestanden:** Im Frontmatter steht `qs: bestanden`. Fehlt das, schlägt der Skill vor, zuerst die QS laufen zu lassen. Auf Wunsch fährt er trotzdem fort und vermerkt das in der Summary.

---

## Aufbau der Summary

1. **Auf einen Blick:** drei bis fünf Kernsätze zur Forschungsfrage
2. **Forschungsfrage & Basis:** Interviews, Perspektive, Grenzen der Aussagekraft
3. **Die wichtigsten Insights** (5–8), jeweils mit:
   - Insight-IDs und Job-Dimensionen
   - Belastbarkeit
   - Erläuterung
   - ein bis zwei Originalzitaten mit Link in die Map
   - Begründung der Auswahl
4. **Jobs to be Done im Überblick:** funktional, sozial, emotional
5. **Wie sich das Bild entwickelt hat:** stabil, später sichtbar, relativiert, Sättigung (aus dem Entwicklungsprotokoll)
6. **Spannungen & Widersprüche**
7. **Was gut funktioniert:** Stärken, auf denen aufgebaut werden kann
8. **Handlungsfelder:** als „Wie könnten wir …?“-Fragen
9. **Offene Fragen & blinde Flecken:** inklusive nächster Research-Schritte
10. **Anhang:** alle Insights mit Status „in Summary ja/nein“
11. **Prüfvermerk**

---

## Wie die Top-Insights ausgewählt werden

| Kriterium | Frage |
|---|---|
| Breite | Wie viele Personen stützen den Insight? |
| Tiefe | Wie stark ist er emotional oder sozial aufgeladen? |
| Hebel | Führen andere Insights auf ihn zurück? |
| Relevanz | Wie direkt beantwortet er die Forschungsfrage? |
| Spannung | Zeigt er einen entscheidenden Zielkonflikt? |
| Stabilität | Hat er sich über mehrere Interviews gehalten (laut Entwicklungsprotokoll)? |

**Belastbarkeit:**
- **stark:** mehrere Personen, keine Widersprüche
- **mittel:** wenige Personen oder einzelne Widersprüche
- **schwach / Hypothese:** Einzelstimme, dünne Datenbasis oder erst spät entstanden

---

## Grundregeln

- **Nichts Neues behaupten:** Nur, was in der Map steht.
- **Jede Aussage hat eine Insight-ID** und ist in die Map verlinkt.
- **Zitate wortgleich aus der Map** übernehmen, mit Block-Link: `[[affinity-map_TK_DS_v4#^p01-067|P01]]`.
- **Problemraum statt Lösung:** Handlungsfelder werden als Fragen formuliert, nie als Maßnahmen.
- **Stärken nicht weglassen:** Eine Summary nur aus Problemen verzerrt das Bild.
- **Kurz:** Der Kern umfasst etwa zwei bis drei Seiten.

Vor der Auslieferung prüft der Skill:
- Jede Aussage ist durch die Map gedeckt.
- Zitate und Links stimmen.
- Die Zahlen stimmen mit der Map überein.
- Es gibt keine Lösungen und keine Klarnamen.

---

## Dateien

| Datei | Inhalt |
|---|---|
| `research-summary_<projekt>_v<n>.md` | Summary auf Basis der Map-Version n |

Bei einer Aktualisierung entsteht eine neue Datei. Sie enthält einen Abschnitt „Änderungen gegenüber Summary v<alt>“ (neue, veränderte, entfallene Top-Insights).

---

## Arbeiten in Obsidian

- Map und Summary im selben Vault ablegen, dann führen alle Links direkt zum Insight oder Zitat.
- `source_map:` im Frontmatter verlinkt die zugrunde liegende Map-Version.
- Die Tags `#job/…` sind identisch mit denen der Map, Suchen funktionieren über beide Dateien.

---

## Zusammenspiel

`affinity-mapping` → finale Map (QS bestanden) → **`research-summary`** → Übergabe an Team, Stakeholder:innen, Workshop
