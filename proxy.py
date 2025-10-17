from flask import Flask, request, jsonify
import requests
import csv
from io import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask proxy berjalan dengan betul ?"

@app.route('/proxy')
def proxy():
    sheet_url = request.args.get('sheet')
    if not sheet_url:
        return jsonify({"error": "Tiada URL sheet diberikan"}), 400
    
    try:
        response = requests.get(sheet_url)
        response.raise_for_status()
        csv_text = response.text

        # Tukar CSV ke JSON
        f = StringIO(csv_text)
        reader = csv.DictReader(f)
        data = [row for row in reader]

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
