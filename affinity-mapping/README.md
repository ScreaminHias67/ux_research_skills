# Skill: affinity-mapping

Erstellt aus UX-Interviewtranskripten schrittweise eine **Affinity Map** als Obsidian-Markdown – von einzelnen Datenpunkten bis zu verdichteten Insights. Referenzrahmen ist das **Jobs-to-be-Done-Modell** nach Clayton Christensen (funktional, sozial, emotional). Nach jedem Schritt prüft eine Qualitätssicherung, dass alles auf die Transkripte zurückführbar ist. Ein eigenes **Entwicklungsprotokoll** hält fest, wie sich die Map von Interview zu Interview verändert.

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
| **Map starten** | „/affinity-mapping – Projekt TK_DS, Forschungsfrage: …, hier das erste Transkript“ | `affinity-map_<projekt>_v1.md` |
| **Transkript hinzufügen** | „Nächstes Transkript einarbeiten“ | neue Version `v<n+1>` mit Änderungsbericht und Markierungen |
| **re-cluster** | „Bitte re-cluster, Linse: Spannungen & Widersprüche“ | neue Version mit anderen Clustern und „Was ist neu?“ |
| **QS** | „Bitte QS für v3 laufen lassen“ | QS-Bericht; bei Befunden korrigierte neue Version |

Bei mehreren Transkripten auf einmal werden sie nacheinander eingearbeitet: eine Version, eine QS und ein Bericht pro Interview.

---

## Die Ebenen

| Ebene | Inhalt | Titel |
|---|---|---|
| **L0 Datenpunkt** | Eine atomare Aussage oder Beobachtung, Zitat oder gekennzeichnete Paraphrase, mit ID und Fundstelle | – |
| **L1 Voice of the Customer** | Cluster aus 2–7 Datenpunkten | Insight in Ich-Form („Ich möchte …, damit …“, „Immer wenn ich …, dann …“) |
| **L2 Insight-Cluster** *(optional)* | Cluster aus L1-Insights | übergeordneter Insight in Ich-Form |
| **L3 Thema** *(optional)* | Cluster aus L2 | thematische Headline |

Regeln:
- Jeder Datenpunkt gehört zu genau einem Cluster. Was nicht passt, kommt auf den **Parkplatz**.
- Insight-Titel beschreiben Bedürfnisse, keine Themen und keine Lösungen.
- Jeder Insight bekommt eine oder mehrere Job-Dimensionen, jede davon durch Datenpunkte belegt.
- Ein Coverage-Check zeigt, wie die Dimensionen verteilt sind. Lücken werden benannt, nicht aufgefüllt.

---

## Schrittweiser Aufbau

1. **v1** entsteht aus genau einem Transkript.
2. Jedes weitere Transkript erzeugt eine **neue Version**, die Vorversion bleibt unverändert.
3. Neue Datenpunkte gehen zuerst in passende Cluster. Bei Bedarf werden Cluster neu gebildet, geschärft, aufgespalten oder zusammengeführt.
4. **Markierungen** zeigen nur die Änderungen des aktuellen Schritts:

| Tag | Bedeutung |
|---|---|
| `#neu` | Insight durch dieses Transkript entstanden |
| `#bestaetigt` | jetzt von einer weiteren Person gestützt |
| `#geaendert` | Titel, Bedeutung, Job-Dimension oder Struktur angepasst |
| `#widerspruch` | neue Person widerspricht |
| `· neu` | Datenpunkt aus dem aktuellen Transkript |

5. Der **Änderungsbericht** jedes Schritts landet im **Entwicklungsprotokoll** `map-entwicklung_<projekt>.md` (Kurzfassung im Chat, Verweis in der Map).

---

## Entwicklungsprotokoll

Eine fortlaufende Datei pro Projekt, die die Dynamik der Map auf einer Metaebene beschreibt. Sie wird mit v1 angelegt und bei jedem Schritt fortgeschrieben:

- **Gesamtbild der Entwicklung** (bei jedem Schritt neu geschrieben):
  - Verlaufstabelle über alle Versionen
  - wie sich das Bild verändert hat
  - stabile, volatile und spät entstandene Insights
  - Sättigung und Verschiebung der Job-Dimensionen
- **Insight-Lebensläufe:** pro Insight, wann er entstanden, bestätigt, geändert oder widersprochen wurde und wo er heute steht
- **Schritt-Protokoll:** pro Transkript, re-cluster oder QS ein Eintrag mit neuen, bestätigten, veränderten, widersprochenen und aufgelösten Insights. Es wird nur angehängt, alte Einträge bleiben unverändert.

Das Protokoll ist Teil der QS und Input für den Skill `research-summary`.

---

## Qualitätssicherung

Läuft nach jedem Schritt und vor der Auslieferung, wenn möglich durch eine separate Prüf-Instanz.

- **A – Datenpunkte:**
  - Zitate per Skript mit dem Transkript abgleichen.
  - Sprecher:in und Fundstelle prüfen.
  - Paraphrasen ohne Zusätze, Kontext nicht verfälscht.
- **B – Verdichtungen:** Titel, Callouts und Job-Dimensionen durch Datenpunkte gedeckt; Deutungen als Deutung formuliert.
- **C – Struktur:** eindeutige IDs, jeder Datenpunkt genau einmal, stimmige Zählungen, vollständige Pseudonymisierung.

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

IDs: Datenpunkte `P01-007` (stabil über alle Versionen), Insights `I01`, Aggregate `L2-A`.

---

## Arbeiten in Obsidian

- **Einklappen:** Die Ebenen sind Überschriften (L2 `##`, L1 `###`), sie lassen sich einklappen.
- **Filtern:** Tags `#job/funktional`, `#job/sozial`, `#job/emotional`, `#neu`, `#qs/unsicher` sind über die Suche filterbar.
- **Verlinken:** Jeder Datenpunkt hat eine Block-ID, z. B. `[[affinity-map_TK_DS_v1#^p01-067]]`. So lassen sich Zitate aus anderen Notizen direkt verlinken.
- **Versionskette:** Über `previous:` im Frontmatter kommst du zur Vorversion.
- **Transkripte im Vault:** Liegen sie dort, setzt der Skill die Quellen als Wikilinks.

---

## Gut zu wissen

- **Frühe Versionen sind Hypothesen.** Nach ein oder zwei Interviews sind viele Insights `Einzelstimme`.
- **Fundstellen:** Zeitstempel oder Zeilennummern im Transkript machen die Rückführung präziser. Fehlen sie, wird der Gesprächsabschnitt (§) nach der Interviewfrage referenziert.
- **Diarisierungsfehler** im Transkript (falsch zugeordnete Sprecher:innen) werden ausgeschlossen und in den methodischen Notizen begründet.
- **Pseudonymisierung:** Personen erscheinen als P01, P02 …, Kolleg:innen als Rollen.
- **Die Map ist ein Arbeitsstand, keine Wahrheit.** Widersprüche und Unsicherheiten bleiben sichtbar.

---

## Zusammenspiel

`affinity-mapping` → finale Map (QS bestanden) + Entwicklungsprotokoll → `research-summary` → Übergabedokument
