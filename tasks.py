import time

def heavy_job(seconds: int) -> str:
    time.sleep(seconds)
    return f"done after {seconds}s"
