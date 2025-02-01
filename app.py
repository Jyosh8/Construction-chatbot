from flask import Flask, request, jsonify, render_template
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Initialize Flask app
app = Flask(__name__)

# Load the chatbot model and data
lemmatizer = WordNetLemmatizer()
intents = json.loads(open("C:\\python projects\\chatbot\\intents.json", encoding="utf-8").read())
words = pickle.load(open("words.pkl", 'rb'))
classes = pickle.load(open("classes.pkl", 'rb'))
model = load_model("chatbot_model.keras")

# Function to clean up and tokenize the sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Function to create a bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Function to predict the intent of the user's message
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]
    
    # Debugging: Print the predicted intents and their probabilities
    print("Predicted Intents:", return_list)
    
    return return_list

# Function to get a response based on the predicted intent
def get_response(intents_list, intents_json):
    if not intents_list:
        # If no intent matches, return the fallback response
        for intent in intents_json['intents']:
            if intent['tag'] == 'fallback':
                return random.choice(intent['responses'])
    
    # If an intent is found, return the corresponding response
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    
    # If no intent matches, return the fallback response
    for intent in intents_json['intents']:
        if intent['tag'] == 'fallback':
            return random.choice(intent['responses'])

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file

# Route to handle chatbot requests
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']  # Get the user's message
    ints = predict_class(user_message)  # Predict the intent
    res = get_response(ints, intents)  # Get the response
    return jsonify({'response': res})  # Return the response as JSON

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
