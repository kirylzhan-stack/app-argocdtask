import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    image_name = os.getenv('IMAGE_NAME', 'Unknown (variable not set)')
    
    return f"""
    <html>
        <body style="background-color: #808080; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif;">
            <h1 style="font-size: 50px; color: white; text-align: center;">
                Hello!!!!!!!!!!!! This container is running image:<br>
                <span style="color: #f0f0f0;">{image_name}</span>
            </h1>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)