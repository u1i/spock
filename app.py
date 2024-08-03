from flask import Flask, request, jsonify, render_template
from urllib.parse import urlparse, urlunparse
import uuid
import datetime
import requests

app = Flask(__name__)

# In-memory storage (replace with a database in a production environment)
endpoints = {}

def get_public_url():
    # Start with assuming the request's own scheme and host
    scheme = request.scheme
    host = request.host

    # Check for common headers that indicate HTTPS
    if any(request.headers.get(header) for header in [
        'X-Forwarded-Proto',
        'X-Forwarded-Ssl',
        'X-Url-Scheme',
    ]) == 'https':
        scheme = 'https'

    # Check for cloud provider headers
    for header in ['X-Forwarded-Host', 'X-Original-Host', 'Host']:
        if header in request.headers:
            host = request.headers[header]
            break

    # Construct the base URL
    base_url = urlunparse((scheme, host, '', '', '', ''))
    
    return base_url

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
    
    base_url = get_public_url()
    endpoint_url = f"{base_url}/endpoint/{endpoint_id}"
    
    return render_template('endpoint.html', 
                           endpoint_id=endpoint_id, 
                           requests=endpoints[endpoint_id], 
                           endpoint_url=endpoint_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
