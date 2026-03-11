##### Voraussetzungen: 
1. `venv` aktivieren!
2. Instalation der Bibliothek: 

`pip install pymilvus sentence-transformers`

`pip freeze > requirements.txt`

4. Docker Desktop installieren
5. In Projekt Ordner:
```bash
  mkdir docker-milvus
  cd docker-milvus
```
6. Docker-Konfiguration herunterladen:

```bash
  wget https://github.com/milvus-io/milvus/releases/download/v2.4.6/milvus-standalone-docker-compose.yml -O docker-compose.yml
```

Falls `wget` nicht verfügbar, dann einfach im Browser öffnen.

7. Server lokal via Docker starten:

   Im docker-Verzeichnis: 
```bash
  docker-compose up -d
```