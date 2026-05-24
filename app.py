from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)

MAX_SIZE = 5 * 1024 * 1024  # 5MB

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('image')
    if not f:
        abort(400)

    data = f.read(MAX_SIZE + 1)
    if len(data) > MAX_SIZE:
        abort(413)

    # Usa imgbb (gratuito, sem conta necessária para API pública)
    resp = requests.post(
        'https://api.imgbb.com/1/upload',
        data={'key': '2e46da7f4e8ede09d9b54609b03d04dc'},
        files={'image': ('upload.jpg', data, f.content_type)},
        timeout=30
    )

    if resp.status_code != 200:
        abort(502)

    result = resp.json()
    public_url = result['data']['url']
    lens_url = 'https://lens.google.com/uploadbyurl?url=' + requests.utils.quote(public_url)
    return jsonify({'lens_url': lens_url})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
