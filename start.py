"""Wrapper to add Cache-Control headers to the OpenBB API."""

import json
import os
from pathlib import Path

OBB_DIR = Path.home() / ".openbb_platform"


def write_user_settings():
    token = os.environ.get("CFTC_APP_TOKEN", "")
    settings = {"credentials": {"CFTC_APP_TOKEN": token}}
    OBB_DIR.mkdir(parents=True, exist_ok=True)
    (OBB_DIR / "user_settings.json").write_text(json.dumps(settings))


write_user_settings()

from fastapi import Request
from fastapi.responses import JSONResponse
from openbb_platform_api.main import app, launch_api
from starlette.middleware.base import BaseHTTPMiddleware

CACHE_PATHS = {"/api/v1/cftc/cot"}
MAX_AGE = 604800  # 7 days


@app.middleware("http")
async def add_cache_control(request, call_next):
    response = await call_next(request)
    if (
        request.method == "GET"
        and response.status_code == 200
        and any(request.url.path.startswith(p) for p in CACHE_PATHS)
    ):
        response.headers["Cache-Control"] = f"public, max-age={MAX_AGE}"
    return response


class RequireOpenBBUserMiddleware(BaseHTTPMiddleware):
    _EXEMPT_PATHS = {"/health", "/"}

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or request.url.path in self._EXEMPT_PATHS:
            return await call_next(request)
        if not request.headers.get("x-openbb-user"):
            return JSONResponse(
                status_code=403, content={"detail": "Missing required header."}
            )
        return await call_next(request)


app.add_middleware(RequireOpenBBUserMiddleware)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    launch_api(host="0.0.0.0", port=7750)
