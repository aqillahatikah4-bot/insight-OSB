from flask import Flask, request, jsonify, send_from_directory
import requests
import csv
from io import StringIO
import os

app = Flask(__name__, static_folder="static")

@app.route('/proxy')
def proxy():
    sheet_url = request.args.get('sheet')
    if not sheet_url:
        return jsonify({"error": "Tiada URL sheet diberikan"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0 Safari/537.36"
    }

    try:
        response = requests.get(sheet_url, headers=headers, timeout=10)
        response.raise_for_status()
        csv_text = response.text.strip()

        # ?? Semak kalau fail bukan CSV tapi HTML (Google block)
        if csv_text.startswith("<") or "DOCTYPE html" in csv_text:
            return jsonify({
                "error": "Link bukan CSV sebenar. Google mungkin sekat permintaan direct.",
                "note": "Cuba guna link export?format=csv"
            }), 400

        # Tukar CSV ke JSON
        f = StringIO(csv_text)
        reader = csv.DictReader(f)
        data = [row for row in reader if any(row.values())]

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Gagal ambil CSV: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
