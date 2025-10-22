web: gunicorn app:app
worker: rq worker -u $REDIS_URL default
# もし定期実行が必要なら（任意）
# clock: rqscheduler -u $REDIS_URL

