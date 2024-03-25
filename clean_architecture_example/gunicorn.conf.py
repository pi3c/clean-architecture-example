import logging
import os

# Configuration directory
CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# WSGI application
wsgi_app = "external.web_api.main:app_factory()"

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Binding
bind = os.getenv("SERVER_BIND", "0.0.0.0:8000")

# Number of workers
workers = 4

# Daemon
daemon = False

# Access log
accesslog = os.path.join(CONFIG_DIR, "access.log")

# Error log
errorlog = os.path.join(CONFIG_DIR, "error.log")

# Log level
loglevel = "info"

# Access log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Error logger
error_logger = logging.getLogger("gunicorn.error")
error_logger.handlers = []
error_logger.addHandler(logging.FileHandler(errorlog))
error_logger.setLevel(loglevel.upper())

# Access logger
access_logger = logging.getLogger("gunicorn.access")
access_logger.handlers = []
access_logger.addHandler(logging.FileHandler(accesslog))
access_logger.setLevel(loglevel.upper())
access_logger.propagate = False
