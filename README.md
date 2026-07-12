# Josh AI

An enterprise AI assistant built on **IBM watsonx Orchestrate**, served by a lightweight **Flask** backend.

---

## Project structure

```
josh-ai/
├── app.py              ← Flask backend (page routes + /api/config + /health)
├── requirements.txt    ← Python dependencies
├── .env.example        ← Environment variable template (copy to .env)
│
├── index.html          ← Home / landing page
├── chat.html           ← Full-screen Josh AI chat
├── about.html          ← About & help page
├── Menu.html           ← Legacy alias → redirects to index.html
│
├── styles.css          ← Shared dark-mode stylesheet
└── static/
    └── js/
        └── josh.js     ← Frontend JS module (wxO loader, nav, error handling)
```

---

## Quick start

### 1 — Clone and install dependencies

```bash
git clone <repo-url>
cd josh-ai
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2 — Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and confirm the values match your IBM watsonx Orchestrate deployment:

| Variable | Description |
|---|---|
| `ORCHESTRATION_ID` | Orchestrate space/orchestration identifier |
| `HOST_URL` | Regional API endpoint (e.g. `https://us-south.watson-orchestrate.cloud.ibm.com`) |
| `DEPLOYMENT_PLATFORM` | `ibmcloud` |
| `CRN` | Cloud Resource Name for your Orchestrate instance |
| `AGENT_ID` | The deployed agent to load in the chat UI |
| `PORT` | Port Flask listens on (default `5000`) |
| `FLASK_DEBUG` | `true` for hot-reload during development |

### 3 — Run the development server

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## How it works

```
Browser                     Flask (app.py)             IBM watsonx Orchestrate
  │                              │                              │
  │  GET /chat.html              │                              │
  │ ─────────────────────────►  │                              │
  │ ◄─────────────────────────  │                              │
  │                              │                              │
  │  GET /api/config             │                              │
  │ ─────────────────────────►  │                              │
  │ ◄── { orchestrationID,      │                              │
  │        hostURL, agentId… }  │                              │
  │                              │                              │
  │  (josh.js injects wxoLoader) │                              │
  │ ──────────────────────────────────────────────────────────► │
  │ ◄────────────────── wxO chat UI mounts in #root ─────────── │
```

1. Flask serves all HTML/CSS/JS pages.
2. `chat.html` loads [`static/js/josh.js`](static/js/josh.js) as an ES module.
3. `josh.js` calls **`/api/config`** to get the wxO credentials from the server — credentials are **never hardcoded in client-side files**.
4. `josh.js` injects the `wxoLoader.js` script from IBM and calls `wxoLoader.init()`.
5. The wxO SDK mounts the full chat UI inside `<div id="root">`.

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Redirect → `/index` |
| `GET` | `/index` | Home page |
| `GET` | `/chat` | Chat page |
| `GET` | `/about` | About page |
| `GET` | `/api/config` | Returns wxO config as JSON |
| `GET` | `/health` | Liveness probe `{"status":"ok"}` |

---

## Production deployment

### Gunicorn (Linux / macOS)

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
```

### Windows (waitress)

```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Docker (optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

---

## Development tips

- Set `FLASK_DEBUG=true` in `.env` for auto-reload on file changes.
- The `/health` endpoint is useful for container orchestration readiness probes.
- All watsonx credentials are loaded from environment variables — never commit `.env`.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS (ES module) |
| Backend | Python 3.10+, Flask 3, flask-cors, python-dotenv |
| AI | IBM watsonx Orchestrate (wxO embed SDK) |
| Infra | IBM Cloud (us-south) |
