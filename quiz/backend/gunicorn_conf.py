# From: https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/315f04413114e938ff37a410b5979126facc90af/python3.7/gunicorn_conf.py

import json
import multiprocessing
import os
from app.core.config import settings

workers_per_core_str = settings.WORKERS_PER_CORE
web_concurrency_str = settings.WEB_CONCURRENCY
host = "0.0.0.0"
port = settings.PORT
use_loglevel = settings.LOG_LEVEL
use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
keepalive = 120
errorlog = "-"
