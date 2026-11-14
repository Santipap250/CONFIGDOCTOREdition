# OBIXCONFIGDOCTOR
## FPV Drone Configuration Analyzer

OBIXCONFIGDOCTOR is a Flask-based FPV drone configuration and analysis platform. It brings build checks, tuning guidance, configuration analysis, calculators, and pilot tools into one responsive web application.

**Live application:** https://configdoctor.onrender.com/landing  
**GitHub:** https://github.com/Santipap250/OBIXCONFIGDOCTOR---Vercel-Ready-Edition

> The application provides engineering-oriented estimates and checks. Recommendations are starting points, not guarantees; validate every configuration on the bench and in a safe test flight.

## Core capabilities

- **Drone configuration analysis:** frame size, battery, motor KV, propeller, weight, PID and filter setup.
- **Performance estimates:** thrust-to-weight ratio, battery runtime, motor/propeller and RPM filter calculations.
- **Configuration tools:** Betaflight CLI analysis and comparison, CLI Surgeon, PID Advisor, Quick Tune and Rates Visualizer.
- **Flight-data tools:** Blackbox CSV analysis, loop analysis, OSD layout export and tuning log support.
- **Hardware helpers:** Battery Health, Motor Thermal, ESC Checker, VTX tools and FPV Gear recommendations.
- **Community features:** ratings and likes API, downloads, team/about pages and configuration sharing tools.

## Technology

- Python 3.11+ (Vercel deployment uses Python 3.12)
- Flask + Jinja2 + Flask-WTF + Flask-Limiter
- Python standard library for analysis logic; psycopg 3 for persistent PostgreSQL community features
- SQLite for local development; PostgreSQL supported for persistent serverless data
- Gunicorn for Render / conventional WSGI hosting
- Vercel Python runtime for serverless deployment

## Repository layout

```text
OBIXCONFIGDOCTOR/
├── app.py                    # Flask WSGI entrypoint (Vercel detects this)
├── core.py                   # Shared analysis, database and helper logic
├── analyzer/                 # FPV analysis engines
├── blueprints/               # Flask route groups
├── gear/                     # FPV compatibility catalogue/recommender
├── logic/                    # Presets and configuration logic
├── templates/                # Jinja2 pages and partials
├── static/                   # Source assets + local/static fallback
├── public/static/            # Vercel CDN copy of /static assets
├── data/                     # Static JSON catalogue; runtime DB is not committed
├── tests/                    # Automated tests
├── requirements.txt
├── vercel.json
├── .python-version
└── README.md
```

## Run locally

1. Install Python 3.11 or newer.
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

3. Create a local environment file and generate a secret key:

```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the generated value into `SECRET_KEY` in `.env`. Keep `.env` private.

4. Start the app:

```bash
python app.py
```

Open http://127.0.0.1:10000/landing. The local app uses SQLite at `data/community.db`.

## Deploy to Vercel

The repository is prepared for Vercel's current Flask framework detection: `app.py` exposes a top-level WSGI object named `app`; Vercel detects Flask from `requirements.txt`; and `public/static/**` is published through Vercel's static asset CDN, while large static media is excluded from the Python Function bundle. The legacy `builds`/`routes` configuration has been removed.

1. Push this repository to GitHub.
2. In Vercel, select **Add New → Project**, import `Santipap250/OBIXCONFIGDOCTOR---Vercel-Ready-Edition`, and keep the project root at `/`.
3. Leave Build Command and Output Directory on their automatic defaults.
4. Add the required environment variables before the first production deployment:

| Variable | Required | Value / purpose |
|---|---:|---|
| `SECRET_KEY` | Yes | Random secret, at least 32 bytes; generate with Python `secrets.token_hex(32)` |
| `FLASK_DEBUG` | Yes | `0` |
| `TRUST_PROXY` | Yes | `1` for Vercel's trusted proxy headers |
| `FORCE_INSECURE` | Yes | `0` |
| `BASE_URL` | Recommended | Production URL, e.g. `https://your-domain.vercel.app` |
| `DATABASE_URL` | Recommended | Managed PostgreSQL URL for persistent ratings/likes |
| `REDIS_URL` | Optional | Shared Redis URL for distributed rate limiting |

5. Deploy a Preview first. Verify `/healthz`, `/landing`, `/app`, `/rates-visualizer`, `/team`, `/downloads` and `/static/img/configdoctor-logo.png`. Then promote to Production.

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed setup, database notes and troubleshooting.

### Serverless storage notes

- Vercel Functions have a read-only application filesystem; only `/tmp` is writable scratch space. OSD saved exports therefore use a temporary directory on Vercel. They are not permanent file storage.
- SQLite on `/tmp` is only a fallback. It is ephemeral and local to a function instance; ratings and likes will not be durable or shared across all instances without `DATABASE_URL`. Configure a managed PostgreSQL database for production community data.
- The app limits Vercel upload requests to 4 MB to stay below the platform's 4.5 MB function request-body limit. Larger Blackbox/CSV files need client-side/object storage or a hosting platform that accepts larger request bodies.
- In-memory rate limiting is a fallback. For consistent cross-instance rate limits, configure `REDIS_URL`.

## Render / Gunicorn compatibility

The existing `Procfile`, `render.yaml` and Gunicorn setup are retained for conventional hosting. Local and Render deployments continue to use the `static/` source directory and SQLite unless `DATABASE_URL` is configured.

## Tests

Install development requirements and run:

```bash
pip install -r requirements-dev.txt
pytest -q
```

The automated suite covers route smoke tests, analyzer logic, CLI validation, Blackbox input handling, downloads hardening and related calculations. A deployment smoke test should still be run on the Vercel Preview URL because platform-specific limits cannot be fully reproduced by unit tests.

## Copyright

Copyright © 2026 Santipap. All rights reserved. See [LICENSE](LICENSE). Third-party dependencies and assets remain subject to their own licenses.
