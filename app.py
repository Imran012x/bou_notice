from flask import Flask, jsonify, request
from scraper import scrape_notices

app = Flask(__name__)

# Define the API route for scraping
@app.route('/')
def index():
   return "Notice Board"# Define the API route for scraping
   
@app.route('/api/notices/<int:page>', methods=['GET'])
def get_notices(page):
    section = request.args.get('section')
    notices_data = scrape_notices(section, page)
    return jsonify(notices_data)

if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port,debug=True)



