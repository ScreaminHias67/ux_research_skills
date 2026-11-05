---
name: "affinity-mapping"
description: "Baut aus UX-Interviewtranskripten schrittweise eine Affinity Map (Datenpunkte → VoC-Insights → Aggregationen, JTBD) als Obsidian-Markdown; Transkripte hinzufügen und re-cluster."
---

# Affinity Mapping aus Interviewtranskripten

Dieser Skill verdichtet qualitative Interviewdaten bottom-up zu Insights und baut die Map **schrittweise** auf: Jede Map startet mit dem ersten Transkript, jedes weitere Transkript wird einzeln eingearbeitet. Nach jedem Schritt läuft eine **Qualitätssicherung (QS)**, die prüft, dass jede Dateneinheit auf das Transkript zurückführbar ist und nichts halluziniert wurde. Danach werden die maßgeblichen Änderungen ausgegeben und neue Insights markiert. Alle Änderungsberichte landen zusätzlich in einer eigenen Datei, dem **Entwicklungsprotokoll** (`map-entwicklung_<projekt>.md`), das die Dynamik der Map auf einer Metaebene beschreibt: Wie hat sich das Verständnis über die Interviews hinweg verändert, was ist stabil, was ist neu, was kippt? Referenzrahmen ist das Jobs-to-be-Done-Modell nach Clayton Christensen mit den drei Job-Dimensionen **funktional**, **sozial** und **emotional**. Ergebnis ist immer eine Markdown-Datei, die in Obsidian gut lesbar und navigierbar ist.

Vier Befehle:
- **Map starten:** erstes Transkript → neue Affinity Map (v1)
- **Transkript hinzufügen** („add“, „nächstes Transkript“, „einarbeiten“): neues Transkript in die bestehende Map einarbeiten → neue Version mit Änderungsbericht
- **re-cluster:** bestehende Map → neue Version mit anderen Clustern und neuen Sinnzusammenhängen
- **QS** („QS“, „prüfen“, „Halluzinationscheck“): bestehende Map erneut gegen die Transkripte prüfen, ohne neu zu clustern

Die QS ist bei den ersten drei Befehlen **Pflicht** und läuft vor der Auslieferung. Eine Map, die die QS nicht bestanden hat, wird nicht ausgeliefert.

---

## 1. Die Ebenen

| Ebene | Name | Inhalt | Titelregel |
|---|---|---|---|
| L0 | Information / Datenpunkt | Eine atomare Aussage oder Beobachtung aus dem Transkript | Kein Titel – Zitat oder enge Paraphrase + Quellenverweis |
| L1 | Voice of the Customer (VoC) | Cluster aus L0-Datenpunkten, der einen Insight beschreibt | Ich-Perspektive der Nutzenden, formuliert als Insight |
| L2 (optional) | Insight-Cluster | Cluster aus L1-Insights | Ich-Perspektive der Nutzenden, übergeordneter Insight |
| L3 (optional) | Thema | Cluster aus L2 | Thematische Headline (neutral, keine Ich-Form) |

### L0 – Datenpunkte
- **Atomar:** genau eine Aussage, ein Bedürfnis, ein Verhalten, ein Schmerzpunkt oder eine Beobachtung pro Datenpunkt. Lange Passagen aufteilen.
- **Rückführbar:** jeder Datenpunkt hat eine ID und einen Quellenverweis (Transkript, Person, Zeitstempel oder Zeilennummer; fehlen beide, den Gesprächsabschnitt § nach der Interviewfrage benennen).
- **Nah am Material:** wörtliches Zitat bevorzugen (in Anführungszeichen); Paraphrase nur, wenn das Zitat ohne Kontext unverständlich ist – dann als `(Paraphrase)` kennzeichnen.
- **Zitierkonventionen** (damit die QS sie prüfen kann): Auslassungen nur als `[…]`; Ersetzungen zur Pseudonymisierung nur in eckigen Klammern (`[UX-Kollegin]`); ergänzender Kontext nur außerhalb der Anführungszeichen in runden Klammern. Innerhalb der Anführungszeichen sonst kein Wort verändern – auch keine Grammatik- oder Tippfehler korrigieren.
- **Keine Interpretation** auf L0. Deutung beginnt erst auf L1.
- Beobachtungen der interviewenden Person (z. B. Zögern, Lachen) als eigener Datenpunkt mit Typ `Beobachtung`. Aussagen der Interviewenden selbst sind keine Datenpunkte.
- ID-Schema: `P01-007` (Teilnehmende:r 01, Datenpunkt 7). IDs sind über alle Versionen **stabil**. Teilnehmende werden pseudonymisiert (P01, P02 …) in der Reihenfolge, in der ihre Transkripte eingearbeitet werden. Klarnamen, Firmen- und Ortsangaben, die eine Person identifizierbar machen, entfernen oder generalisieren.

### L1 – Voice of the Customer
- 2–7 Datenpunkte pro Cluster. Cluster, die nur von einer Person gestützt sind, werden mit `Einzelstimme` markiert – nach dem ersten Transkript gilt das für viele; das ist normal.
- Jeder Datenpunkt gehört zu **genau einem** L1-Cluster. Was nicht passt, kommt auf den **Parkplatz** – nie erzwingen.
- Titel ist ein **Insight aus Nutzendenperspektive**, kein Thema. Muster:
  - „Ich möchte …, damit …“
  - „Immer wenn ich …, dann …“
  - „Ich fühle mich …, wenn …“
  - „Mir ist wichtig, dass andere …“
  - „Ich vermeide …, weil …“
- Schlechte Titel (vermeiden): „Navigation“, „Probleme mit dem Export“, „Nutzer wollen Dashboard“ (Thema, Dritte Person oder Lösung statt Bedürfnis).
- **Keine Lösungen** in Titeln („Ich möchte einen Button für …“ → umformulieren zum zugrunde liegenden Bedürfnis).
- Jeder L1-Insight bekommt eine stabile ID (`I01`, `I02` …), damit seine Entwicklung über Versionen nachverfolgbar ist. Bei Aufspaltung erhalten die neuen Teile neue IDs mit Verweis auf die Herkunft („aus I04“).
- Jeder L1-Insight wird **einer oder mehreren Job-Dimensionen** zugeordnet (siehe Abschnitt 2).

### L2 – Insight-Cluster (optional)
- Nur bilden, wenn sich zwischen L1-Insights ein echter übergeordneter Sinnzusammenhang zeigt (Faustregel: ab ca. 8 L1-Clustern).
- Titel weiterhin Ich-Perspektive, abstrakter als L1, beschreibt den größeren Job oder die zentrale Spannung.
- Die Job-Dimensionen eines L2-Clusters ergeben sich aus seinen L1-Insights (Vereinigungsmenge); nicht separat erfinden.

### L3 – Themen (optional)
- Nur bei großen Datensätzen. Thematische Headlines (z. B. „Kontrolle über die eigene Arbeit“), dienen der Orientierung.

---

## 2. Referenzrahmen: Jobs to be Done

Jeder L1-Insight wird einer oder mehreren Job-Dimensionen zugeordnet:

- **Funktional:** Was will die Person praktisch erledigen? (Aufgaben, Ergebnisse, Effizienz, Hürden)
- **Sozial:** Wie will die Person von anderen wahrgenommen werden, wie wirkt sie auf ihr Umfeld? (Status, Zugehörigkeit, Verantwortung gegenüber anderen, Rollenerwartungen)
- **Emotional:** Wie will sich die Person fühlen bzw. was will sie vermeiden zu fühlen? (Sicherheit, Kontrolle, Stolz, Angst, Frust)

### Mehrfachzuordnung
- Ein Insight bekommt **alle** Dimensionen, die durch seine Datenpunkte belegt sind.
- Es gibt **keine erzwungene Hauptdimension**. Ist eine Dimension klar dominant, darf sie zuerst genannt werden; sonst gleichrangig.
- Jede zugeordnete Dimension muss durch mindestens einen Datenpunkt im Cluster gestützt sein. Nicht „vorsichtshalber“ alle drei vergeben.
- Im Beschreibungstext (Callout) kurz benennen, **wie** die Dimensionen zusammenhängen.

### Coverage-Check
- Beim Clustern aktiv nach allen drei Dimensionen suchen – soziale und emotionale Jobs stecken oft in Nebensätzen, Begründungen und Tonfall.
- Am Ende zählen: Insights pro Dimension (mehrfach zugeordnete zählen in jeder ihrer Dimensionen) sowie die Kombinationen.
- Ist eine Dimension schwach oder leer, das im Abschnitt „Lücken“ benennen und Folgefragen vorschlagen. **Niemals** Insights erfinden oder Dimensionen zuschreiben, um eine Lücke zu füllen.

---

## 3. Schrittweiser Aufbau

### Grundregel
- Jede Map startet mit **genau einem** Transkript (v1).
- Jedes weitere Transkript wird **einzeln** eingearbeitet und erzeugt eine neue Version (v2, v3 …).
- Werden mehrere Transkripte auf einmal geliefert: in der angegebenen Reihenfolge (sonst nach Dateiname/Datum) nacheinander einarbeiten – eine Version, eine QS und ein Änderungsbericht pro Transkript. Vorher kurz die Reihenfolge nennen.
- Weitere Transkripte bauen immer auf der **neuesten Version** auf (auch wenn diese durch re-cluster entstanden ist), außer die Nutzer:in nennt eine andere.
- **Transkripte als Dateien sichern:** Wird ein Transkript in den Chat eingefügt statt angehängt, es unverändert als Datei speichern (`transkript_<projekt>_T01.txt`), damit die QS maschinell dagegen prüfen kann.

### Schritt 1: Map starten
1. Transkript lesen; Kontext und Forschungsfrage festhalten. Ist keine Forschungsfrage genannt, kurz nachfragen oder aus dem Material ableiten und als Annahme kennzeichnen.
2. Datenpunkte extrahieren (L0), Smalltalk und Moderation weglassen.
3. Bottom-up clustern (L1) – nach Bedeutung, nicht nach Leitfaden-Fragen. Titel formulieren, Job-Dimension(en) zuordnen.
4. L2/L3 nur, wenn wirklich sinnvoll.
5. Checkliste (Abschnitt 6) durchgehen und Entwurf `affinity-map_<projekt>_v1.md` schreiben.
6. **QS durchführen** (Abschnitt 5), Befunde korrigieren, QS-Bericht einfügen.
7. **Entwicklungsprotokoll anlegen** (`map-entwicklung_<projekt>.md`, siehe unten) mit dem Basiseintrag für v1.
8. Map und Protokoll ausliefern. In v1 keine Neu-Markierung, sondern nur die Basis.

### Folgeschritte: Transkript hinzufügen
1. **Datenpunkte extrahieren** für die neue Person (neue Personen-ID, IDs der bestehenden Datenpunkte bleiben).
2. **Zuerst in bestehende Cluster einordnen**, wo die Bedeutung wirklich passt.
3. **Neue Cluster bilden** für neue Sinnzusammenhänge – auch mit Datenpunkten vom Parkplatz der Vorversion.
4. **Bestehende Struktur anpassen, wo die neuen Daten es begründen:** Titel schärfen, Cluster aufspalten oder zusammenführen, Job-Dimensionen ergänzen, L2/L3 neu bilden.
5. **Widersprüche nicht glätten:** im Cluster markieren (`> [!warning] Widerspruch`) oder als eigenen Cluster bilden.
6. **Markieren** (siehe unten) und Entwurf `affinity-map_<projekt>_v<n+1>.md` speichern. **Vorversion nicht verändern.**
7. **Änderungsbericht ins Entwicklungsprotokoll schreiben** (neuer Schritt-Eintrag, Gesamtbild und Insight-Lebensläufe aktualisieren). In der Map selbst steht nur ein kurzer Verweis darauf.
8. **QS durchführen** (Abschnitt 5) – für die gesamte Map, nicht nur für die neuen Datenpunkte, weil sich Titel und Beschreibungen bestehender Cluster geändert haben können – und für den neuen Protokolleintrag.
9. **Im Chat** die maßgeblichen Änderungen und das QS-Ergebnis kurz ausgeben; Map und aktualisiertes Protokoll ausliefern.

### Markierungen in der neuen Version
Markiert wird nur, was sich **in diesem Schritt** geändert hat. Markierungen aus Vorversionen werden entfernt.

| Status | Markierung | Bedeutung |
|---|---|---|
| Neu | `#neu` am Titel + Callout `> [!tip] Neu in v<n>` | Insight entstand durch dieses Transkript |
| Bestätigt | `#bestaetigt` | Bestehender Insight wird jetzt von einer weiteren Person gestützt |
| Verändert | `#geaendert` + Callout mit altem Titel | Titel/Bedeutung angepasst, Job-Dimension ergänzt |
| Aufgespalten / zusammengeführt | `#geaendert` + Herkunftsvermerk („aus I04“, „vereint I02 + I07“) | Strukturänderung |
| Widersprochen | `#widerspruch` | Neue Person widerspricht dem Insight |
| Neue Datenpunkte | Zusatz `· neu` am Listeneintrag | Datenpunkt aus dem aktuellen Transkript |

### Entwicklungsprotokoll (eigene Datei)

Eine **einzige, fortlaufende Datei** pro Projekt: `map-entwicklung_<projekt>.md`. Sie wird mit v1 angelegt und bei jedem Schritt (Transkript hinzufügen, re-cluster, QS mit Korrekturen) fortgeschrieben. Sie beschreibt nicht die Inhalte der Map im Detail, sondern **wie sich die Map verändert** – die Metaebene des Erkenntnisprozesses. Sie ist Input für den Skill `research-summary`.

Aufbau (Vorlage in Abschnitt 7):

1. **Gesamtbild der Entwicklung** – wird bei jedem Schritt **neu geschrieben**:
   - **Verlaufstabelle** über alle Versionen: Transkript, neue Datenpunkte, neue / bestätigte / veränderte / widersprochene / aufgelöste Insights, Job-Verteilung.
   - **Wie sich das Bild verändert hat:** drei bis sechs Sätze zum Erkenntnisverlauf – welche Annahmen aus frühen Versionen sich verfestigt haben, welche gekippt oder relativiert wurden, welche Themen erst spät aufgetaucht sind.
   - **Stabile Insights:** über mehrere Versionen bestätigt, wenig verändert.
   - **Volatile Insights:** mehrfach umformuliert, aufgespalten, widersprochen.
   - **Späte Insights:** erst in den letzten Schritten entstanden – noch dünn belegt.
   - **Sättigung:** Entwicklung der Zahl neuer Insights pro Transkript. Sinkt sie über mehrere Transkripte deutlich, als mögliches Sättigungssignal benennen – vorsichtig formuliert, nicht als Beweis.
   - **Verschiebung der Job-Dimensionen** über die Zeit.
2. **Insight-Lebensläufe** – Tabelle, bei jedem Schritt aktualisiert: pro Insight-ID entstanden in, bestätigt in, geändert in, widersprochen in, aktueller Status (`stabil`, `neu`, `volatil`, `aufgelöst`, `aufgespalten in …`, `vereint in …`). Aufgelöste und umbenannte Insights bleiben mit ihrem Verbleib stehen.
3. **Schritt-Protokoll** – chronologisch, **nur anhängen, frühere Einträge nie ändern**. Pro Schritt ein Eintrag mit:
   - Version, Datum, Anlass (Transkript Txx / re-cluster mit Linse / QS) und Link auf die Map-Version
   - **Neue Insights** (mit Titel und Job-Dimensionen)
   - **Bestätigte Insights**
   - **Veränderte Insights** (alter → neuer Titel, Aufspaltungen, Zusammenführungen, ergänzte Job-Dimensionen)
   - **Widersprüche**
   - **Aufgelöste Insights** und Bewegungen vom/zum Parkplatz
   - **Verschiebung der Job-Verteilung**
   - **Einschätzung in einem Satz:** Was hat dieser Schritt Neues gebracht?
   - QS-Ergebnis in einer Zeile

Regeln:
- Jede Aussage im Protokoll muss durch einen Vergleich der beteiligten Map-Versionen belegbar sein. Keine Deutung des Erkenntnisverlaufs, die die Maps nicht tragen.
- Im Gesamtbild Deutungen als Deutung formulieren („deutet darauf hin“, „wirkt“).
- In der Map steht statt eines ausführlichen Änderungsberichts ein Verweis-Callout auf den passenden Protokolleintrag (siehe Template).
- Im Chat nur die maßgeblichen Änderungen nennen; Detailbewegungen einzelner Datenpunkte gehören nicht ins Protokoll, sondern sind an den `· neu`-Markierungen in der Map sichtbar.

---

## 4. Befehl „re-cluster“

Auslöser: „re-cluster“, „neu clustern“, „anders clustern“ o. Ä.

Ziel: eine **neue Version** mit **anderen Clustern und neuen Sinnzusammenhängen** – kein Umbenennen der alten Cluster. Re-cluster nimmt keine neuen Transkripte auf.

Regeln:
1. **L0 bleibt unverändert:** dieselben Datenpunkte, dieselben IDs und Block-IDs.
2. **Neue Linse wählen** (oder die genannte verwenden) und im Frontmatter (`lens:`, `step: recluster`) benennen. Mögliche Linsen:
   - **Job-Dimension zuerst:** oberste Ordnung funktional / sozial / emotional, plus Sektion „Dimensionsübergreifend“; mehrfach zugeordnete Insights stehen vollständig an genau einer Stelle, sonst nur per Link `[[#„Insight-Titel“]]`.
   - **Spannungen & Widersprüche:** Cluster um Zielkonflikte
   - **Situation / Auslöser:** „Immer wenn …“-Momente
   - **Journey / Phasen:** vorher – währenddessen – danach
   - **Hürden vs. Antreiber:** Push/Pull, Ängste und Gewohnheiten (Forces of Progress)
   - **Segmente / Rollen:** wo sich Gruppen unterscheiden
   Ohne Vorgabe eine Linse wählen, die sich deutlich von der vorherigen unterscheidet, und kurz begründen.
3. **Wirklich neu clustern:** mindestens die Hälfte der L1-Cluster mit neuer Zusammensetzung. Identisch wiederkehrende Cluster als „robuster Insight“ markieren (`#robust`).
4. **Neue Insight-Titel** nach denselben Regeln; neue Insight-IDs, Job-Dimensionen neu bestimmen.
5. **Vorversion nicht verändern.** Neue Datei `affinity-map_<projekt>_v<n+1>.md` mit `previous:`-Verweis.
6. **Eintrag im Entwicklungsprotokoll** mit Anlass „re-cluster: <Linse>“: neue Sinnzusammenhänge, robuste Insights (`#robust`), aufgelöste Cluster, verschobene Job-Verteilung, Zuordnung alter zu neuen Insight-IDs in den Insight-Lebensläufen. In der Verlaufstabelle als Zeile „– (re-cluster: <Linse>)“.
7. **QS durchführen** (Abschnitt 5). Der Schwerpunkt liegt hier auf Ebene B (neue Titel und Beschreibungen); zusätzlich prüfen, dass kein Datenpunkt beim Umsortieren verändert wurde, verloren ging oder doppelt erscheint.

---

## 5. Qualitätssicherung (QS)

Ziel: Jede Dateneinheit ist auf das Transkript zurückführbar, und die Map enthält keine Halluzinationen – weder erfundene Zitate noch Details, Zahlen, Wertungen oder Schlussfolgerungen, die das Material nicht trägt.

### Wer prüft
- Wenn ein Agent- bzw. Subagent-Tool verfügbar ist, führt eine **separate Prüf-Instanz** die QS durch, die nur die Transkriptdatei(en) und die Map erhält – nicht den Arbeitskontext der Erstellung. So bewertet die Map nicht sich selbst.
- Sonst prüft Claude selbst, aber in einem eigenen Durchgang nach Fertigstellung der Map, jede Stelle gezielt gegen das Transkript nachlesend – nie aus dem Gedächtnis.

### Ebene A – Datenpunkte (L0), jeder einzeln

**A1 Maschineller Zitatabgleich** (wenn das Transkript als Datei vorliegt): Alle wörtlichen Zitate per Skript gegen das Transkript prüfen. Vorlage:

```python
import re, sys, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[„“”\"»«’‘']", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

transcript = norm(open(sys.argv[1], encoding="utf-8").read())
map_md = open(sys.argv[2], encoding="utf-8").read()

problems = []
for line in map_md.splitlines():
    m_id = re.search(r"\^(p\d+-\d+)\s*$", line)
    if not m_id:
        continue
    dp_id = m_id.group(1)
    for quote in re.findall(r"„(.+?)“", line):
        # Auslassungen […] und Ersetzungen [...] trennen das Zitat in Segmente
        for seg in re.split(r"\[[^\]]*\]", quote):
            seg = norm(seg).strip(" .,;:…")
            if len(seg) >= 4 and seg not in transcript:
                problems.append((dp_id, seg))

for dp_id, seg in problems:
    print(f"NICHT GEFUNDEN  {dp_id}: {seg}")
print(f"{len(problems)} Problem(e)")
```

Aufruf: `python qs_zitate.py transkript_<projekt>_T01.txt affinity-map_<projekt>_v<n>.md` (bei mehreren Transkripten diese vorher zusammenführen oder je Person gegen das passende Transkript prüfen). Jeder Treffer wird manuell geklärt.

**A2 Prüfung pro Datenpunkt** (bei Zitaten und Paraphrasen):
- **Existenz:** Die Aussage steht so im Transkript. Bei Zitaten wortgleich (außer den erlaubten `[…]`- und `[Ersetzung]`-Konventionen).
- **Sprecher:in:** Die Aussage stammt von der angegebenen Person – nicht von Interviewenden oder einer anderen teilnehmenden Person. Bei offensichtlich falscher Sprecherzuordnung im Transkript selbst (Diarisierungsfehler) den Datenpunkt ausschließen und in den methodischen Notizen begründen.
- **Fundstelle:** Der Quellenverweis (Zeitstempel, Zeile oder Abschnitt §) führt zur richtigen Stelle.
- **Paraphrasentreue:** Die Paraphrase fügt nichts hinzu. Jede Zahl, jeder Name, jede Zeitangabe, jede Wertung und jede Kausalbeziehung („weil“, „deshalb“) muss im Transkript stehen. Abschwächungen und Unsicherheiten der Person („gefühlt“, „wahrscheinlich“, „ich glaube“) bleiben erhalten.
- **Klammerzusätze:** Kontext in runden Klammern ist ebenfalls aus dem Transkript belegt und ändert die Bedeutung nicht.
- **Sinntreue im Kontext:** Das Zitat wird nicht gegen seinen Zusammenhang verwendet (z. B. Ironie, Verneinung im Nachsatz, hypothetische Aussage).

### Ebene B – Verdichtungen (L1–L3, Callouts, Überblick)
- **Titel:** Jeder Insight-Titel ist durch die Datenpunkte seines Clusters gedeckt – keine Aussage, die erst ein anderer Cluster oder Vorwissen liefert.
- **Callout-Texte:** Jede Sachbehauptung (z. B. „zweite Plattform ist Android“, „seit zwei Jahren“) ist durch einen Datenpunkt belegt. Deutungen sind als Deutung formuliert („wirkt“, „deutet darauf hin“), nicht als Tatsache.
- **Job-Dimensionen:** Jede vergebene Dimension ist durch mindestens einen konkreten Datenpunkt gestützt.
- **Kontext, Lücken, Notizen:** Angaben über Personen und Organisation (Rollen, Teamgrößen, Daten) stehen im Transkript oder wurden von der Nutzer:in genannt.

### Ebene C – Struktur und Konsistenz
- Jede Datenpunkt-ID ist eindeutig, jede Block-ID passt zur ID, keine Lücken oder Dubletten in der Nummerierung pro Person.
- Jeder Datenpunkt steht genau einmal (in einem Cluster oder auf dem Parkplatz).
- Zahlen in Frontmatter, Überblickstabelle, Job-Verteilung und Entwicklungstabelle stimmen mit dem Inhalt überein (nachzählen, am besten per Skript).
- Personenangaben pro Insight und `Einzelstimme`-Markierungen stimmen mit den tatsächlichen Datenpunkten überein.
- Pseudonymisierung vollständig: keine Klarnamen von Personen im gesamten Dokument.
- (Folgeschritte/re-cluster) Kein bestehender Datenpunkt wurde verändert oder ist verloren gegangen.
- **Entwicklungsprotokoll:** Zahlen in Verlaufstabelle und Insight-Lebensläufen stimmen mit den Map-Versionen überein; jede Aussage im neuen Eintrag (neu, bestätigt, verändert, aufgelöst) ist durch den Vergleich mit der Vorversion belegt; frühere Einträge sind unverändert.

### Umgang mit Befunden
- **Korrigieren, nicht kaschieren:** Fehlerhafte Zitate auf den Originalwortlaut zurücksetzen; nicht belegbare Details aus Paraphrasen und Callouts streichen; falsche Fundstellen korrigieren; Zahlen neu zählen.
- **Nicht belegbare Datenpunkte entfernen.** Fehlt dadurch einem Cluster die Grundlage, Cluster auflösen oder Titel abschwächen; verbleibende Datenpunkte ggf. auf den Parkplatz.
- **Nie eine Lücke durch neue Formulierungen „reparieren“**, die wiederum nicht belegt sind.
- Nach Korrekturen die betroffenen Stellen und alle Zählungen erneut prüfen.
- Grenzfälle, die sich nicht eindeutig klären lassen (z. B. unverständliche Transkriptstellen), mit `#qs/unsicher` markieren und im QS-Bericht nennen.

### QS-Bericht
Am Ende der Map ein Abschnitt **„QS-Bericht v<n>“** (Vorlage in Abschnitt 7) und im Chat eine Kurzfassung:
- geprüfte Datenpunkte (Zitate / Paraphrasen), Prüfmethode (Skript + manuell, separate Prüf-Instanz ja/nein)
- Befunde nach Art (z. B. Wortlaut abweichend, Sprecher:in falsch, Paraphrase mit Zusatz, Callout-Behauptung unbelegt, Zählfehler) und wie sie behoben wurden
- verbleibende `#qs/unsicher`-Stellen
- Ergebnis: **bestanden** (keine offenen Befunde außer markierten Unsicherheiten) oder **nicht bestanden** (dann nicht ausliefern, sondern erst korrigieren)

### Befehl „QS“ einzeln
Auf Wunsch kann die QS für eine bestehende Map separat laufen. Dann alle drei Ebenen prüfen, Befunde korrigieren und das Ergebnis als neue Version (`step: qs`) speichern – die geprüfte Version bleibt unverändert – und einen Eintrag „QS“ im Entwicklungsprotokoll anhängen, wenn sich Insights dadurch verändert haben. Liegen keine Befunde vor, nur den Bericht im Chat ausgeben, ohne neue Version.

---

## 6. Checkliste vor der QS
- Jeder Datenpunkt genau einmal verortet (Cluster oder Parkplatz)?
- Jeder L1-Titel in Ich-Form, Insight statt Thema, ohne Lösung?
- Belegt jeder Insight sich durch seine Datenpunkte (kein Überdehnen)?
- Ist jede zugeordnete Job-Dimension durch Datenpunkte gestützt?
- Coverage-Check gemacht?
- Zitierkonventionen eingehalten (`[…]`, `[Ersetzung]`, Kontext in runden Klammern außerhalb der Anführungszeichen)?
- (Folgeschritte) Nur aktuelle Änderungen markiert, alte Markierungen entfernt, IDs stabil, Vorversion unverändert?
- Entwicklungsprotokoll fortgeschrieben (Gesamtbild neu, Lebensläufe aktualisiert, neuer Schritt-Eintrag angehängt, alte Einträge unverändert) und Verweis in der Map gesetzt?

Sprache: Sprache der Transkripte bzw. der Anfrage. Im Deutschen geschlechterinklusiv mit Doppelpunkt formulieren (Nutzer:innen, Teilnehmer:innen).

---

## 7. Output-Template (Obsidian)

Grundsätze: YAML-Frontmatter für Metadaten, Überschriften-Hierarchie für die Ebenen (in Obsidian einklappbar), Tags für Job-Dimensionen und Änderungsstatus (filterbar), Block-IDs (`^p01-007`) an Datenpunkten, damit sie per `[[datei#^p01-007]]` verlinkbar sind. Liegen die Transkripte als Dateien im Vault, Quellen als Wikilink `[[Transkript P01]]` setzen. Die Block-ID steht immer am Zeilenende (das QS-Skript erkennt Datenpunkte daran).

Ohne L2/L3: L1 als `##`, Datenpunkte als Liste. Mit L2: L2 als `##`, L1 als `###`. Mit L3: L3 `##`, L2 `###`, L1 `####`.

```markdown
---
title: Affinity Map – <Projekt>
version: 3
step: add            # start | add | recluster | qs
lens: bottom-up
previous: "[[affinity-map_<projekt>_v2]]"
date: YYYY-MM-DD
transcripts: [T01, T02, T03]
participants: [P01, P02, P03]
added_in_this_step: T03 (P03)
research_question: "<Forschungsfrage>"
datapoints: 61
voc_clusters: 12
qs: bestanden
tags: [ux-research, affinity-map, jtbd]
---

# Affinity Map – <Projekt>

> [!info] Kontext
> Forschungsfrage, eingearbeitete Interviews, Besonderheiten.

## Überblick

| ID | Insight | Jobs | Datenpunkte | Personen | Status |
|---|---|---|---|---|---|
| I01 | Ich möchte … | funktional, emotional | 5 | P01, P03 | bestätigt |
| I09 | Immer wenn ich … | sozial | 3 | P03 | neu |

**Job-Verteilung** (Mehrfachzuordnung möglich): funktional 7 · sozial 4 · emotional 6
**Häufige Kombinationen:** funktional+emotional 3 · funktional+sozial 2

> [!note] Änderungen in v3 (Transkript T03)
> 2 neue, 4 bestätigte, 1 veränderter Insight. Details und Gesamtentwicklung: [[map-entwicklung_<projekt>#v3 – Transkript T03]]

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

---

## Parkplatz
- „…“ — P02 · T01, 00:44:10 ^p02-030

## Lücken & offene Fragen
- …

## Methodische Notizen
- Annahmen, Ausschlüsse, Unsicherheiten beim Clustern

## QS-Bericht v3
- **Geprüft:** 61 Datenpunkte (38 Zitate, 23 Paraphrasen), 12 Insights, alle Zählungen
- **Methode:** Zitatabgleich per Skript + manuelle Prüfung; separate Prüf-Instanz: ja
- **Befunde & Korrekturen:**
  - Wortlaut abweichend: 2 → auf Original zurückgesetzt (p03-004, p03-011)
  - Paraphrase mit unbelegtem Zusatz: 1 → Zusatz gestrichen (p02-017)
  - Callout-Behauptung unbelegt: 1 → gestrichen (I05)
  - Zählfehler: 1 → korrigiert (Job-Verteilung)
- **Unsicher:** p03-019 (Transkriptstelle schwer verständlich) #qs/unsicher
- **Ergebnis:** bestanden
```

### Template Entwicklungsprotokoll

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
> Beschreibt, wie sich die Affinity Map über die Interviews hinweg verändert hat. Inhalte stehen in der Map, hier steht der Erkenntnisverlauf.

## Gesamtbild der Entwicklung
*Stand v3 – wird bei jedem Schritt neu geschrieben.*

### Verlauf
| Version | Anlass | Neue DP | Neu | Bestätigt | Verändert | Widersprochen | Aufgelöst | Jobs (f · s · e) |
|---|---|---|---|---|---|---|---|---|
| [[affinity-map_<projekt>_v1\|v1]] | T01 | 23 | 6 | – | – | – | – | 5 · 2 · 3 |
| [[affinity-map_<projekt>_v2\|v2]] | T02 | 19 | 3 | 4 | 1 | 0 | 0 | 7 · 3 · 5 |
| [[affinity-map_<projekt>_v3\|v3]] | T03 | 17 | 2 | 4 | 1 | 1 | 0 | 8 · 4 · 6 |

### Wie sich das Bild verändert hat
Drei bis sechs Sätze zum Erkenntnisverlauf.

### Stabil
- I01 – seit v1, in v2 und v3 bestätigt

### Volatil
- I05 – in v2 umformuliert, in v3 um emotionale Dimension ergänzt

### Spät entstanden
- I09 – erst in v3, Einzelstimme

### Sättigung
Neue Insights pro Transkript: 6 → 3 → 2. Vorsichtige Einschätzung …

### Verschiebung der Job-Dimensionen
…

## Insight-Lebensläufe
| ID | Insight (aktueller Titel) | Entstanden | Bestätigt | Geändert | Widersprochen | Status |
|---|---|---|---|---|---|---|
| I01 | Ich möchte … | v1 | v2, v3 | – | – | stabil |
| I06 | Ich … | v1 | – | v3 | – | aufgespalten in I10, I11 |
| I09 | Immer wenn ich … | v3 | – | – | – | neu |

## Schritt-Protokoll
*Chronologisch, nur angehängt.*

### v1 – Transkript T01
- **Datum:** YYYY-MM-DD · **Map:** [[affinity-map_<projekt>_v1]]
- **Basis:** 6 Insights, 23 Datenpunkte, Job-Verteilung 5 · 2 · 3
- **Einschätzung:** …
- **QS:** bestanden

### v3 – Transkript T03
- **Datum:** YYYY-MM-DD · **Map:** [[affinity-map_<projekt>_v3]] · **Vorversion:** [[affinity-map_<projekt>_v2]]
- **Neu:** I09 „…“ (sozial)
- **Bestätigt:** I01, I04
- **Verändert:** I05 „alt“ → „neu“; I06 aufgespalten in I10 + I11
- **Widerspruch:** P03 widerspricht I03
- **Aufgelöst / Parkplatz:** p01-018 vom Parkplatz in I09
- **Job-Verteilung:** soziale Dimension erstmals deutlich belegt
- **Einschätzung:** …
- **QS:** bestanden
```

---

## 8. Qualitätsprinzipien

- Belegen statt behaupten: Jeder Insight und jede Job-Zuordnung muss aus den Datenpunkten nachvollziehbar sein.
- Lieber weniger und belegt als mehr und ausgeschmückt: Im Zweifel streichen, nicht ergänzen.
- Häufigkeit ist nicht Relevanz: Ein stark emotional geladener Einzelbefund kann wichtiger sein als ein häufiger Nebensatz.
- Frühe Versionen sind vorläufig: Nach wenigen Transkripten Insights als Hypothesen behandeln.
- Widersprüche sichtbar lassen, nicht glätten.
- Die Map ist ein Arbeitsstand für das Team, keine Wahrheit – Unsicherheiten offen markieren.