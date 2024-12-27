import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Suppress TensorFlow warnings

from flask import Flask, request, render_template, flash
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def init_model_and_tokenizer():
    try:
        model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
        model_path = os.path.join(model_dir, 'trained_model.h5')
        tokenizer_path = os.path.join(model_dir, 'tokenizer.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found. Please run trainer.py first to create {model_path}")
        
        if not os.path.exists(tokenizer_path):
            raise FileNotFoundError(f"Tokenizer file not found. Please run trainer.py first to create {tokenizer_path}")
        
        model = load_model(model_path)
        
        with open(tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
            
        return model, tokenizer
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        return None, None

model, tokenizer = init_model_and_tokenizer()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Add mock statistics (you can replace with real data)
    stats = {
        'analyzed': 1234,
        'accuracy': 95.5,
        'avg_confidence': 87.3
    }
    
    if request.method == 'POST':
        if model is None or tokenizer is None:
            flash('Model not initialized. Please ensure model files exist and restart the application.')
            return render_template('index.html', stats=stats)
            
        try:
            text = request.form['text']
            if not text.strip():
                flash('Please enter some text to analyze')
                return render_template('index.html', stats=stats)
            
            seq = tokenizer.texts_to_sequences([text])
            padded = pad_sequences(seq, maxlen=250)
            pred = model.predict(padded)
            result = "Likely True" if pred > 0.5 else "Likely False"
            confidence = float(pred[0][0] if pred > 0.5 else 1 - pred[0][0])
            confidence = round(confidence * 100, 2)
            return render_template('index.html', result=result, confidence=f"{confidence}%", stats=stats)
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return render_template('index.html', stats=stats)
    return render_template('index.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True) 