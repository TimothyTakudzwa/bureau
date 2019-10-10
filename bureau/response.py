
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
from .transactions import *

@app.route('/response/', methods=['GET', 'POST'])
def response():
    form = ResponseForm()
    phone_number = '263774555111'
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

def update_position(client,position,msg):
    client.position = position
    client.save_to_db()
    return msg

def bot_action(message,client):
    print(client)
    if client.stage == 'initial':
        print('I am in here')
        print(client.position)
        print(client.stage)
        response_message = initial_handler(message, client)
    elif client.stage == 'menu':
        response_message = menu_handler(message, client)

    elif client.stage == 'proc_handler':
        response_message = proc_handler(message, client)
    # Please specify stage for menu on your if statement
    return response_message

def proc_handler(client, message):
    #print(client)
    #if client.nlp_stage == 'all_data_available':
    if client.nlp_stage == 'sell':
        if client.position == 1:
            req = Requests.get_by_id(client.last_request_id)
            req.action = 'sell'
            req.save_to_db()
            client.save_to_db() 
            amount = int(filter(str.isdigit, message))
            if amount is not None:
                req.amount = amount
                req.save_to_db()
                client.save_to_db() 
                currencies = Currencies.query.all()
                my_currencies = [currencies]
                words = list(message.split())
                message_currencies = [currency for currency in words if currency in my_currencies]
                currency_size = len(message_currencies)
                client.position == 1

                if currency_size == 1:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        response_message = 'which currency do you want'
                        response_message = update_position(client,2,response_message)           
                    elif client.position == 2:
                        req.currency_b = message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)       
                    return response_message
                
                elif currency_size == 2:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        req.currency_b=message_currencies[1]
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)           
                    return response_message

                else:
                    if client.position == 1:
                        response_message = 'Which currency do you have?'
                        response_message = update_position(client,2,response_message)
                    elif client.position == 2:
                        req.currency_a=message
                        response_message = 'which currency do you want'
                        response_message = update_position(client,3,response_message)
                    elif client.position == 3:
                        req.currency_b =message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message

            else:
                currencies = Currencies.query.all()
                my_currencies = [currencies]
                words = list(message.split())
                req.position == 1
                message_currencies = [currency for currency in words if currency in my_currencies]
                currency_size = len(message_currencies)
                client.position == 1
                
                if currency_size == 1:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        response_message = 'which currency do you want'
                        response_message = update_position(client,2,response_message)
                    elif client.position == 2:
                        req.currency_b = message
                        response_message = 'what is the amount'
                        response_message = update_position(client,3,response_message)                       
                    elif client.position == 3:
                        req.amount = message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message
                                    
                elif currency_size == 2:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        req.currency_b=message_currencies[1]
                        response_message = 'what is the amount'
                        response_message = update_position(client,2,response_message)            
                    elif client.position == 2:
                        req.amount = message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message            
                
                else:
                    if client.position == 1:
                        response_message = 'Which currency do you have?'
                        response_message = update_position(client,2,response_message)
                    elif client.position == 2:
                        req.currency_a=message
                        response_message = 'which currency do you want'
                        response_message = update_position(client,3,response_message)    
                    elif client.position == 3:
                        req.currency_b=message
                        response_message = 'what is the amount'
                        response_message = update_position(client,4,response_message)        
                    elif client.position == 4:
                        req.amount =message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message

    if client.nlp_stage == "buy":
        if client.position == 1:
            req = Requests.get_by_id(client.last_request_id)
            req.action = 'buy'
            req.save_to_db()
            client.save_to_db() 
            amount = int(filter(str.isdigit, message))
            if amount is not None:
                req.amount = amount
                req.save_to_db()
                client.save_to_db() 
                currencies = Currencies.query.all()
                my_currencies = [currencies]
                words = list(message.split())
                message_currencies = [currency for currency in words if currency in my_currencies]
                currency_size = len(message_currencies)
                client.position == 1

                if currency_size == 1:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        response_message = 'which currency do you have'
                        response_message = update_position(client,2,response_message)           
                    elif client.position == 2:
                        req.currency_b = message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)       
                    return response_message
                
                elif currency_size == 2:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        req.currency_b=message_currencies[1]
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)           
                    return response_message

                else:
                    if client.position == 1:
                        response_message = 'Which currency do you want?'
                        response_message = update_position(client,2,response_message)
                    elif client.position == 2:
                        req.currency_a=message
                        response_message = 'which currency do you have'
                        response_message = update_position(client,3,response_message)
                    elif client.position == 3:
                        req.currency_b =message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message

            else:
                currencies = Currencies.query.all()
                my_currencies = [currencies]
                words = list(message.split())
                req.position == 1
                message_currencies = [currency for currency in words if currency in my_currencies]
                currency_size = len(message_currencies)
                client.position == 1
                
                if currency_size == 1:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        response_message = 'which currency do you have'
                        response_message = update_position(client,2,response_message)
                    elif client.position == 2:
                        req.currency_b = message
                        response_message = 'what is the amount'
                        response_message = update_position(client,3,response_message)                       
                    elif client.position == 3:
                        req.amount = message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message
                                    
                elif currency_size == 2:
                    if client.position == 1:
                        req.currency_a=message_currencies[0]
                        req.currency_b=message_currencies[1]
                        response_message = 'what is the amount'
                        response_message = update_position(client,2,response_message)            
                    elif client.position == 2:
                        req.amount = message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message            
                
                else:
                    if client.position == 1:
                        response_message = 'Which currency do you want?'
                        response_message = update_position(client,2,response_message)
                    elif client.position == 2:
                        req.currency_a=message
                        response_message = 'which currency do you have'
                        response_message = update_position(client,3,response_message)    
                    elif client.position == 3:
                        req.currency_b=message
                        response_message = 'what is the amount'
                        response_message = update_position(client,4,response_message)        
                    elif client.position == 4:
                        req.amount =message
                        response_message = update_position(client,0,response_message)
                        response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
                    return response_message        

    elif client.nlp_stage == "buy_only":
        if client.position == 1:
            req= Requests.get_by_id(client.last_request_id)
            req.action = 'buy' 
            response_message = 'Which currency do you have?'
            response_message = update_position(client,2,response_message)
        elif client.position == 2:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_a = message
            response_message = 'which currency would you want?'
            response_message = update_position(client,3,response_message) 
        elif client.position == 3:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_b = message
            response_message = 'the amount you have?'
            response_message = update_position(client,4,response_message)       
        elif client.position == 4:
            req = Requests.get_by_id(client.last_request_id)
            req.amount = message
            response_message = update_position(client,0,response_message)
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
        return response_message

    elif client.nlp_stage == "sell_only":
        if client.position == 1:
            req= Requests.get_by_id(client.last_request_id)
            req.action = 'sell' 
            response_message = 'Which currency do you want to sell?'
            response_message = update_position(client,2,response_message)
        elif client.position == 2:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_a = message
            response_message = 'which currency would you want?'
            response_message = update_position(client,3,response_message) 
        elif client.position == 3:
            req = Requests.get_by_id(client.last_request_id)
            req.currency_b = message
            response_message = 'the amount you have?'
            response_message = update_position(client,4,response_message)       
        elif client.position == 4:
            req = Requests.get_by_id(client.last_request_id)
            req.amount = message
            response_message = update_position(client,0,response_message)
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)       
        return response_message

    return response_message
           
def initial_handler(message, client):
    if client.position == 1:
        client.name = message
        response_message = 'Whats your physical address?'
        response_message = update_position(client,2,response_message)
    elif client.position == 2:
        client.address = message
        response_message = 'Which bank do you want funds credited in?'
        response_message = update_position(client,3,response_message)
    elif client.position == 3:
        client.destination_bank = message
        response_message = 'Please provide the account number'
        response_message = update_position(client,4,response_message)
    elif client.position == 4:
        client.account_no = message
        client.stage = 'menu'
        response_message = 'Thank you for registering with us. Type "menu" proceed to transact!'
        response_message = update_position(client,0,response_message)

    return response_message

 
def menu_handler(message, client):
    response_message = ""
    if client.position == 0  or message == 'menu':
        response_message = 'Select any of the options below\n 1) Buy\n 2) Sell'
        response_message = update_position(client,1,response_message)
    elif client.position == 1: 
        req = Requests()
        req.client_id = client.id
        req.save_to_db()
        client.last_request_id = req.id
        client.save_to_db()
        if message.lower() == 'buy' or message == '1' :
            req.action = 'BUY'
            currencies = Currencies.query.all()
            response_message = 'Which currency would you like to buy? \n\n'
            i = 1
            for currency in currencies:
                response_message = response_message + str(i) + ". " + currency.currency_name + '\n'
                i += 1

            successful, message = analyze_input(message, currencies, response_message )

            response_message = update_position(client,2,response_message)
                  
        elif message.lower() == 'sell' or message == '2' : 
            req.action = 'SELL'
            currencies = Currencies.query.all()
            response_message = 'Which currency would you like to sell? \n\n'
            i = 1
            for currency in currencies:
                response_message = response_message + str(i) + ". " + currency.currency_name + '\n'
                i += 1

            successful, message = analyze_input(message, currencies, response_message )

            req.save_to_db()
      
        else:
            response_message = analysis(message,client)
              
        response_message = update_position(client,2,response_message)   

    elif client.position == 2:
        currencies = Currencies.query.all() 
        req = Requests.get_by_id(client.last_request_id)

        i = 1
        response_message = "Which Currency do you Want?"
        for currency in currencies:
            response_message = response_message + str(i) + ". " + currency.currency_name + '\n'
            i += 1
        successful, message = analyze_input(message,currencies,response_message)
        if successful:
            req.currency_a = message
            req.save_to_db()
            response_message = update_position(client,3,response_message)

        response_message = update_position(client,3,response_message)
   
    elif client.position == 3:
        currencies = Currencies.query.all() 
        req = Requests.get_by_id(client.last_request_id)
        currencies = Currencies.query.all()
        i = 1
        for currency in currencies:
            response_message = response_message + str(i) + ". " + currency.currency_name + '\n'
            i += 1   
        successful, message = analyze_input(message, currencies, response_message )
        if successful:
            req.currency_b = message
            req.save_to_db()
            response_message = 'Amount?'
            response_message = update_position(client,4,response_message)

    elif client.position == 4:
        req = Requests.get_by_id(client.last_request_id)
        response_message = ""
        tran = ""
        if req:
            req.amount = message
            req.date = datetime.now()
            req.save_to_db()
            # Make Transaction With The Highest Available Rate
            
            '''
            if req.action == 'BUY'
                rate = Rates.query.filter_by(currency_a=req.currency_a.upper()).filter_by(currency_b=req.currency_b.upper()).order_by('rate').first()
            elif req.action == 'SELL':
                rate = Rates.query.filter_by(currency_a=req.currency_a.upper()).filter_by(currency_b=req.currency_b.upper()).order_by(desc('rate')).first()
            '''
            rate = Rates.query.filter_by(currency_a=req.currency_a.upper()).filter_by(currency_b=req.currency_b.upper()).order_by(desc('rate')).first()
            if rate:
                date = datetime.now()
                ref_no = "#45653356522"
                total_amount = (req.amount * rate.rate)
                tran = Transaction(client_id=client.id, bureau_id=rate.bureau_id, total_amount=total_amount, rate=rate.rate, transaction_type=req.action, date=datetime.now(), reference_number=ref_no, transaction_code=00000, completed=True, amount=req.amount)
                bureau = Bureau.get_by_id(rate.bureau_id) 
                tran.save_to_db()
                if tran:
                    response_message = 'Completed! :Transaction details\n {0}\n{1}\n{2}\n{3}\n{4}' .format(tran.id, bureau.name ,tran.total_amount, tran.transaction_type,tran.reference_number)
                else:
                    response_message = "Transaction Failed"
            else:
                response_message = f"No Rate Availabe {rate}"    

        else:
            response_message = "No Request Object" 
        
        response_message = update_position(client,0,response_message)    

    return response_message

def analyze_input(message, list_data, response_message):
    currencies = Currencies.query.all()
    currency_codes = [currency.currency_code.lower() for currency in currencies]
    # Check if message is a digit

    if message.isdigit():
        # Check If Value Entered Is Greater Than The len of Currencies
        if int(message) > len(currency_codes):
            error_message = "Your Selected Option Is Not On The List" 
            return False, error_message + response_message
        else:
            code = currency_codes[int(message)-1]
            return True, code
    else:
        if message in currency_codes:
            #Check if message entered is the message list
            #the message is correct
            return True, message
        else:
            #the message is incorrect
            error_message = "The Option You Entered Is Invalid" 
            return False, error_message + response_message

def analysis(message,client):
    response_message = ""
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
        print(nlp_class)
        client.nlp_stage = nlp_class
        client.stage = 'proc_handler'
        print(client.stage)
        client.position == 1
        client.save_to_db()
        print(client.nlp_stage)
        response_message = proc_handler(message, client)
    
    else:
        client.stage = 'menu'
        response_message = menu_handler(message,client)

    return response_message
        