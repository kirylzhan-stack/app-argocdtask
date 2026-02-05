import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    image_name = os.getenv('IMAGE_NAME', 'Unknown (variable not set)')
    return f"Hello! This container is running image: {image_name}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)