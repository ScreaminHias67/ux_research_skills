# UX-Research-Skills für Claude

Zwei Claude-Skills, die die Auswertung qualitativer Nutzer:innen-Interviews unterstützen – von der Affinity Map bis zur Übergabe der Ergebnisse. Beide arbeiten mit Markdown-Dateien, die sich gut in [Obsidian](https://obsidian.md) lesen und verlinken lassen.

| Skill | Was er macht |
|---|---|
| [`affinity-mapping`](./affinity-mapping) | Baut aus Interviewtranskripten Schritt für Schritt eine Affinity Map – vom Datenpunkt bis zum Insight – und dokumentiert, wie sie sich mit jedem Interview verändert |
| [`research-summary`](./research-summary) | Verdichtet die finale Map und ihr Entwicklungsprotokoll zu einer kompakten Research-Summary als Übergabedokument |

> Die Skills sind auf Deutsch geschrieben und erzeugen deutschsprachige Ergebnisse (geschlechterinklusiv mit Doppelpunkt). Bei Transkripten in anderen Sprachen arbeiten sie in deren Sprache.

---

## Grundhaltung: Menschen forschen, die Skills unterstützen

**Interviews führen immer Menschen** – Menschen, die gute Fragen stellen und gut zuhören. Nachfragen, Pausen aushalten, Zwischentöne wahrnehmen und Vertrauen aufbauen kann kein Skill übernehmen.

Die Skills ersetzen die Auswertung durch Menschen **nicht**. Sie sollen:
- die Auswertung **erleichtern**, wenn für ein gemeinsames Affinity Mapping im Team zu wenig Zeit ist
- die **Qualität gegenüber einfachen Transkript-Summaries erhöhen**, weil das Material mehrstufig, nachvollziehbar und gegen das Original geprüft verdichtet wird

Maps und Summaries sind Arbeitsstände. Die Deutungshoheit bleibt bei den Menschen, die die Interviews geführt haben.

## Einwilligung & Datenschutz

- **Aufzeichnung nur mit Einwilligung:** Interviews werden nur aufgezeichnet und transkribiert, wenn alle Gesprächspartner:innen vorher informiert eingewilligt haben – auch in die Auswertung mit KI.
- **Datenschutz mitdenken:** Transkripte nur in dafür freigegebenen KI-Werkzeugen verarbeiten, identifizierende Angaben möglichst vor dem Upload entfernen, sensible Inhalte nicht unnötig übernehmen, Ergebnisse geschützt ablegen und fristgerecht löschen.

Details stehen in den READMEs der beiden Skills. Diese Hinweise ersetzen keine Rechtsberatung – im Zweifel die zuständigen Datenschutzbeauftragten einbeziehen.

---

## Wie die Skills zusammenspielen

```mermaid
flowchart LR
    T1[Transkript 1] --> M1[Map v1]
    T2[Transkript 2] --> M2[Map v2]
    Tn[Transkript n] --> Mn[Map vn]
    M1 --> M2 --> Mn
    M1 -.-> E[Entwicklungsprotokoll]
    M2 -.-> E
    Mn -.-> E
    Mn --> S[Research-Summary]
    E --> S
```

1. **`affinity-mapping`** startet mit dem ersten Transkript (v1) und arbeitet jedes weitere einzeln ein. Jede Version wird gegen die Transkripte geprüft; alle Änderungen landen im Entwicklungsprotokoll.
2. **`research-summary`** nimmt die finale, geprüfte Map und das Entwicklungsprotokoll und erstellt daraus die Übergabe an Team, Auftraggeber:innen oder einen Workshop.

---

## affinity-mapping

**Ebenen**

| Ebene | Inhalt |
|---|---|
| L0 Datenpunkt | atomares Zitat oder gekennzeichnete Paraphrase mit ID und Fundstelle |
| L1 Voice of the Customer | Cluster aus Datenpunkten, Titel als Insight in Ich-Form („Ich möchte …, damit …“) |
| L2 Insight-Cluster *(optional)* | übergeordneter Insight in Ich-Form |
| L3 Thema *(optional)* | thematische Headline |

**Kernfunktionen**
- **Jobs to be Done** nach Clayton Christensen als Referenzrahmen: Jeder Insight ist einer oder mehreren Dimensionen zugeordnet – funktional, sozial, emotional – inklusive Coverage-Check
- **Schrittweiser Aufbau:** pro Transkript eine neue Version, Markierungen für neue, bestätigte, veränderte und widersprochene Insights
- **Entwicklungsprotokoll:** beschreibt auf einer Metaebene, wie sich die Map verändert – stabile, volatile und spät entstandene Insights, Insight-Lebensläufe, Sättigung
- **`re-cluster`:** dieselben Datenpunkte unter einer neuen Linse neu ordnen (z. B. Spannungen, Journey, Forces of Progress)
- **Qualitätssicherung:** Zitatabgleich per Skript und Prüfung jedes Datenpunkts, jeder Verdichtung und aller Zählungen gegen das Original – damit nichts halluziniert wird

**Befehle**

| Befehl | Beispiel |
|---|---|
| Map starten | „/affinity-mapping – Projekt XY, Forschungsfrage: …, hier das erste Transkript“ |
| Transkript hinzufügen | „Nächstes Transkript einarbeiten“ |
| re-cluster | „Bitte re-cluster, Linse: Spannungen & Widersprüche“ |
| QS | „Bitte QS für v3 laufen lassen“ |

→ [Ausführliche README](./affinity-mapping/README.md)

## research-summary

**Aufbau der Summary**
- Auf einen Blick
- Forschungsfrage und Basis
- 5–8 Top-Insights mit Belastbarkeit, Belegzitaten und Begründung der Auswahl
- Jobs-to-be-Done-Überblick
- Wie sich das Bild entwickelt hat
- Spannungen und Widersprüche
- Was gut funktioniert
- Handlungsfelder als „Wie könnten wir …?“-Fragen
- Offene Fragen und blinde Flecken

**Grundregeln**
- Nichts Neues behaupten: Jede Aussage hat eine Insight-ID und ist in die Map verlinkt.
- Zitate werden wortgleich aus der Map übernommen.
- Problemraum statt Lösung: Handlungsfelder sind Fragen, keine Maßnahmen.

**Varianten:** One-Pager, Workshop-Vorbereitung, angepasst an eine Zielgruppe.

→ [Ausführliche README](./research-summary/README.md)

---

## Erzeugte Dateien

| Datei | Skill | Inhalt |
|---|---|---|
| `affinity-map_<projekt>_v<n>.md` | affinity-mapping | eine Map-Version pro Schritt, Vorversionen bleiben unverändert |
| `map-entwicklung_<projekt>.md` | affinity-mapping | fortlaufendes Entwicklungsprotokoll |
| `transkript_<projekt>_T<nn>.txt` | affinity-mapping | gesichertes Transkript, falls es in den Chat eingefügt wurde |
| `research-summary_<projekt>_v<n>.md` | research-summary | Summary auf Basis der Map-Version n |

Alle Dateien im selben Obsidian-Vault ablegen: Dann führen Links von der Summary über den Insight bis zum einzelnen Zitat.

---

## Installation

Jeder Skill ist ein Ordner mit einer `SKILL.md` (die Anweisungen für Claude) und einer `README.md` (die Dokumentation für Menschen).

```
affinity-mapping/
├── SKILL.md
└── README.md
research-summary/
├── SKILL.md
└── README.md
```

- **Claude (Web/Desktop):** den jeweiligen Ordner als ZIP packen und in den Skill-Einstellungen hochladen.
- **Claude Code:** die Ordner in das Skills-Verzeichnis kopieren, z. B. `~/.claude/skills/`.

Danach lassen sich die Skills per `/affinity-mapping` und `/research-summary` aufrufen oder werden automatisch genutzt, wenn eine Anfrage passt.

---

## Feedback

Die Skills sind in Erprobung. Erfahrungen, Fehler und Ideen gern als Issue oder Pull Request – besonders interessant: Wo weicht die Map von eurer eigenen Auswertung ab, und was hat die QS übersehen?

**Autor:** Hias Wrba
