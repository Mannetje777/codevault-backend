import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Maakt cross-origin requests mogelijk (frontend op Netlify -> backend op Render)

# In-memory opslag voor code snippets
snippets = []

# Root route (health check voor Render en eenvoudige bevestiging dat backend draait)
@app.route('/')
def home():
    return "<h1>CodeVault Backend</h1><p>De backend draait correct.</p>", 200

# Route om alle snippets op te halen of een nieuwe snippet toe te voegen
@app.route('/snippets', methods=['GET', 'POST'])
def handle_snippets():
    if request.method == 'GET':
        # Geef alle snippets terug als JSON
        return jsonify(snippets), 200
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'code' not in data or 'language' not in data:
            return jsonify({"error": "Ongeldige snippet data"}), 400
        # Nieuwe snippet object aanmaken
        snippet = {
            "id": len(snippets) + 1,
            "code": data['code'],
            "language": data['language']
        }
        snippets.append(snippet)
        return jsonify(snippet), 201

# Route voor statistieken (bijv. aantal snippets per taal)
@app.route('/stats', methods=['GET'])
def stats():
    # Tel aantal snippets per programmeertaal
    language_counts = {}
    for s in snippets:
        lang = s.get('language', 'Onbekend')
        language_counts[lang] = language_counts.get(lang, 0) + 1
    # Geef de telling per taal terug als JSON
    return jsonify(language_counts), 200

# Start de Flask-app op de juiste host en poort (gebruik Render's PORT variabele)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
