import os
import requests
from fastapi import FastAPI, HTTPException, Header
from .services import util, redis
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse

app = FastAPI()

# This is only really for serving test files. We would probably serve static
# files from S3 directly.
app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")


def get_location(ip):
    if not ip:
        ip = "43.230.99.85"
    response = requests.get(f"https://ipinfo.io/{ip}?token={os.environ.get('IPINFO_TOKEN')}")
    return response.json()

@app.get("/lookup")
def lookup(id: str, x_forwarded_for: str = Header(None)):
    redis.incr(id)
    count = redis.get(id)
    location = get_location(x_forwarded_for)
    return {"count": count, "location": location}

@app.get("/report")
def report():
    r = []
    keys = redis.scan()[1]
    for key in keys:
        r.append({"id": key, "count": redis.get(key)})
    return r

@app.get("/.*", include_in_schema=False)
def root():
    with open('/app/app/static/index.html') as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/log-output-test")
def log_output_test():
    util.logger.debug("logging debug")
    util.logger.info("logging info")
    util.logger.warn("logging warning")
    util.logger.error("logging error")
    return {"msg": "Logging output"}