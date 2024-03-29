from flask import Flask, jsonify, request, Response
import socket
from mockoon_cli import generate_json
from mockoon_cli import generate_yaml
from mockoon_cli import get_unused_port

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def check_health():
    return jsonify({'status' : 'OK', 'hostname' : socket.gethostname()}), 200

@app.route('/api/config', methods=['GET'])
def traefik_dynamic_config():
    output = request.args.get('output')
    if output == 'json':
        content = generate_json()
        mimetype = 'application/json'
        header = {'Content-Disposition':'attachment;filename=services.json'}
    else:
        content = generate_yaml()
        mimetype = 'text/yaml'
        header = {'Content-Disposition':'attachment;filename=services.yaml'}
    return Response(content,
        mimetype=mimetype,
        headers=header)

@app.route('/api/getUnusedPort', methods=['GET'])
def mockoon_cli_get_port():
    port = get_unused_port()
    return jsonify({'port' : port}), 200


## Custom HTTP status error handler ##
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(500)
def interval_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=8000)
