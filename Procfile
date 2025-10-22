web: gunicorn app:app
worker: rq worker -u $REDIS_URL default?ssl_cert_reqs=none