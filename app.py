# app.py
from flask import Flask, jsonify
from scraper import scrape_notices

app = Flask(__name__)

# Define the API route for scraping
@app.route('/api/notices', methods=['GET'])
def get_notices():
    notices_data = scrape_notices()
    return jsonify(notices_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


