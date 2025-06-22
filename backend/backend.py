from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/api')
def hello():
    pod_name = os.environ.get('POD_NAME', 'unknown')
    pod_ip = os.environ.get('POD_IP', socket.gethostbyname(socket.gethostname()))
    hostname = socket.gethostname()
    
    return {
        "message": "Hello from Backend! Deployment successful.",
        "pod_name": pod_name,
        "pod_ip": pod_ip,
        "hostname": hostname
    }

@app.route('/health')
def health():
    return {"status": "healthy", "hostname": socket.gethostname()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)