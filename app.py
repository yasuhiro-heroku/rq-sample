from flask import Flask, jsonify
from redis import Redis
from rq import Queue
import os
from tasks import heavy_job

app = Flask(__name__)

# Heroku KVS は TLS 必須。`rediss://` を含む REDIS_URL を使う
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
conn = Redis.from_url(redis_url)  # rediss なら自動でTLS

q = Queue("default", connection=conn)

@app.get("/")
def index():
    # 重い処理を非同期にキュー投入
    job = q.enqueue(heavy_job, 5)  # 5秒スリープの例
    return jsonify({"enqueued": job.id})

