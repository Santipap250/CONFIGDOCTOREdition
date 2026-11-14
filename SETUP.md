# OBIXCONFIGDOCTOR — Setup Guide

## Local development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Generate a strong secret and place it in `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Start Flask:

```bash
python app.py
```

Open `http://127.0.0.1:10000/landing`.

## Vercel

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md). In short: import the GitHub repository, allow Vercel to detect Flask automatically, set `SECRET_KEY`, `FLASK_DEBUG=0`, `TRUST_PROXY=1` and `FORCE_INSECURE=0`, then deploy a Preview. Configure `DATABASE_URL` for persistent community ratings and likes.

## Render / Gunicorn

The existing `render.yaml` and `Procfile` remain available. Set `SECRET_KEY` in Render and deploy with the existing Gunicorn start command. For durable community data, use managed PostgreSQL through `DATABASE_URL` or a persistent disk for SQLite.
