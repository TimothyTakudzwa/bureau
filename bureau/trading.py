
# Load data preprocessing libraries
import pandas as pd
import numpy as np
# Load vectorizer and similarity measure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, flash, url_for, redirect, make_response
from .models import * 
from . import app, db
from flask_login import login_required, logout_user, current_user, login_user
from .import login_manager
from twilio.twiml.messaging_response import MessagingResponse

@app.route('/tradings')
def trade():
	return render_template('trading.html')


@app.route('/trading', methods=['GET', 'POST'])
def trading_chatbot():
    df = pd.read_csv("my_csv.csv")
    df.columns = ["Sentence","Category"]
    df.dropna(inplace=True)
    # Train the vectorizer
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.Category)))
    # Vectorize sentences
    Sentence_vectors = vectorizer.transform(df.Sentence)
    
    # user input
    input_sentence = request.form.get('input_sentence')
    # Locate the closest sentence
    input_sentence_vector = vectorizer.transform([input_sentence])

    # Compute similarities
    similarities = cosine_similarity(input_sentence_vector, Sentence_vectors)

    # Find the closest question
    closest = np.argmax(similarities, axis=1)
    category = df.Category.iloc[closest].values[0]
    category = str(category)
        
        
    return render_template("trading.html", category=category ,input_sentence = input_sentence) 
    



   
