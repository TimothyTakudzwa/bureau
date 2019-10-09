
# Load data preprocessing libraries
import pandas as pd
import numpy as np
# Load vectorizer and similarity measure
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db
from sqlalchemy import desc

@app.route('/response/', methods=['GET', 'POST'])
def response():
    global response_message
    form = ResponseForm()
    phone_number = '26377776'
    phone_number = '26377742'
    response_message = "Hello"
    if request.method == 'POST':
        message = form.request.data
        client = Client.get_by_phone_number(phone_number)
        if client is None: 
            client = Client(stage='initial', position=1, phone_number=phone_number)
            client.save_to_db()
            response_message = 'Hie this is our first time talking. Before we proceed might i know your name'
        else: 
            response_message = bot_action(message,client)
    return render_template('response.html', form = form, response=response_message)

def update_stage(client,position,msg):
    client.position = position
    client.save_to_db()
    return msg

def bot_action(message,client):
    print(client)
    if client.stage == 'initial':
        response_message = initial_handler(message, client)
    elif client.stage == 'menu':
        response_message = menu_handler(message, client)
    elif client.stage == 'proc_hanler':
        response_message == proc_handler(message, client)
    # Please specify stage for menu on your if statement
    #elif client.stage == 'menu': # ammendment 2
       # response_message = menu_handler(message, client)
    return response_message

def proc_handler(client, message):
    #if client.nlp_stage == 'all_data_available':
            
    if client.nlp_stage == "buy_only":
        if client.position == 1:
            req= Requests.get_by_id(client.last_request_id)
            req.action = 'buy' 
            response_message = 'What currency do you have?'
            req.position == 2
            req.save_to_db()
            client.save_to_db()

        elif client.position == 2:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_a = message
            response_message = 'what currency would you want?'
            client.position = 3
            req.save_to_db()
            client.save_to_db() 

        elif client.position == 3:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_b = message
            response_message = 'the amount you have?'
            client.position = 4
            req.save_to_db()
            client.save_to_db()
        
        elif client.position == 4:
            req = Requests.get_by_id(client.last_request_id)
            req.amount = message
            req.save_to_db()
            client.position = 0
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)

        return response_message

    if client.nlp_stage == "sell_only":
        if client.position == 1:
            req= Requests.get_by_id(client.last_request_id)
            req.action = 'sell' 
            response_message = 'What currency do you want to sell?'
            req.position == 2
            req.save_to_db()
            client.save_to_db()

        elif client.position == 2:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_a = message
            response_message = 'what currency would you want?'
            client.position = 3
            req.save_to_db()
            client.save_to_db() 

        elif client.position == 3:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_b = message
            response_message = 'the amount you have?'
            client.position = 4
            req.save_to_db()
            client.save_to_db()
        
        elif client.position == 4:
            req = Requests.get_by_id(client.last_request_id)
            req.amount = message
            req.save_to_db()
            client.position = 0
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
        
        return response_message

    return response_message
           
def initial_handler(message, client):
    if client.position == 1:
        client.name = message
        response_message = 'Whats your physical address'
        response_message = update_stage(client,2,response_message)
    elif client.position == 2:
        client.address = message
        response_message = 'May I know the bank you wish to transfer the funds'
        response_message = update_stage(client,3,response_message)
    elif client.position == 3:
        client.destionation_bank = message
        response_message = 'Please provide the account number'
        response_message = update_stage(client,4,response_message)
    elif client.position == 4:
        client.account_no = message
        client.stage = 'menu'
        response_message = 'Thank you for registering with us. Type "menu" proceed to transact!'
        response_message = update_stage(client,0,response_message)

    elif client.position == 0  or message == 'menu':
        client.position = 1 
        client.save_to_db() 
        response_message = 'Select any of the options below\n 1) Buy\n 2) Sell'
    elif client.position == 1: 
        request = Requests()
        request.save_to_db() 
        if message == 'buy' or message == '1' :
            request.action = 'BUY'
            response_message = 'What currency would you like to buy?'
            request.save_to_db()
        else : 
            request.action = 'SELL'
            response_message = 'What currency would you like to sell?'
            request.save_to_db()
        client.position = 2 
        client.last_request_id = request.id
        client.save_to_db()


    elif client.position == 2: 
        req = Requests.get_by_id(client.last_request_id)
        req.currency_a = message
        response_message = 'what currency would you want?'
        client.position = 3
        req.save_to_db()
        client.save_to_db()
    
    elif client.position == 3:
        req = Requests.get_by_id(client.last_request_id)
        req.currency_b = message
        response_message = 'Amount?'
        client.position = 4
        req.save_to_db()
        client.save_to_db()
    
    elif client.position == 4:
        req = Requests.get_by_id(client.last_request_id)
        req.amount = message
        req.save_to_db()
        client.position = 0
        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
    return response_message
   
    return response_message
    # Please create a separate function to handle the menu and do not mix it with the initial handler, if you are not using this please remove it to avoid having unneccessary code 
    # Identify actions that you are consistent in all your functions and modularize, avoid repeating yourself.
    # Please handle case sensitivity on messae for buy and sell 
 
def menu_handler(message, client):
    if client.position == 0  or message == 'menu':
        response_message = 'Select any of the options below\n 1) Buy\n 2) Sell'
        response_message = update_stage(client,1,response_message)
    elif client.position == 1: 
        # Please add the client_id on the request made and link to the client who is making the request
        request = Requests()
        request.client_id = client.id #First ammendment
        request.save_to_db()
        client.last_request_id = request.id
        client.save_to_db()
        if message.lower() == 'buy' or message == '1' :
            request.action = 'BUY'
            response_message = 'What currency would you like to buy?'
            request.save_to_db()

        elif message.lower() == 'sell' or message == '2' : 
            request.action = 'SELL'
            response_message = 'What currency would you like to sell?'
            request.save_to_db()

        else:
            analysis(message,client)
              
        response_message = update_stage(client,2,response_message)   

    elif client.position == 2: 
        req = Requests.get_by_id(client.last_request_id)
        if req:
            req.currency_a = message
            req.save_to_db()
        else:
            response_message = "No Request Object" 
                  
        response_message = 'what currency would you want?'
        response_message = update_stage(client,3,response_message)        
   
    elif client.position == 3:
        req = Requests.get_by_id(client.last_request_id)
        if req:
            req.currency_b = message
            req.save_to_db()
        else:
            response_message = "No Request Object"     

        response_message = 'Amount?'
        response_message = update_stage(client,4,response_message)

    elif client.position == 4:
        req = Requests.get_by_id(client.last_request_id)
        if req:
            req.amount = message
            req.date = datetime.now()
            req.save_to_db()
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
        else:
            response_message = "No Request Object" 
        
        response_message = update_stage(client,0,response_message)    

    return response_message

def analysis(message,client):
    df = pd.read_csv("my_csv.csv")
    df.columns = ["Sentence","nlp_class"]
    df.dropna(inplace=True)
    # Train the vectorizer
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.nlp_class)))
    # Vectorize sentences
    Sentence_vectors = vectorizer.transform(df.Sentence)
    if message is not None:
        input_message = vectorizer.transform([message])
        # Compute similarities
        similarities = cosine_similarity(input_message, Sentence_vectors)
        # Find the closest sentence
        closest = np.argmax(similarities, axis=1)
        nlp_class = df.nlp_class.iloc[closest].values[0]
        client.nlp_stage = nlp_class
        client.stage = 'nlp_proc'
        client.position == 1
    
    else:
        client.stage = 'menu'
        