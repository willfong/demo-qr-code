import requests
from fastapi import FastAPI, HTTPException, Header
from .services import util, statsd
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse

app = FastAPI()

# This is only really for serving test files. We would probably serve static
# files from S3 directly.
app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")

@app.get("/.*", include_in_schema=False)
@statsd.statsd_root_stats
def root():
    with open('/app/app/static/index.html') as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/lookup")
@statsd.statsd_root_stats
def lookup(x_forwarded_for: str = Header(None)):
    util.logger.warning(f"IP Address: {x_forwarded_for}")
    return {"msg": x_forwarded_for}


@app.get("/log-output-test")
@statsd.statsd_root_stats
def log_output_test():
    util.logger.debug("logging debug")
    util.logger.info("logging info")
    util.logger.warn("logging warning")
    util.logger.error("logging error")
    return {"msg": "Logging output"}