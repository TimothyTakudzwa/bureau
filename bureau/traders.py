from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db
# Load data preprocessing libraries
import pandas as pd
import numpy as np
# Load vectorizer and similarity measure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@app.route('/trading', methods=['GET', 'POST'])
def trading():
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
    while input_sentence:
        input_sentence_vector = vectorizer.transform([input_sentence])

        # Compute similarities
        similarities = cosine_similarity(input_sentence_vector, Sentence_vectors)

        # Find the closest sentence
        closest = np.argmax(similarities, axis=1)
        category = df.Category.iloc[closest].values[0]
        if category == "c":
            flash('you are converting from which currency ')
            return redirect(url_for('trade'))
        elif category == "b":
            flash('you are converting to which currency')
            return redirect(url_for('trade'))
        elif category == "d":
            return redirect(url_for('tred'))
        else:
            return redirect(url_for('trading'))

        return render_template('trading.html', category = category, input_sentence = input_sentence)
    return render_template('trading.html')

@app.route('/trade', methods=['GET', 'POST'])
def trade():
    df = pd.read_csv("my_csv.csv")
    df.columns = ["Sentence","Category"]
    df.dropna(inplace=True)
    # Train the vectorizer
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.Category)))
    # Vectorize sentences
    Sentence_vectors = vectorizer.transform(df.Sentence)
    
    # user input
    currency = request.form.get('currency')
    amount = request.form.get('amount')
    while currency and amount:
        input_sentence_vector = vectorizer.transform([currency])

        # Compute similarities
        similarities = cosine_similarity(input_sentence_vector, Sentence_vectors)

        # Find the closest sentence
        closest = np.argmax(similarities, axis=1)
        category = df.Category.iloc[closest].values[0]
        if category == "us":
            return redirect(url_for('trader'))
        elif category =="zwl":
            return redirect(url_for('trader'))
        else:
            return redirect(url_for('trade'))

        return render_template('trade.html', category = category, currency = currency, amount = amount)

    return render_template('trade.html')

@app.route('/trad', methods=['GET', 'POST'])
def trad():
    df = pd.read_csv("my_csv.csv")
    df.columns = ["Sentence","Category"]
    df.dropna(inplace=True)
    # Train the vectorizer
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.Category)))
    # Vectorize sentences
    Sentence_vectors = vectorizer.transform(df.Sentence)
    
    # user input
    currency = request.form.get('currency')
    amount = request.form.get('amount')
    rate = request.form.get('rate')
    while currency and amount:
        input_sentence_vector = vectorizer.transform([currency])

        # Compute similarities
        similarities = cosine_similarity(input_sentence_vector, Sentence_vectors)

        # Find the closest sentence
        closest = np.argmax(similarities, axis=1)
        category = df.Category.iloc[closest].values[0]
        if category == "us":
            return redirect(url_for('trader'))
        elif category =="zwl":
            return redirect(url_for('trader'))
        else:
            return redirect(url_for('trad'))

        return render_template('trad.html', category = category, currency = currency, amount = amount, rate = rate)

    return render_template('trad.html')

@app.route('/tred', methods=['GET', 'POST'])
def tred():
    # user input
    amount = request.form.get('amount')
    rate = request.form.get('rate')
    if amount and rate:
        return redirect(url_for('trader'))
    return render_template('tred.html',amount = amount, rate = rate)

@app.route('/trader', methods=['GET', 'POST'])
def trader():
    return render_template('completed.html')