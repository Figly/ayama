import os

bind = "0.0.0.0:8080"

if os.environ.get("ENVIRONMENT", None) is not None:
    chdir = "/usr/src/app"

loglevel = "WARNING"
max_requests = 10000
max_requests_jitter = 1000
worker_class = "gevent"
workers = "3"

errorlog = "-"
accesslog = "-"

if os.environ.get("DEBUG", False):
    reload = True
    loglevel = "DEBUG"
