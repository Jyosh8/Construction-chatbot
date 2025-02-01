import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf  # Updated import
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model  # Corrected import

lemmatizer = WordNetLemmatizer()

# Use correct file path handling
intents = json.loads(open("C:\python projects\chatbot\intents.json", encoding="utf-8").read())
words = pickle.load(open("words.pkl", 'rb'))
classes = pickle.load(open("classes.pkl", 'rb'))
model = load_model("chatbot_model.keras")  # Fixed loading model

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        # Fallback response if no intent matches
        for intent in intents_json['intents']:
            if intent['tag'] == 'fallback':
                return random.choice(intent['responses'])
    tag = intents_list[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    # Fallback response if no intent matches
    for intent in intents_json['intents']:
        if intent['tag'] == 'fallback':
            return random.choice(intent['responses'])

print("GO! Bot is running!")

while True:
    message = input("You: ")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("Bot:", res)
