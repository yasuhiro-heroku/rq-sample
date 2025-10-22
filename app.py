from flask import Flask, jsonify
from rq import Queue
import os
from tasks import heavy_job

app = Flask(__name__)

# Heroku KVS は TLS 必須。`rediss://` を含む REDIS_URL を使う
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
conn = redis.from_url(redis_url, ssl_cert_reqs="none")  # ここがポイント

q = Queue("default", connection=conn)

@app.get("/")
def index():
    # 重い処理を非同期にキュー投入
    job = q.enqueue(heavy_job, 5)  # 5秒スリープの例
    return jsonify({"enqueued": job.id})

