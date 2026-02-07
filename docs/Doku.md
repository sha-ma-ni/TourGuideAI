Virtuelle Umgebung erstellen:
```bash
python3 -m venv venv
``` 

Aktivieren der virtuellen Umgebung:
```bash
venv/Scripts/activate
```

Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```
Kommentar: Installiert alle benötigten Python‑Pakete für das Projekt.


ProjektStruktur:
```project/
├── venv/                  # Virtuelle Umgebung
├── data/                  # Datendateien
├── notebooks/             # Jupyter Notebooks
├── src/                   # Quellcode
    ├── __init__.py        # Initialisierungsdatei
    ├── loader.py          # Laden und Vorverarbeiten von Daten
    ├── embeddings.py      # Erstellen von Embeddings
    ├── vektors.py         # Vektoroperationen (Chroma/FAISS initialisieren)
    └── rag.py             # Retrieval + LLM kombinieren
├── app.py                 # Hauptanwendung    
├── requirements.txt       # Abhängigkeiten
└── README.md              # Projektbeschreibung
```


