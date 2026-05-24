from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests, os, base64

app = Flask(__name__)
CORS(app)

MAX_SIZE = 5 * 1024 * 1024

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('image')
    if not f:
        abort(400)

    data = f.read(MAX_SIZE + 1)
    if len(data) > MAX_SIZE:
        abort(413)

    try:
        # freeimage.host aceita base64
        b64 = base64.b64encode(data).decode('utf-8')
        resp = requests.post(
            'https://freeimage.host/api/1/upload',
            data={
                'key': '6d207e02198a847aa98d0a2a901485a5',
                'action': 'upload',
                'format': 'json',
                'source': b64
            },
            timeout=25
        )
        result = resp.json()
        public_url = result['image']['url']
        lens_url = 'https://lens.google.com/uploadbyurl?url=' + requests.utils.quote(public_url)
        return jsonify({'lens_url': lens_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 502

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
