---
name: research-summary
description: Verdichtet eine finale Affinity Map (Obsidian-Markdown) zu einer Research-Summary mit den wichtigsten Insights als Übergabedokument für Team und Stakeholder:innen.
---

# Research-Summary aus einer Affinity Map

Dieser Skill nimmt eine **finale Affinity Map** und das zugehörige **Entwicklungsprotokoll** `map-entwicklung_<projekt>.md` (beide erstellt mit dem Skill `affinity-mapping`) als Input und erstellt daraus eine kompakte **Research-Summary**. Sie ist der Übergabepunkt der Researchergebnisse an Team, Auftraggeber:innen oder einen Workshop. Die Summary bleibt im **Problemraum**: Sie beschreibt, was die Forschung zeigt, und öffnet Handlungsfelder als Fragen – sie liefert keine Lösungen.

Ergebnis ist eine Markdown-Datei, die in Obsidian gut lesbar ist und per Links direkt in die Map zurückführt.

---

## 1. Input prüfen

1. **Map lesen:** die angegebene Datei oder die neueste Version `affinity-map_<projekt>_v<n>.md`. Bei mehreren Versionen nennen, welche verwendet wird.
2. **QS-Status prüfen:** Steht im Frontmatter `qs: bestanden` bzw. gibt es einen bestandenen QS-Bericht? Wenn nicht: darauf hinweisen und anbieten, zuerst die QS des Skills `affinity-mapping` laufen zu lassen. Auf ausdrücklichen Wunsch trotzdem fortfahren und den fehlenden QS-Status in der Summary vermerken.
3. **Entwicklungsprotokoll lesen:** `map-entwicklung_<projekt>.md` im selben Ordner bzw. Vault. Prüfen, dass `current_version` zur verwendeten Map passt. Fehlt das Protokoll oder passt die Version nicht, darauf hinweisen; ohne Protokoll die Summary nur aus der Map erstellen, den Abschnitt „Wie sich das Bild entwickelt hat“ weglassen und das im Prüfvermerk vermerken.
4. **Kontext erfassen:** Forschungsfrage, Anzahl Interviews und Teilnehmende, Rollen, Perspektive (wer sind die „Nutzenden“?), methodische Notizen und Lücken der Map.
5. **Zielgruppe klären:** Wenn nicht genannt, ist die Standard-Zielgruppe „Projektteam und Auftraggeber:innen, die die Map nicht gelesen haben“. Auf Wunsch Varianten für Workshop-Vorbereitung oder Management.

---

## 2. Grundregeln

- **Nichts Neues behaupten:** Die Summary enthält nur, was in der Map oder im Entwicklungsprotokoll steht. Keine neuen Fakten, Zahlen, Zitate oder Deutungen, die die Map nicht trägt.
- **Jede Aussage hat eine Insight-ID:** Jede inhaltliche Aussage verweist auf mindestens einen Insight (`I06`) oder Aggregat (`L2-B`), verlinkt in die Map.
- **Zitate unverändert übernehmen:** Zitate werden exakt aus der Map kopiert, inklusive Quellenangabe, und per Block-Link verlinkt: `[[affinity-map_<projekt>_v<n>#^p01-067|P01]]`.
- **Belastbarkeit offenlegen:** Jeder Top-Insight bekommt eine Einschätzung der Belastbarkeit (siehe 3.2).
- **Problemraum statt Lösung:** Handlungsfelder als „Wie könnten wir …?“-Fragen formulieren, nie als Maßnahme.
- **Ich-Perspektive der Insights bleibt erhalten**, fließtext-Erläuterungen in neutraler Sprache.
- **Kurz:** Kern der Summary (ohne Anhang) etwa zwei bis drei Seiten. Lieber weniger Insights gut begründet als viele.
- Sprache der Map. Im Deutschen geschlechterinklusiv mit Doppelpunkt formulieren.

---

## 3. Auswahl der wichtigsten Insights

### 3.1 Auswahlkriterien
Aus allen Insights 5–8 **Top-Insights** auswählen. Bewertet wird nach:

| Kriterium | Frage |
|---|---|
| **Breite** | Von wie vielen Personen ist der Insight gestützt? |
| **Tiefe** | Wie stark ist er emotional oder sozial aufgeladen, wie viel Gewicht geben die Personen ihm? |
| **Hebel** | Führen andere Insights auf ihn zurück (Grundproblem statt Symptom)? |
| **Relevanz** | Wie direkt beantwortet er die Forschungsfrage? |
| **Spannung** | Zeigt er einen Zielkonflikt oder Widerspruch, der für die Weiterarbeit entscheidend ist? |
| **Stabilität** | Hat er sich laut Entwicklungsprotokoll über mehrere Interviews gehalten oder ist er volatil bzw. spät entstanden? |

Wo die Map L2-Aggregate hat, bevorzugt auf L2-Ebene bündeln und die tragenden L1-Insights nennen. Häufigkeit allein ist kein Grund für die Auswahl; ein stark aufgeladener Einzelbefund kann Top-Insight sein, wird dann aber als solcher gekennzeichnet.

Die Auswahl kurz begründen (ein Satz pro Top-Insight, welche Kriterien greifen).

### 3.2 Belastbarkeit
- **stark:** mehrere Personen, mehrere Datenpunkte, keine Widersprüche, laut Protokoll über mehrere Versionen stabil
- **mittel:** mehrere Datenpunkte, aber wenige Personen, einzelne Widersprüche oder volatiler Verlauf
- **schwach / Hypothese:** Einzelstimme, dünne Datenbasis oder erst in den letzten Schritten entstanden

Bei frühen Forschungsständen (wenige Interviews) die gesamte Summary als vorläufig kennzeichnen.

---

## 4. Aufbau der Summary

Dateiname: `research-summary_<projekt>_v<n>.md` (n = Version der verwendeten Map).

```markdown
---
title: Research-Summary – <Projekt>
source_map: "[[affinity-map_<projekt>_v<n>]]"
source_development: "[[map-entwicklung_<projekt>]]"
map_version: <n>
map_qs: bestanden
date: YYYY-MM-DD
research_question: "<Forschungsfrage>"
interviews: <Anzahl>
participants: <Anzahl>
audience: "<Zielgruppe>"
tags: [ux-research, research-summary, jtbd]
---

# Research-Summary – <Projekt>

> [!abstract] Auf einen Blick
> Drei bis fünf Sätze: die zentralen Erkenntnisse in Bezug auf die Forschungsfrage, jeweils mit Insight-IDs.

## Forschungsfrage & Basis
- Forschungsfrage, Zeitraum, Anzahl Interviews und Teilnehmende (Rollen, pseudonymisiert)
- Perspektive: wessen Sicht bilden die Insights ab?
- Grenzen der Aussagekraft (z. B. fehlende Perspektiven, früher Stand)

## Die wichtigsten Insights

### 1. „<Insight in Ich-Form>“
`I06` `I07` · #job/funktional #job/emotional · **Belastbarkeit:** stark

Zwei bis vier Sätze: Was zeigt sich, warum ist das wichtig, wie hängen die Job-Dimensionen zusammen?

> „Wörtliches Zitat aus der Map“ — [[affinity-map_<projekt>_v<n>#^p01-067|P01]]

*Warum ausgewählt:* Hebel – viele andere Insights führen darauf zurück; von beiden Personen gestützt.

### 2. …

## Jobs to be Done im Überblick
| Dimension | Zentrale Jobs | Insights |
|---|---|---|
| Funktional | … | I01, I06 |
| Sozial | … | I07, I17 |
| Emotional | … | I08, I09 |

Ein bis zwei Sätze zur Verteilung und zu auffälligen Kombinationen.

## Wie sich das Bild entwickelt hat
Aus dem Entwicklungsprotokoll, drei bis sechs Sätze plus kurze Listen:
- **Von Anfang an stabil:** … — I01, I06
- **Erst später sichtbar geworden:** … — I09
- **Relativiert oder gekippt:** … — I05
- **Sättigung:** neue Insights pro Interview 6 → 3 → 2; vorsichtige Einschätzung
Verweis: [[map-entwicklung_<projekt>#Gesamtbild der Entwicklung]]

## Spannungen & Widersprüche
- Zielkonflikt A vs. B — I10 ↔ I08

## Was gut funktioniert
Stärken und Ressourcen, auf denen aufgebaut werden kann — mit Insight-IDs. (Nicht weglassen: eine Summary nur aus Problemen verzerrt das Bild.)

## Handlungsfelder
Als „Wie könnten wir …?“-Fragen, jeweils mit Bezug:
- Wie könnten wir …, damit …? — I06, I07

## Offene Fragen & blinde Flecken
- Lücken aus der Map (schwach belegte Job-Dimensionen, fehlende Perspektiven) und vorgeschlagene nächste Research-Schritte

## Anhang: Alle Insights
| ID | Insight | Jobs | Personen | Belastbarkeit | In Summary |
|---|---|---|---|---|---|
| [[affinity-map_<projekt>_v<n>#I01 „…“\|I01]] | … | … | … | … | ja/nein |

## Prüfvermerk
- Basis: Map v<n>, QS-Status; Entwicklungsprotokoll Stand v<n> (oder: nicht vorhanden)
- Jede Aussage gegen die Map geprüft: ja
- Zitate wortgleich mit der Map: ja
```

---

## 5. Ablauf

1. Input prüfen (Abschnitt 1).
2. Alle Insights mit Job-Dimensionen, Personen und Datenpunktzahl erfassen; Spannungen, Widersprüche, Stärken und Lücken aus der Map sammeln; aus dem Entwicklungsprotokoll Status (stabil, volatil, spät), Erkenntnisverlauf und Sättigungseinschätzung übernehmen.
3. Top-Insights nach den Kriterien auswählen, Belastbarkeit bestimmen, Auswahl begründen.
4. Pro Top-Insight ein bis zwei Zitate wählen, die den Kern am klarsten zeigen – nicht immer die dramatischsten.
5. Summary nach Template schreiben, „Auf einen Blick“ zuletzt formulieren.
6. **Prüfung vor Auslieferung:**
   - Jede inhaltliche Aussage hat eine Insight-ID und ist durch die Map gedeckt.
   - Jedes Zitat ist wortgleich in der Map vorhanden (am besten per Skript abgleichen) und der Block-Link zeigt auf die richtige ID.
   - Keine Lösungen, nur Handlungsfelder als Fragen.
   - Belastbarkeit und Grenzen sind benannt.
   - Zahlen (Interviews, Teilnehmende, Insights) stimmen mit der Map überein; Aussagen zum Verlauf und zur Stabilität stimmen mit dem Entwicklungsprotokoll überein.
   - Keine Klarnamen.
7. Datei ausliefern und im Chat in drei bis fünf Sätzen sagen, welche Insights ausgewählt wurden und warum. Kann das Tool keine Dateien schreiben, die Summary vollständig als Markdown-Codeblock mit dem vorgesehenen Dateinamen ausgeben. Kann es keinen Code ausführen, Zitate manuell gegen die Map abgleichen und das im Prüfvermerk festhalten.

---

## 6. Varianten auf Wunsch

- **Kurzfassung** („One-Pager“, „für Mail/Slack“): nur „Auf einen Blick“, die Top-Insights als je ein Satz und die Handlungsfelder – ohne Zitate und Anhang.
- **Workshop-Vorbereitung:** Top-Insights plus Spannungen als Diskussionsimpulse, Handlungsfelder als Leitfragen für Gruppenarbeit.
- **Andere Zielgruppe:** Ton und Detailtiefe anpassen, Inhalt und Belegpflicht bleiben gleich.

Wird die Summary aktualisiert (neue Map-Version), eine neue Datei mit neuer Versionsnummer anlegen und in einem Abschnitt „Änderungen gegenüber Summary v<alt>“ benennen, welche Top-Insights neu, verändert oder entfallen sind.
