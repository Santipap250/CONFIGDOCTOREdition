# Vercel Deployment Guide — OBIXCONFIGDOCTOR

This guide describes deploying the Flask application from GitHub to Vercel. It does not deploy automatically or create cloud resources on your behalf.

## 1. Prepare GitHub

1. Download/extract this project.
2. Commit the complete contents of this folder to the repository root (the folder containing `app.py`, `requirements.txt`, `vercel.json` and `templates/`).
3. Confirm `.env`, `.vercel/`, `data/*.db`, `.venv/` and Python cache files are not committed.

## 2. Import into Vercel

1. Open the Vercel dashboard and choose **Add New → Project**.
2. Import `Santipap250/OBIXCONFIGDOCTOR---Vercel-Ready-Edition` (or the repository where you uploaded this project).
3. Set Root Directory to `/`.
4. Keep Framework Preset on automatic detection / Flask if shown.
5. Do not enter a custom Build Command or Output Directory. Vercel detects Flask through the top-level WSGI object in `app.py` and the Flask dependency in `requirements.txt`.
6. Add the environment variables below, then deploy a Preview.

## 3. Required environment variables

Generate a secret on your own computer:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Add the result as `SECRET_KEY`. Do not paste it into GitHub or share it in chat.

| Name | Value | Required |
|---|---|---:|
| `SECRET_KEY` | Generated random secret | Yes |
| `FLASK_DEBUG` | `0` | Yes |
| `TRUST_PROXY` | `1` | Yes |
| `FORCE_INSECURE` | `0` | Yes |
| `BASE_URL` | `https://<your-production-domain>` | Recommended |
| `DATABASE_URL` | Managed PostgreSQL connection string with SSL | Recommended for production |
| `REDIS_URL` | Managed Redis connection string | Optional |

Set variables for **Preview** and **Production** as appropriate. After assigning a custom domain, update `BASE_URL` to that canonical domain and redeploy.

## 4. Persistent PostgreSQL for community data

`/api/rating` and `/api/like` store votes. A serverless instance cannot rely on a database file inside the deployment directory.

1. Create a managed PostgreSQL database (for example, through a provider supported by your Vercel account).
2. Copy its SSL-enabled connection string into Vercel as `DATABASE_URL`.
3. Deploy again. The application creates the `ratings` and `likes` tables on first use.

If `DATABASE_URL` is not set, the app falls back to SQLite under `/tmp`. This prevents read-only filesystem errors, but it is **temporary instance-local data** and must not be treated as persistent production storage.

## 5. Static files and uploads

- Vercel serves `public/static/**` through its CDN at `/static/**`. The same source files remain under `static/` for local/Render use; image, CSS, JS, video and favicon assets are excluded from the Python Function bundle to reduce its size. Server-side download samples and the manifest/service-worker files remain in the function source tree.
- The project targets a 60-second maximum function duration for compatibility with Vercel Hobby plans. The project uses a 4 MB application upload limit on Vercel. The platform rejects Function request bodies larger than 4.5 MB before Flask sees them. Large Blackbox logs should be reduced or uploaded directly to object storage instead of being posted through the Flask Function.
- OSD export downloads saved with the server-side save option are written to `/tmp` on Vercel. Treat those exports as temporary; the OSD editor's client-side export/download remains the durable user workflow.

## 6. Preview verification

After deployment, open each URL on the Preview domain:

```text
/healthz
/landing
/app
/team
/about
/rates-visualizer
/cli_surgeon
/blackbox
/osd
/downloads
/sitemap.xml
/robots.txt
/static/img/configdoctor-logo.png
/static/img/support-qr.png
```

Expected checks:

- `/healthz` returns JSON `{"status":"ok"}`.
- Pages return HTML rather than a 404/500.
- CSS, images, logo and QR code load without a 404.
- Analyzer form submits and renders a result.
- CLI and Blackbox APIs return validation errors for empty input and results for valid input.
- `/api/rating` returns counts. To verify persistent writes, configure PostgreSQL before testing POST endpoints.

Then inspect Vercel Runtime Logs for Python import errors, missing templates, database connectivity errors and function timeouts before promoting the Preview to Production.

## 7. Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Deployment fails before serving | `SECRET_KEY` missing | Add the variable and redeploy |
| CSS/images 404 | Files not uploaded under `public/static/` | Confirm `public/static` mirrors `static` and commit both |
| Community votes disappear | SQLite `/tmp` fallback is being used | Configure managed PostgreSQL in `DATABASE_URL` |
| 413 on Blackbox upload | Vercel 4.5 MB Function request limit | Reduce the CSV or use direct object storage / another host for large uploads |
| Rate limits vary by instance | In-memory rate-limit store | Configure managed Redis via `REDIS_URL` |
| OSD saved link expires / unavailable after a cold start | `/tmp` scratch storage is ephemeral | Use client-side OSD export or external object storage for durable files |
| Wrong canonical URLs in SEO | `BASE_URL` does not match the production domain | Set `BASE_URL` and redeploy |

## 8. Local parity

Use the Vercel CLI if you want to exercise the same runtime flow locally:

```bash
npm install --global vercel
python -m venv .venv
# activate the environment, then
pip install -r requirements.txt
vercel dev
```

Vercel's current Flask guide recommends `vercel dev` and automatic framework detection. Keep `vercel.json` focused on function settings; do not reintroduce the legacy `builds` / catch-all `routes` configuration.
