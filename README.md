# Golden Compass

Macro-guided gold investment monitoring dashboard targeting Cloud Run deployment.

## Overview

Golden Compass ingests macro and market datasets (FRED real-yield, GVZ, USD index series plus Twelve Data spot prices) and renders a Streamlit UI for trend and volatility insight. The scaffold separates data acquisition, analytics, and presentation layers so additional sources or transformations can be slotted in easily.

```
.
├── app/                  # Streamlit UI entrypoint
├── golden_compass/       # Core Python package (config, data, analytics)
├── scripts/              # Utility scripts (bootstrap cache, etc.)
├── tests/                # Pytest suite seed
├── .streamlit/           # Streamlit runtime configuration
├── Dockerfile            # Container image for Cloud Run
├── pyproject.toml        # Project metadata + optional dev deps
├── requirements.txt      # Runtime dependencies for pip install
└── Makefile              # Developer shortcuts
```

## Quickstart (Local)

1. **Python environment** (>= 3.10):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   make dev-install
   cp .env.example .env  # add provider API keys
   ```
2. **Streamlit app**:
   ```bash
   make run-local
   ```
3. **Tests & lint** (optional):
   ```bash
   make lint
   make test
   ```

## Data Provider Setup

- `FRED_API_KEY`: [Create from FRED](https://fred.stlouisfed.org/docs/api/api_key.html).
- `TWELVE_DATA_API_KEY`: [Twelve Data developer key](https://twelvedata.com/).

Keys can be set in `.env` (auto-read) or injected as environment variables when running or deploying.

## Cloud Run Deployment

1. **Build image**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/golden-compass
   ```
2. **Deploy service**:
   ```bash
   gcloud run deploy golden-compass-dashboard \
     --image gcr.io/PROJECT_ID/golden-compass \
     --region REGION \
     --allow-unauthenticated \
     --set-env-vars FRED_API_KEY=...,TWELVE_DATA_API_KEY=...
   ```
3. Optional: attach a scheduler/Cloud Tasks job to hit `scripts/bootstrap_data.py` in a separate Cloud Run Job for cache warming.

## Extending the Scaffold

- Add new sources in `golden_compass/data/sources.py` and implement corresponding client in `golden_compass/services/`.
- Introduce richer analytics in `golden_compass/analytics/` and wire into the Streamlit views.
- For persistent storage, point `Settings.data_dir` to a mounted volume (Cloud Storage FUSE) or swap for BigQuery/Firestore clients in the loader layer.

## Next Steps

1. Flesh out API clients with error handling/backoff and optional BigQuery persistence.
2. Design Streamlit pages/tabs for macro narratives (e.g., liquidity heat map, COT positioning).
3. Add automated tests for service adapters and analytics helpers.
4. Configure CI (GitHub Actions/Cloud Build) to lint, test, and build the container image.
