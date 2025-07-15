# Videoflix Backend Project

Dieses Projekt ist ein vollständiges Backend für einen Netflix-Klon, erstellt mit **Python**, **Django**, **Django REST Framework**, **Docker**, **PostgreSQL** und **Redis**. Es ermöglicht Nutzern, Videos hochzuladen, zu streamen, sich zu registrieren und zu authentifizieren.

---

## Voraussetzungen

- [Docker Desktop](https://www.docker.com/products/docker-desktop) ist zwingend erforderlich.
- [Visual Studio Code](https://code.visualstudio.com/) zum Starten des Projekts inkl. der mitgelieferten Konfigurationsdateien:
  - `docker-compose.yml`
  - `backend.Dockerfile`
  - `backend.entrypoint.sh`
- Das zugehörige Frontend findest du hier:\
  👉 [prepared-frontend-videoflix](https://github.com/MaxLackmann/prepared-frontend-videoflix)
- Testvideos kannst du im Admin Panel problemfrei anlegen.

---

## Nutzung

1. Stelle sicher, dass das Frontend läuft.

2. Klone dieses Projekt:

   ```bash
   git clone https://github.com/MaxLackmann/new-videoflix_backend.git
   cd new-videoflix_backend
   ```

3. Kopiere `.env.template` nach `.env` und passe die Variablen an:

   ```bash
   cp .env.template .env
   ```

4. Starte das Backend:

   ```bash
   docker compose up --build
   ```

5. Das Backend ist nun erreichbar unter:

   ```
   http://localhost:8000
   ```

**Wichtig:** Stelle sicher, dass alle Abhängigkeiten in `requirements.txt` installiert wurden. Falls du lokal entwickelst:

---

## Ziel des Projekts

Dieses Backend wurde entwickelt, um folgende Ziele zu erreichen:

- **Lernorientiert**: Der Aufbau folgt strikt Best Practices.
- **Erweiterbar**: Apps sind klar getrennt (z. B. `content`, `user`, `mailing`) und leicht erweiterbar.
- **Produktionsnah**: Docker, Umgebungsvariablen, RQ-Worker, Video-Konvertierung mit FFmpeg und HLS-Streaming werden realitätsnah verwendet.

---

## Videoauflösungen

Die unterstützten HLS-Auflösungen im Backend sind:

- **480p**
- **720p**
- **1080p**

---

## API-Dokumentation

Die API ist automatisch dokumentiert und unter folgender URL erreichbar:

```bash
http://localhost:8000/api/
```

---

## Tests

```bash
docker compose exec web pytest
```

---

## Hinweise

- Die `.dockerignore` verhindert unnötige Dateien im Container (z. B. `.pyc`, `__pycache__`, `.git`, `.env`, `media/` usw.).
- Der Superuser wird beim Containerstart automatisch aus der `.env` erstellt.
- Videos werden per FFmpeg in HLS (480p, 720p, 1080p) konvertiert und segmentiert.

---

## Hinweis

Dieses Projekt ist **ausschließlich für Schüler der Developer Akademie** gedacht und **nicht zur freien Nutzung oder Weitergabe freigegeben**.

