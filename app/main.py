from flask import Flask, jsonify, request, redirect
from threading import Lock
from app.models import URLMapping, url_store
from app.utils import generate_short_code, is_valid_url, isoformat

app = Flask(__name__)

store_lock = Lock()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "Missing 'url' in request body"}), 400
    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"message": "Invalid URL"}), 400
    # Generate unique short code
    with store_lock:
        for _ in range(10):  # Try up to 10 times to avoid collision
            code = generate_short_code()
            if code not in url_store:
                break
        else:
            return jsonify({"message": "Could not generate unique short code"}), 500
        mapping = URLMapping(original_url=long_url, short_code=code)
        url_store[code] = mapping
    short_url = f"http://localhost:5000/{code}"
    return jsonify({"short_code": code, "short_url": short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    with store_lock:
        mapping = url_store.get(short_code)
        if not mapping:
            return jsonify({"message": "URL not found"}), 404
        mapping.click_count += 1
        target_url = mapping.original_url
    return redirect(target_url, code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    with store_lock:
        mapping = url_store.get(short_code)
        if not mapping:
            return jsonify({"message": "URL not found"}), 404
        return jsonify({
            "url": mapping.original_url,
            "clicks": mapping.click_count,
            "created_at": isoformat(mapping.created_at)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)