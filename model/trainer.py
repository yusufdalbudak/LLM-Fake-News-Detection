import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Suppress TensorFlow warnings

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pickle
import os

try:
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(os.path.dirname(current_dir), 'dataset')
    
    # Print paths for debugging
    print(f"Current directory: {current_dir}")
    print(f"Dataset directory: {dataset_dir}")
    
    # Check if dataset files exist
    fake_path = os.path.join(dataset_dir, 'fake.csv')
    true_path = os.path.join(dataset_dir, 'true.csv')
    
    if not os.path.exists(fake_path):
        raise FileNotFoundError(f"fake.csv not found at {fake_path}")
    if not os.path.exists(true_path):
        raise FileNotFoundError(f"true.csv not found at {true_path}")
    
    # Load datasets
    print("Loading datasets...")
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)
    
    print(f"Loaded {len(fake_df)} fake news and {len(true_df)} true news articles")
    
    # Rest of your code...
    fake_df['label'] = 0
    true_df['label'] = 1
    
    combined_df = pd.concat([fake_df, true_df], ignore_index=True)
    
    tokenizer = Tokenizer(num_words=5000, lower=True)
    tokenizer.fit_on_texts(combined_df['text'].values)
    X = tokenizer.texts_to_sequences(combined_df['text'].values)
    X = pad_sequences(X, maxlen=250)
    
    # Save tokenizer
    tokenizer_path = os.path.join(current_dir, 'tokenizer.pkl')
    print(f"Saving tokenizer to {tokenizer_path}")
    with open(tokenizer_path, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Continue with model training...
    Y = combined_df['label'].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    model = Sequential()
    model.add(Embedding(5000, 128, input_length=X.shape[1]))
    model.add(SpatialDropout1D(0.2))
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    print("Training model...")
    model.fit(X_train, Y_train, epochs=5, batch_size=64, validation_data=(X_test, Y_test), verbose=2)
    
    # Save model
    model_path = os.path.join(current_dir, 'trained_model.h5')
    print(f"Saving model to {model_path}")
    model.save(model_path)
    
    print("Training completed successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}") 