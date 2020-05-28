import os

bind = "0.0.0.0:8080"
chdir = "/usr/src/app"
loglevel = "DEBUG"
max_requests = 10000
max_requests_jitter = 1000
worker_class = "gevent"
workers = "3"

errorlog = "-"
accesslog = "-"

if os.environ.get("DEBUG", "False").lower() == "true":
    reload = True
