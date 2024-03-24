import os

wsgi_app = "external.web_api.main:app_factory()"
worker_class = "uvicorn.workers.UvicornWorker"
bind = os.getenv("SERVER_BIND", "0.0.0.0:8000")
workers = 4
daemon = False
