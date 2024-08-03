from flask import Flask, request, jsonify, render_template, url_for
import uuid
import datetime

app = Flask(__name__)

# In-memory storage (replace with a database in a production environment)
endpoints = {}

def get_host():
    return request.host

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
    
    # Try to parse JSON if the content type is application/json
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
    
    host = get_host()
    endpoint_url = url_for('capture_request', endpoint_id=endpoint_id, _external=True)
    
    return render_template('endpoint.html', 
                           endpoint_id=endpoint_id, 
                           requests=endpoints[endpoint_id], 
                           endpoint_url=endpoint_url,
                           host=host)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
