### *Projekt*
**"TourGuideAI"** ist ein Retrieval Augmented Generation (RAG) Projekt zur Unterstützung von Touristen bei der Planung ihrer Reise in Brandenburg. Es kombiniert die Leistungsfähigkeit von Large Language Models (LLMs) mit einer Wissensdatenbank, um personalisierte und informative Antworten auf Fragen zu Sehenswürdigkeiten, Öffnungszeiten, Eintrittspreisen und mehr zu liefern.

> **HINWEIS:** Dieses Projekt ist ein Studienprojekt und dient ausschließlich zu Bildungszwecken. Es ist nicht für kommerzielle Nutzung oder öffentliche Bereitstellung gedacht.

### *Motivation*
Reisen gehört zu unserem Alltag. Aber die Planung, welche Sehenswürdigkeiten oder Veranstaltungen man besuchen könnte, dauert oft sehr lange. Ein RAG-System könnte dabei helfen, einfacher und schneller die Reise vorzubereiten. Im Rahmen des Moduls „Besondere Kapitel der Wirtschaftsinformatik“ an der HTW Berlin würde ich ein RAG-System für die Reisen in Brandenburg erstellen.

### *Problemstellung*
Das Hauptproblem liegt darin, dass die Reiseplanung viel Zeit in Anspruch braucht, auch für den Wochenendausflug. Oft sind die relevanten Informationen über verschiedenen Quellen verteilt.
Ein generatives Modell ohne Retrieval reicht hier nicht aus, weil es nur auf Trainingsdaten basiert und die Daten veraltet sein können. Da RAG die Daten aus externen Quellen abruft, werden sie aktuell und geprüft eingebunden, sodass die Antworten tagesaktuell und korrekt sind.

### *Datenquellen*
Die offiziellen Webseiten von Museen und Sehenswürdigkeiten in Brandenburg sind urheberrechtlich geschützt.
Deswegen habe ich nur die Informationen (Fakten) über Öffnungszeiten, Eintrittspreise, etc. von den Webseiten gesammelt, aber nicht die Inhalte selbst. Die Informationen habe ich in einer Datei gespeichert, die für RAG benutzt werden kann.
- https://www.museum-barberini.de/de/
- https://www.plastinarium.de - die Inhalte sind stark geschützt.
- https://www.industriemuseum-brandenburg.de/home
- https://grosser-kahnhafen.de

Folgende Webseite habe ich nur für Orientierung benutzt:
- https://museums-entdecker.de/home/oeffnungszeiten-eintritt
- https://www.reiseland-brandenburg.de/kontakt-services/kontakt-beratung/touristinformationen/

Für "TourGuideAI" habe ich Informationen in JSON-Format gesammelt, die für RAG benutzen werden können.
Außerdem habe ich die Wikipedia-Seite über Tourismus in Brandenburg benutzt. Die Inhalte stehen unter Creative‑Commons‑Lizenz CC BY‑SA 4.0, die Nutzung für RAG und kommerzielle Nutzung erlaubt.
- https://de.wikipedia.org/wiki/Tourismus_in_Brandenburg

### *Funktionsweise*

### *Erwartete Ergebnisse*

### *Projekt starten*
1. Repository clonen:
```bash
git clone   
```
2. Eine virtuelle Umgebung im Projektverzeichnis erstellen:
```bash
python3 -m venv venv
```
3. Virtuelle Umgebung aktivieren: <br>

Für Windows:
```bash
venv/Scripts/activate
```
Für Linux/Mac:
```bash
source venv/bin/activate
```
4. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```     
### *Nutzungsrechte*
- kommerzielle Nutzung ist *nicht erlaubt*
- öffentliche Bereitstellung ist *nicht erlaubt*
- Inhalte dürfen nur für Lern- und Bildungszwecke genutzt werden

#RAG #RetrievalAugmentedGeneration #TourGuideAI #HTWBerlin #BesondereKapitelDerWirtschaftsinformatik #FIW