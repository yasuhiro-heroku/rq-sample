from flask import Flask, jsonify
from rq import Queue
import os
from urllib.parse import urlparse
import redis  # ← 追加
from tasks import heavy_job

app = Flask(__name__)

# Heroku KVS は TLS 必須。REDIS_URL は rediss:// ... の形
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# Dev Centerの推奨例に準拠（TLS + 証明書検証オフ）
# 参考: https://devcenter.heroku.com/articles/connecting-heroku-redis  (Python セクション)
url = urlparse(redis_url)
conn = redis.Redis(
    host=url.hostname,
    port=url.port,
    password=url.password,
    ssl=(url.scheme == "rediss"),
    ssl_cert_reqs=None,  # ← ここがポイント（自己署名により検証を無効化）
)

q = Queue("default", connection=conn)

@app.get("/")
def index():
    job = q.enqueue(heavy_job, 5)
    return jsonify({"enqueued": job.id})
