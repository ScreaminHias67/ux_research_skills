# Skill: affinity-mapping

Erstellt aus UX-Interviewtranskripten schrittweise eine **Affinity Map** als Obsidian-Markdown – von einzelnen Datenpunkten bis zu verdichteten Insights. Die Map entsteht **emergent und bottom-up**: Mit jedem Interview darf sie sich neu ordnen. Referenzrahmen ist das **Jobs-to-be-Done-Modell** nach Clayton Christensen (funktional, sozial, emotional). Nach jedem Schritt prüft eine Qualitätssicherung, dass alles auf die Transkripte zurückführbar ist. Ein eigenes **Entwicklungsprotokoll** hält fest, wie sich das Verständnis von Interview zu Interview verschiebt.

---

## Grundhaltung: Menschen forschen, der Skill unterstützt

> [!important] Interviews führen immer Menschen
> Die Interviews müssen immer von Menschen geführt werden, die gute Fragen stellen und gut zuhören. Nachfragen, Pausen aushalten, Zwischentöne wahrnehmen und Vertrauen aufbauen kann kein Skill übernehmen – und ohne diese Qualität im Gespräch ist auch das beste Transkript wenig wert.

Sinn und Zweck des Skills ist **nicht**, die Auswertung durch Menschen zu ersetzen. Er soll:
- die Auswertung **erleichtern**, wenn für ein gemeinsames Affinity Mapping im Team zu wenig Zeit ist
- die **Qualität gegenüber einfachen Transkript-Summaries erhöhen**, weil das Material mehrstufig und nachvollziehbar verdichtet wird (Datenpunkt → Insight → Aggregation, mit Prüfung gegen das Original)

Die Map ist ein Arbeitsstand, den das Research-Team liest, hinterfragt, umsortiert und mit dem eigenen Erleben aus den Gesprächen abgleicht. Die Deutungshoheit bleibt bei den Menschen, die die Interviews geführt haben.

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

- Qualitative Interviews strukturiert und nachvollziehbar auswerten
- Insights aus Sicht der Nutzenden formulieren statt Themen zu sammeln
- Sehen, was jedes einzelne Interview zur Erkenntnis beiträgt (inkl. Sättigungssignal)
- Material aus neuen Blickwinkeln betrachten (re-cluster)
- Eine belastbare Grundlage für die Übergabe mit dem Skill `research-summary` schaffen

---

## Befehle

| Befehl | Beispiel-Prompt | Ergebnis |
|---|---|---|
| **Map starten** | „/affinity-mapping – Projekt TK_DS, Forschungsfrage: …, hier die ersten beiden Transkripte“ | `affinity-map_<projekt>_v1.md` aus 1–2 Transkripten |
| **Transkript hinzufügen** | „Nächstes Transkript einarbeiten“ | neue Version `v<n+1>` mit Änderungsbericht und Markierungen |
| **re-cluster** | „Bitte re-cluster, Linse: Spannungen & Widersprüche“ oder „… Linse: neu von unten“ | neue Version mit anderen Clustern |
| **QS** | „Bitte QS für v3 laufen lassen“ | QS-Bericht; bei Befunden korrigierte neue Version |

Werden beim Start mehr als zwei Transkripte geliefert, entsteht v1 aus den ersten beiden; die übrigen werden nacheinander eingearbeitet – eine Version, eine QS und ein Bericht pro Interview.

Die Map auf ein Miro-Board bringen und Änderungen des Teams zurücklesen: Skill [`affinity-miro`](../affinity-miro).

---

## Die Ebenen

| Ebene | Inhalt | Titel |
|---|---|---|
| **L0 Datenpunkt** | Eine atomare Aussage oder Beobachtung, Zitat oder gekennzeichnete Paraphrase, mit ID und Fundstelle | – |
| **L1 Voice of the Customer** | Cluster aus Datenpunkten (Richtwert 2–7, keine feste Grenze) | Insight in Ich-Form („Ich möchte …, damit …“, „Immer wenn ich …, dann …“) |
| **L2 Insight-Cluster** *(optional)* | Cluster aus L1-Insights | übergeordneter Insight in Ich-Form |
| **L3 Thema** *(optional)* | Cluster aus L2 | thematische Headline |

Regeln:
- Faustregel für die Menge: **1 Interviewminute ≈ 1 Datenpunkt.** Der Skill nennt vorab einen Zielwert und begründet im QS-Bericht, wenn er deutlich abweicht – er füllt aber nie künstlich auf.
- Größere Cluster sind in Ordnung, wenn sie sich nicht sinnvoll teilen lassen; ab etwa 10 Datenpunkten prüft der Skill, ob sich Unter-Insights zeigen. Ein einzelner, starker Datenpunkt darf ein eigener Cluster sein.
- Jeder Datenpunkt gehört zu genau einem Cluster. Was nicht passt, kommt auf den **Parkplatz**.
- Insight-Titel beschreiben Bedürfnisse, keine Themen und keine Lösungen.
- Jeder Insight bekommt eine oder mehrere Job-Dimensionen, jede davon durch Datenpunkte belegt.
- Ein Coverage-Check zeigt, wie die Dimensionen verteilt sind. Lücken werden benannt, nicht aufgefüllt.

---

## Schrittweiser Aufbau

0. **Sprecherprüfung:** Vor jeder Verarbeitung zeigt der Skill, wer im Transkript spricht (Label, Rollenvorschlag, Redeanteil, Zahl der Fragen, Beispielsatz), und wartet auf deine Bestätigung. So werden Interviewende nicht versehentlich als Interviewte ausgewertet.
1. **v1** entsteht aus einem oder zwei Transkripten, die gemeinsam geclustert werden.
2. Jedes weitere Transkript erzeugt eine **neue Version**, die Vorversion bleibt unverändert.
3. **Offene Neuordnung:** Die Vorversion ist Ausgangslage, nicht Maßstab. Neue und bestehende Datenpunkte werden gleichberechtigt betrachtet; Cluster dürfen aufgelöst, neu geschnitten und umformuliert werden – so, wie ein Team an der Wand ganze Bereiche umbaut, wenn neue Zettel dazukommen. Jede Änderung muss sich aus den Daten begründen.
4. Ein Insight behält seine ID, solange sein Kern gleich bleibt. Wird er neu geschnitten, bekommt er eine neue ID mit Herkunft über die Datenpunkte („vereint I04 + I07“).
5. **Markierungen** zeigen nur die Änderungen des aktuellen Schritts:

| Tag | Bedeutung |
|---|---|
| `#neu` | Insight durch dieses Transkript entstanden |
| `#bestaetigt` | jetzt von einer weiteren Person gestützt |
| `#geaendert` | neu geschnitten: Titel, Zuschnitt, Job-Dimension oder Struktur angepasst |
| `#widerspruch` | neue Person widerspricht |
| `#team` | vom Team auf dem Miro-Board geändert |
| `· neu` | Datenpunkt aus dem aktuellen Transkript |

6. Der **Änderungsbericht** jedes Schritts landet im **Entwicklungsprotokoll** `map-entwicklung_<projekt>.md` (Kurzfassung im Chat, Verweis in der Map).

---

## Entwicklungsprotokoll

Eine fortlaufende Datei pro Projekt, die die Dynamik der Map auf einer Metaebene beschreibt. Sie wird mit v1 angelegt und bei jedem Schritt fortgeschrieben:

- **Gesamtbild der Entwicklung** (bei jedem Schritt neu geschrieben):
  - Verlaufstabelle über alle Versionen
  - wie sich das Bild verschoben hat
  - unverändert seit, neu geschnitten, spät entstanden – neutral beschrieben: Veränderung ist erwünscht und kein Qualitätsmangel
  - Sättigung und Verschiebung der Job-Dimensionen
- **Schritt-Protokoll:** pro Transkript, re-cluster, QS oder Miro-Rücksync ein Eintrag mit neuen, bestätigten, neu geschnittenen (mit Herkunft), widersprochenen und aufgelösten Insights. Es wird nur angehängt, alte Einträge bleiben unverändert.

Das Protokoll ist Teil der QS und Input für den Skill `research-summary`.

---

## Qualitätssicherung

Läuft nach jedem Schritt und vor der Auslieferung, wenn möglich durch eine separate Prüf-Instanz. Mechanisches erledigt das Skript, die Prüf-Instanz bekommt nur Transkript-Ausschnitte rund um die neuen Datenpunkte – das spart viele Tokens.

- **A – Datenpunkte:**
  - Zitate per Skript mit dem Transkript abgleichen – nur neue und veränderte; dass alte unverändert sind, prüft das Skript.
  - Sprecher:in (auch per Skript anhand der bestätigten Sprecherzuordnung) und Fundstelle prüfen.
  - Paraphrasen ohne Zusätze, Kontext nicht verfälscht.
- **B – Verdichtungen:** Titel, Callouts und Job-Dimensionen durch Datenpunkte gedeckt; Deutungen als Deutung formuliert.
- **C – Struktur:** eindeutige IDs, jeder Datenpunkt genau einmal, stimmige Zählungen (alles per Skript), vollständige Pseudonymisierung.

Befunde werden korrigiert, nicht kaschiert – im Zweifel wird gestrichen. Ergebnis ist ein **QS-Bericht** am Ende der Map; nicht bestandene Maps werden nicht ausgeliefert.

**Zitierkonventionen** (damit die Prüfung funktioniert):
- Auslassungen nur als `[…]`
- Pseudonymisierte Ersetzungen nur in eckigen Klammern: `[UX-Kollegin]`
- Kontext nur in runden Klammern außerhalb der Anführungszeichen
- Innerhalb von Zitaten nichts korrigieren

---

## Dateien & Benennung

| Datei | Inhalt |
|---|---|
| `transkript_<projekt>_T01.txt` | gesichertes Original-Transkript (wird angelegt, wenn eingefügt statt angehängt) |
| `affinity-map_<projekt>_v1.md` | Basisversion |
| `affinity-map_<projekt>_v<n>.md` | jede weitere Version (add, re-cluster, qs) mit `previous:`-Verweis |
| `map-entwicklung_<projekt>.md` | Entwicklungsprotokoll über alle Versionen (eine Datei, fortgeschrieben) |
| `sprecher_<projekt>.json` | bestätigte Sprecherzuordnung – enthält ggf. Klarnamen, gehört zu den Transkripten in einen geschützten Ordner |
| `qs-kontext_v<n>.md` | Transkript-Ausschnitte für die Prüf-Instanz (Arbeitsdatei) |

IDs: Datenpunkte `P01-007` (stabil über alle Versionen), Team-Notizen `team-001`, Insights `I01` (bleiben bei gleichem Kern, werden nie wiederverwendet).

---

## Aufbau des Skills

```
affinity-mapping/
├── SKILL.md              Kernanweisungen (immer geladen)
├── references/
│   ├── templates.md      Vorlagen für Map und Protokoll (nur vor v1)
│   └── qs.md             QS im Detail, Anweisung für die Prüf-Instanz
└── scripts/
    └── amap.py           Sprecherprüfung, neue Version, QS-Skript, Tabellen
```

`amap.py` braucht nur Python 3, keine Installation. Die wichtigsten Befehle:

| Befehl | Wofür |
|---|---|
| `speakers` | Sprechertabelle, Dauer, Zielwert Datenpunkte; Zuordnung speichern |
| `new-version` | Vorversion kopieren und Markierungen des letzten Schritts entfernen – danach wird nur noch gezielt editiert |
| `check` | Zitate, Sprecher:innen, Struktur und Zählungen prüfen |
| `context` | Transkript-Ausschnitte für die Prüf-Instanz |
| `stats` / `trend` | Überblickstabelle und Verlaufstabelle erzeugen |

Ohne Codeausführung arbeitet der Skill nach denselben Regeln manuell und vermerkt das im QS-Bericht.

---

## Arbeiten in Obsidian

- **Einklappen:** Die Ebenen sind Überschriften (L2 `##`, L1 `###`), sie lassen sich einklappen.
- **Filtern:** Tags `#job/funktional`, `#job/sozial`, `#job/emotional`, `#neu`, `#qs/unsicher` sind über die Suche filterbar.
- **Verlinken:** Jeder Datenpunkt hat eine Block-ID, z. B. `[[affinity-map_TK_DS_v1#^p01-067]]`. So lassen sich Zitate aus anderen Notizen direkt verlinken.
- **Versionskette:** Über `previous:` im Frontmatter kommst du zur Vorversion.
- **Transkripte im Vault:** Liegen sie dort, setzt der Skill die Quellen als Wikilinks.

---

## Gut zu wissen

- **Frühe Versionen sind Hypothesen.** Nach ein oder zwei Interviews sind viele Insights `Einzelstimme` – und sie dürfen sich später grundlegend ändern.
- **Fundstellen:** Zeitstempel oder Zeilennummern im Transkript machen die Rückführung präziser. Fehlen sie, wird der Gesprächsabschnitt (§) nach der Interviewfrage referenziert.
- **Diarisierungsfehler** im Transkript (falsch zugeordnete Sprecher:innen) werden ausgeschlossen und in den methodischen Notizen begründet.
- **Pseudonymisierung:** Personen erscheinen als P01, P02 …, Kolleg:innen als Rollen.
- **Die Map ist ein Arbeitsstand, keine Wahrheit.** Widersprüche und Unsicherheiten bleiben sichtbar.

---

## Zusammenspiel

`affinity-mapping` ⇄ `affinity-miro` (gemeinsame Arbeit am Board) → finale Map (QS bestanden) + Entwicklungsprotokoll → `research-summary` → Übergabedokument
