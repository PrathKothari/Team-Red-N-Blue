from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
from ml_script import gemini_pro_response

app = Flask(__name__)
CORS(app)

load_dotenv()
api_key = os.getenv("api_key")
genai.configure(api_key=api_key)

@app.route('/recipies', methods=['GET','POST'])
def recipe():
    ingredients = request.form.get('ingredients', None)

    if not ingredients:
        return jsonify({"error": "No data provided"}), 400

    prompt_header = '''
     I would like to create a detailed, step-by-step recipe using everything, with a focus on minimizing or completely eliminating food waste. 
     Please suggest recipes that make the most of all the ingredients I have, ensuring nothing goes unused. 
     If possible, also include a second meal idea that uses any leftovers or scraps efficiently.
     
     I am cooking for one person, but I would like the option to increase the portions by scaling the recipe while keeping the same ratio of ingredients. 
     Please ensure the instructions are clear and easy to follow, with a focus on sustainability and zero waste.
    '''

    prompt = f"\n\nI have following Ingredients: {ingredients}" + prompt_header
    recipes = gemini_pro_response(prompt)

    return recipes

if __name__ == '__main__':
    app.run(debug=True)