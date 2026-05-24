from flask import Flask, request, redirect, abort
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

    resp = requests.post(
        'https://0x0.st',
        files={'file': (f.filename, data, f.content_type)},
        data={'expires': '1'},
        timeout=30
    )
    if resp.status_code != 200:
        abort(502)

    public_url = resp.text.strip()
    from flask import jsonify
    lens_url = 'https://lens.google.com/uploadbyurl?url=' + requests.utils.quote(public_url)
    return jsonify({'lens_url': lens_url})
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
