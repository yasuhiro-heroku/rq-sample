web: gunicorn app:app
worker: rq worker -u "$REDIS_URL?ssl_cert_reqs=none" default