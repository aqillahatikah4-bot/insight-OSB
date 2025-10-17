from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route('/')
def home():
    return send_from_directory("static", "index.html")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
