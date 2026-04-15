# cftc-app
CFTC Commitment of Traders Workspace Application Service

## Running Locally

### API only

```bash
docker build -t cftc-app .
docker run --rm -p 7750:7750 -e CFTC_APP_TOKEN=<your_token> cftc-app
```

The API will be available at `http://localhost:7750`.

### With Nginx (caching + CORS)

```bash
CFTC_APP_TOKEN=<your_token> docker compose -f docker-compose.cftc.yml up --build
```

This starts two API replicas behind an Nginx reverse proxy with response caching and CORS headers. The API will be available at `http://localhost` (port 80).


## Deployment

Deployment is automated via GitHub Actions using [Dokku](https://dokku.com). Pushing to `main` triggers a deploy.

### Required GitHub Repository Secrets

| Secret | Description |
|---|---|
| `DOKKU_HOST` | Dokku server hostname or IP |
| `DOKKU_PROD_REMOTE` | Dokku git remote URL (e.g. `ssh://dokku@host:22/cftc-app`) |
| `DEPLOYER_SSH_PRIVATE_KEY` | SSH private key authorized on the Dokku server |
| `CFTC_APP_TOKEN` | CFTC app token |

### One-time Dokku Server Setup

```bash
dokku apps:create cftc-app
dokku ports:set cftc-app http:80:7750
```
