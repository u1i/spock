from flask import Flask, request, jsonify, render_template
import uuid
import datetime
import requests
from urllib.parse import urlparse

app = Flask(__name__)  # This line was missing

# In-memory storage (replace with a database in a production environment)
endpoints = {}

def get_public_url():
    try:
        # Try to get the ngrok public URL
        ngrok_tunnel = requests.get("http://localhost:4040/api/tunnels").json()
        ngrok_url = ngrok_tunnel['tunnels'][0]['public_url']
        return ngrok_url  # This will include the correct protocol (http or https)
    except:
        # If ngrok is not running, fall back to the request's host
        if request.is_secure:
            protocol = 'https'
        else:
            protocol = 'http'
        return f"{protocol}://{request.host}"

@app.route('/')
def index():
    return render_template('index.html', endpoints=endpoints)

@app.route('/create_endpoint', methods=['POST'])
def create_endpoint():
    endpoint_id = str(uuid.uuid4())[:8]  # Generate a random 8-character hash
    endpoints[endpoint_id] = []
    return jsonify({'endpoint_id': endpoint_id})

@app.route('/endpoint/<endpoint_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def capture_request(endpoint_id):
    if endpoint_id not in endpoints:
        return "Endpoint not found", 404

    request_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'method': request.method,
        'headers': dict(request.headers),
        'args': dict(request.args),
        'form': dict(request.form),
        'data': request.get_data(as_text=True)
    }
    
    if request.is_json:
        request_data['json'] = request.get_json(silent=True)
    else:
        request_data['json'] = None

    endpoints[endpoint_id].append(request_data)
    return "Request captured", 200

@app.route('/view/<endpoint_id>')
def view_endpoint(endpoint_id):
    if endpoint_id not in endpoints:
        return "Endpoint not found", 404
    
    public_url = get_public_url()
    parsed_url = urlparse(public_url)
    endpoint_url = f"{parsed_url.scheme}://{parsed_url.netloc}/endpoint/{endpoint_id}"
    
    return render_template('endpoint.html', 
                           endpoint_id=endpoint_id, 
                           requests=endpoints[endpoint_id], 
                           endpoint_url=endpoint_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
