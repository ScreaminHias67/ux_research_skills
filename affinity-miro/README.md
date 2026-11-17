# Skill: affinity-miro

Bringt eine Affinity Map aus dem Skill [`affinity-mapping`](../affinity-mapping) auf ein **Miro-Board**, damit das Team gemeinsam daran weiterarbeiten kann – und liest die Änderungen anschließend wieder in eine neue Map-Version zurück. Die Markdown-Map bleibt die Grundlage für QS, Entwicklungsprotokoll und [`research-summary`](../research-summary); das Board ist der gemeinsame Arbeitsraum.

---

## Wofür

- Eine vom Skill erstellte Map im Team **gemeinsam hinterfragen und umsortieren**, wie an einer echten Wand
- Die Deutung des Teams **nachvollziehbar** in die Map zurückholen, ohne die Rückführbarkeit auf die Transkripte zu verlieren
- Nach jedem neuen Interview einen **frischen Board-Stand** neben dem alten erzeugen

---

## Befehle

| Befehl | Beispiel-Prompt | Ergebnis |
|---|---|---|
| **Auf Miro bringen** | „/affinity-miro – bring v3 auf dieses Board: <URL>“ | Board-Stand v3 mit Legende |
| **Miro einlesen** | „Lies das Board wieder ein“ | Änderungsliste zur Bestätigung, dann `affinity-map_<projekt>_v4.md` (`step: miro`) |
| **Board aktualisieren** | „Bring die neue Version aufs Board“ | neuer Stand rechts neben dem alten |

---

## So sieht das Board aus

```
[grün  Thema]

[pink    ]  ┌ I09 ───────────────┐  ┌ I10 ───────────────┐
[Insight-]  │ [blau  Insight]    │  │ [blau  Insight]    │
[Cluster ]  │ [gelb]   [gelb]    │  │ [gelb]   [gelb]    │
            │ [gelb]             │  │ [orange Team]      │
            └────────────────────┘  └────────────────────┘

┌ Einzelsignale ─────────┐  ┌ Parkplatz ─────────────┐  ┌ Lücken & offene Fragen ┐
└────────────────────────┘  └────────────────────────┘  └────────────────────────┘
```

| Farbe | Bedeutung |
|---|---|
| gelb | Datenpunkt (Zitat oder Paraphrase), letzte Zeile = ID wie `P03-007` |
| orange | Team-Notiz |
| blau | Insight (L1) – jeder Insight ist ein eigener Frame |
| violett | Orchid – Insight, den nur eine Person liefert, der aber so wertvoll ist, dass er bewusst eigenständig bleibt |
| pink | Insight-Cluster (L2) – gilt für die Reihe rechts daneben |
| grün | Thema (L3) – gilt für den Block darunter |
| grau | Lücke oder offene Frage |

---

## Was das Team auf dem Board tun kann

| Aktion | Was beim Einlesen passiert |
|---|---|
| Zettel in einen anderen Frame ziehen | Datenpunkt wandert in diesen Insight |
| Blauen Titel umformulieren | Insight bekommt den neuen Titel, der alte bleibt dokumentiert |
| Titel-Sticky violett färben bzw. zurück auf blau | Insight wird zum Orchid bzw. verliert den Status (Begründung ergänzt der Skill als Vorschlag) |
| Zettel in den Frame „Einzelsignale“ ziehen | Aussage wartet dort auf Bestätigung durch weitere Interviews |
| Neuen Frame mit blauem Titel anlegen | neuer Insight, vom Skill mit Job-Dimensionen ergänzt (als Vorschlag) |
| Frame leeren oder löschen | Insight wird aufgelöst |
| Neuen Zettel mit Zitat schreiben | wird im Transkript gesucht und – wenn gefunden – zum regulären Datenpunkt |
| Neuen Zettel mit eigener Notiz | wird zur **Team-Notiz** – ein gleichwertiger Datenpunkt mit Quelle „Team“ |
| Zettel in „Lücken“ ergänzen | neue offene Frage in der Map |
| Pinke/grüne Zettel verschieben oder umformulieren | Insight-Cluster und Themen werden neu gebildet |

**Bitte nicht:** IDs (`P03-007`, `I09`) löschen oder ändern und den Text von Zitat-Zetteln umschreiben. Geänderte Zitate werden nicht übernommen – der Originalwortlaut bleibt, damit jede Aussage auf das Interview zurückführbar ist. Gelöschte Zettel gehen nicht verloren, sie landen auf dem Parkplatz.

Die Deutungshoheit liegt beim Team: Titel, Zuordnungen und neue Insights des Teams setzt die Qualitätssicherung nicht zurück und bewertet sie nicht inhaltlich – sie prüft nur, ob IDs, Zitate und Zählungen stimmen.

---

## Ablauf beim Einlesen

1. Der Skill liest den Bereich des letzten Exports vom Board.
2. Ein Skript vergleicht das Board mit der Map und erstellt eine **Änderungsliste**.
3. Du bestätigst die Liste als Ganzes. Was das Team auf dem Board gebaut hat, gilt – auch die Zuordnung zu Clustern und Themen nach Lage. Rückfragen gibt es nur bei technischen Unklarheiten, etwa einem Zitat, das in mehreren Transkripten vorkommt.
4. Erst dann entsteht eine neue Map-Version mit Eintrag im Entwicklungsprotokoll und Qualitätssicherung.

Wird inzwischen ein neues Transkript eingearbeitet, fragt `affinity-mapping` vorher, ob das Board zuerst eingelesen werden soll – sonst laufen zwei Stände auseinander.

---

## Datenschutz

- Auf das Board kommt nur die **pseudonymisierte Map**, nie Transkripte, Sprecherzuordnungen oder Klarnamen.
- Miro ist ein eigener Anbieter. Vor dem ersten Export klären, ob Projektdaten dort verarbeitet werden dürfen.
- Das Board nur mit Projektbeteiligten teilen und nach Projektende gemäß den vereinbarten Fristen löschen.

---

## Voraussetzungen & Grenzen

- **Miro-MCP** muss im KI-Tool verbunden sein, außerdem Python 3 für `scripts/miro.py`.
- Für den Rücksync wird `affinity-mapping` mit seinem Skript `amap.py` gebraucht (Überblick, QS).
- **Tags** kann der Skill über das MCP nicht setzen. Die Person steht deshalb in der ID-Zeile. Selbst gesetzte Tags werden gelesen, aber nicht ausgewertet.
- **Kommentare, Reaktionen und Votes** werden nicht übernommen.
- Insight-Cluster und Themen werden über die **Position** zugeordnet. Bei stark umgebauten Boards fragt der Skill nach.
- Gelesen wird der Bereich des letzten Exports plus Rand. Weit weggezogene Zettel werden nicht gefunden.

---

## Dateien

| Datei | Inhalt |
|---|---|
| `miro_<projekt>.json` | Sync-Datei: Board-URL, exportierte Versionen, Board-Bereiche, Einlese-Verlauf |
| `miro-export_<projekt>_v<n>_teil<k>.svg` | erzeugter Board-Stand, wie er an Miro geschickt wird |
| `miro-read_<projekt>_<datum>.svg` | eingelesener Board-Stand |
| `affinity-map_<projekt>_v<n>.md` mit `step: miro` | neue Map-Version nach dem Einlesen |
