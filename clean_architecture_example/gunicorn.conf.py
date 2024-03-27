import os

# WSGI application
wsgi_app = "app.web_api.main:app_factory()"

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Binding
host = os.getenv("SERVER_HOST", "0.0.0.0")
port = os.getenv("SERVER_PORT", "8000")
bind = f"{host}:{port}"

# Number of workers
workers = 4

# Daemon
daemon = False
