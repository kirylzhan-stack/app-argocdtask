import os
import time
import threading
import logging
import psutil
from flask import Flask, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge, CollectorRegistry

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CUSTOM_REGISTRY = CollectorRegistry()

CPU_GAUGE = Gauge('app_cpu_percent', 'Current CPU usage by the application (in %)', registry=CUSTOM_REGISTRY)
MEMORY_GAUGE = Gauge('app_memory_usage_bytes', 'Current RAM usage by the application (in bytes)', registry=CUSTOM_REGISTRY)

def background_task():
    process = psutil.Process(os.getpid())
    while True:
        mem_info = process.memory_info().rss / 1024 / 1024
        logger.info(f"LOG-GENERATOR: App is alive. Memory usage: {mem_info:.2f} MB. Next log in 30s.")
        time.sleep(30)

@app.route('/')
def hello():
    image_name = os.getenv('IMAGE_NAME', 'Unknown')
    secret = os.getenv('SECRET', 'Not Set')
    
    return f"""
    <html>
        <body style="background-color: #444; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif;">
            <div style="text-align: center; color: white;">
                <h1 style="font-size: 40px;">Web-application for k8s megatask!</h1>
                <p style="font-size: 24px; color: #FF0000;">Secret: {secret}</p>
                <p style="font-size: 18px; color: #00ff00;">Image: {image_name}</p>
            </div>
        </body>
    </html>
    """

@app.route('/metrics')
def metrics():
    process = psutil.Process(os.getpid())
    cpu_usage = process.cpu_percent(interval=None)
    CPU_GAUGE.set(cpu_usage)
    
    memory_usage = process.memory_info().rss
    MEMORY_GAUGE.set(memory_usage)
    
    return Response(generate_latest(CUSTOM_REGISTRY), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    t = threading.Thread(target=background_task, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=9090)