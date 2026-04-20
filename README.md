# cftc-app

CFTC Commitment of Traders Workspace Application Service

## Running Locally

### API only

```bash
docker build -t cftc-app .
docker run --rm -p 7750:7750 -e CFTC_APP_TOKEN=<your_token> cftc-app
```

The API will be available at `http://localhost:7750`.

### With Docker Compose

```bash
CFTC_APP_TOKEN=<your_token> docker compose -f docker-compose.cftc.yml up --build
```

The API will be available at `http://localhost` (port 80).

CORS and caching are handled at the application level. GET 200 responses to `/api/v1/cftc/cot` include a `Cache-Control: public, max-age=604800` header (7 days).

## Deployment

Deployment is automated via GitHub Actions using [Dokku](https://dokku.com). Pushing to `main` triggers a deploy.
