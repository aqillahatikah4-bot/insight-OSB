from flask import Flask, Response, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/proxy')
def proxy():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSA1bscSLT2b4f_gEeFdDPfLePik7R9X29k4jew7jVRLRGbuFP7a--lw3xafVyt1xgG02TdYpKYOagI/pub?gid=0&single=true&output=csv"

    try:
        r = requests.get(sheet_url, timeout=10)
        r.raise_for_status()
        return Response(r.text, mimetype='text/csv')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
