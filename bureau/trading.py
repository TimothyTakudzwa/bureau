# Load data preprocessing libraries
import pandas as pd
import numpy as np
# Load vectorizer and similarity measure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, flash, url_for, redirect, make_response
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import * 
from . import app,db
from flask_login import login_required, logout_user, current_user, login_user
from .import login_manager

@app.route('/trading', methods = ['GET, POST'])
def tradingf():
    df = pd.read_excel('data.xlsx',header=None)
    df.columns = ["Sentence","Category"]
    df.dropna(inplace=True) #if any
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.Category)))

    Sentence_vectors = vectorizer.transform(df.Sentence)
    while True:
        sentence = request.form('sentence')

        # Locate the closest sentence
        input_sentence_vector = vectorizer.transform([sentence])

        # Compute similarities
        similarities = cosine_similarity(input_sentence_vector, Sentence_vectors)

        # Find the closest question
        closest = np.argmax(similarities, axis=1)
        currency = df.Category.iloc[closest].values[0]
        print("currency is " + currency)

    '''
        if df.Category.iloc[closest].values[0] =="a":
            print("you are selling which currency?")
            currency = input()
            currency_vector = vectorizer.transform([currency])
            similarity = cosine_similarity(currency_vector, Sentence_vectors)
            closest_currency = np.argmax(similarity, axis=1)
        
            print("currency is " + df.Category.iloc[closest_currency].values[0])
        
            
        else:
            print("Category is " + df.Category.iloc[closest].values[0])
'''
    return render_template("trading.html", sentence = sentence, currency = currency, df = df)
        




@app.route("/housed", methods = ['GET','POST'])
def datahouse(head = None):
    data = pd.read_csv('my_csv.csv')
    head = data
    return render_template('dataset.html',head = head.to_html(index=False, classes='table table-striped table-hover'))
    
        
'''        
 @app.route('/get-agri', methods=['POST'])
def predict_agriculture():
    if request.method == 'POST':
        model = joblib.load('agric_model.pkl')

        print('-----line 27--------')
        print(request.form.get('year_built'))

        year_built = int(request.form.get('year_built'))

        print('line 31')

        agriculture = int(request.form.get('agriculture'))

        agriculture_value = [
            # features
            agriculture
        ]

        # scikit-learn assumes we want to predict the values for many yeras at once, so it expects an array.
        # We just want to look at a single year , so it will be the only item in our array.
        inp = np.asarray(agriculture_value)
        inp = np.reshape(inp,(-1,1))
        scaler = MinMaxScaler(feature_range=(0, 1))
        x = scaler.fit_transform(inp)
        x = np.reshape(x, (x.shape[0], x.shape[1], 1))
        predicted_agriculture_value = model.predict(x)
        predicted_agriculture_value = scaler.inverse_transform(predicted_agriculture_value)

        # Since we are only predicting the gdp of one year, just look at the first prediction returned
        predicted_value = predicted_agriculture_value[0]
        predicted_value = int(predicted_value)

        return render_template("agric.html", pred=predicted_value) 
'''
    
    