from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# ============ HATUA 1: Weka API key ya OMDb ============
# Tembea hapa: https://www.omdbapi.com/apikey.aspx na register ili kupata API key
OMDB_API_KEY = "YOUR_OMDB_API_KEY"  # Badilisha na API key yako halisi
OMDB_BASE_URL = "https://www.omdbapi.com/"

# ============ HATUA 2: Dictionary ya Kiswahili kwa chatbot ============
SWAHILI_RESPONSES = {
    "habari": "Habari! Nzuri sana, asante kwa kuuliza. Ninataka kusaidia!",
    "jina lako nani": "Jina langu ni Movie Bot, msaada wako wa filamu.",
    "karibu": "Karibu sana! Tunajifurahia kuwa na wewe hapa.",
    "asante": "Kwa karibuni! Niko hapa kusaidia.",
    "filamu gani": "Unaweza kutafuta filamu yoyote katika search bar. Jaribu kutafuta jina la filamu unayopienda!",
    "unavyopigia heshima": "Ninapiga heshima filamu za aksheni, sensa, na sinema.",
    "bye": "Kwaheri! Karamu salama hadi mwingine.",
    "": "Karibu tena! Ni nini kinachokukumbuza?"
}

# ============ HATUA 3: Chagua jibu katika Kiswahili ============
def get_kiswahili_response(user_input):
    """
    Njia: Onesha jibu la Kiswahili kulingana na ujumbe wa mtumiaji.
    - user_input: ujumbe kutoka kwa mtumiaji
    - Rudi: jibu la Kiswahili
    """
    user_input_lower = user_input.lower().strip()
    
    # Angalia kama ujumbe upo katika dictionary
    if user_input_lower in SWAHILI_RESPONSES:
        return SWAHILI_RESPONSES[user_input_lower]
    
    # Tafuta maneno yenye kufanana
    for key, response in SWAHILI_RESPONSES.items():
        if key in user_input_lower or user_input_lower in key:
            return response
    
    # Jibu la kawaida
    return f"Asante kwa ujumbe '{user_input}'. Jaribu kuuliza kitu kingine au tafuta filamu!"

# ============ HATUA 4: Tafuta filamu kutoka OMDb API ============
def search_movies(movie_name):
    """
    Njia: Tafuta filamu katika OMDb API.
    - movie_name: jina la filamu
    - Rudi: JSON data ya filamu au ujumbe wa hitilafu
    """
    try:
        params = {
            "apikey": OMDB_API_KEY,
            "s": movie_name,  # s = search
            "type": "movie"
        }
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        data = response.json()
        
        if data.get("Response") == "True":
            return {"success": True, "movies": data.get("Search", [])}
        else:
            return {"success": False, "message": "Hakuna filamu iliyopatikana. Jaribu kuandika jina tofauti!"}
    except Exception as e:
        return {"success": False, "message": f"Hitilafu: {str(e)}"}

# ============ HATUA 5: Njia kuu (Home Page) ============
@app.route('/')
def home():
    """
    Njia: Onesha homepage yenye search bar na chatbot
    """
    return render_template('index.html')

# ============ HATUA 6: API endpoint ya kutafuta filamu ============
@app.route('/api/search', methods=['POST'])
def api_search():
    """
    Njia: Takatika ujumbe kutoka frontend na tafuta filamu
    """
    data = request.json
    movie_name = data.get('movie', '').strip()
    
    if not movie_name:
        return jsonify({"success": False, "message": "Tafadhali andika jina la filamu!"})
    
    result = search_movies(movie_name)
    return jsonify(result)

# ============ HATUA 7: API endpoint ya chatbot ya Kiswahili ============
@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    Njia: Takatika ujumbe wa chatbot na rudi jibu la Kiswahili
    """
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"response": "Karibu andika ujumbe!"})
    
    bot_response = get_kiswahili_response(user_message)
    return jsonify({"response": bot_response})

# ============ HATUA 8: Error handling ============
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ukurasa haujapatikana"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Hitilafu ya ndani ya seva"}), 500

# ============ HATUA 9: Endesha app ============
if __name__ == '__main__':
    # Cheza: debug=True - kwenye kazi / debug=False - kwenye uzalishaji
    app.run(debug=True, host='localhost', port=5000)
