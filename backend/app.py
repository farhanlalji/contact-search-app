from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Load sample database
def load_database():
    with open('../data/sample_database.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return "Contact Search API is running!"

@app.route('/api/search', methods=['POST'])
def search():
    """Search for contacts in the database"""
    data = request.json
    search_terms = data.get('names', [])
    
    database = load_database()
    results = []
    
    for term in search_terms:
        term_lower = term.lower()
        for record in database:
            if term_lower in record['name'].lower():
                results.append({
                    'search_term': term,
                    'match': record['name'],
                    'context': record.get('context', 'No additional context'),
                    'source': record.get('source', 'Unknown')
                })
    
    return jsonify({'results': results, 'total': len(results)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)