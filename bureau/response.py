import time
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
    phone_number = '26377470000111'
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

def update_position(client,position):
    client.position = position
    client.save_to_db()
    return True

def bot_action(message,client):
    if len(message) > 7:
        response_message = analysis_model(message,client)
    elif client.stage == 'menu':
            response_message = menu_handler(message, client)     
    else:     
        if client.stage == 'initial':
            print('I am in here')
            print(client.position)
            print(client.stage)
            response_message = initial_handler(message, client)
        elif client.stage == 'menu':
            response_message = menu_handler(message, client)
            

        elif client.stage == 'proc_handler':
            response_message = proc_handler(message, client)
        
    return response_message


def proc_handler(message, client):
    if client.nlp_stage == 'sell':      
        response_message = proc_decode(message,client,'sell')       
    elif client.nlp_stage == "buy":
        response_message = proc_decode(message,client,'buy')         
    return response_message


def proc_decode(message, client, action):
    req = Requests.get_by_id(client.last_request_id)
    req.action = action.upper()
    req.save_to_db()    
    message_amount = [int(s) for s in message.split() if s.isdigit()]    
    my_currencies = Currencies.query.all()
    words = list(message.split())
    message_currencies = []
    for word in words:
        for currency in my_currencies:
            if word.lower() == currency.currency_code.lower():                 
                message_currencies.append(currency.currency_code)
            else:
                pass       
    update_position(client,"1")    
    if len(message_amount) > 0:        
        req.amount = message_amount[0]
        req.save_to_db()       
        response_message = currency_comparator(message, client, True, message_currencies, action, req)        
    else:   
        response_message = currency_comparator(message, client, False, message_currencies, action, req)       
    return response_message

    
def currency_comparator(message, client, with_amount, message_currencies, action, req):
    currency_size = len(message_currencies)
    if currency_size == 1:
        if client.position == 1:
            update_currency(message, req, action, True)
            response_message = 'Which currency do you want' if action == 'buy' else "Which currency do you have"
            update_position(client,2)           
        elif client.position == 2:
            update_currency(message, req, action, False)
            if with_amount:
                update_position(client,0)                
            else:
                update_position(client,3)
                response_message = "How much do you want to sell" if action == "sell" else "How much do you want to buy"
                return "How much do you want to sell"
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)       
        elif client.position == 3: 
            req.amount = message
            update_position(client,0)
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
    elif currency_size == 2:
        if client.position == 1:
            req.currency_a=message_currencies[0]
            req.currency_b=message_currencies[1]
            if with_amount:
                response_message = update_position(client,0)
            else:
                client.position == 2
                client.save_to_db()
                return "How much do you want"
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)           
        elif client.position == 2:
            req.amount = message
            update_position(client,0)
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
    else:
        if client.position == 1:
            response_message = 'Which currency do you have?'
            update_position(client,2)
        elif client.position == 2:
            req.currency_a=message
            response_message = 'which currency do you want'
            update_position(client,3)
        elif client.position == 3:
            req.currency_b =message
            if with_amount:
                response_message = update_position(client,0)
            else:
                client.position = 4 
                client.save_to_db()
                response_message = "How much do you want?"
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
        elif client.position == 4:
            req.amount =message
            update_position(client,0)
            response_message = 'Transaction details\n {0}\n{1}\n{2}\n{3}' .format(req.action, req.currency_a, req.currency_b, req.amount)
           
        req.save_to_db()
    return response_message

def update_currency(message, request, action, vice_versa):
    if vice_versa:
        if action == "buy":
            request.currency_b = message
        else:
            request.currency_a = message
    else:
        if action == "buy":
            request.currency_a = message
        else:
            request.currency_b = message

def initial_handler(message, client):
    bank_list = []
    if client.position == 1:
        client.name = message
        response_message = 'Whats your physical address?'
        update_position(client,2)
    elif client.position == 2:
        client.address = message
        response_message = 'Which bank do you want funds credited in?'
        banks = Banks.query.all() #get exported table contents on trello
        i = 1
        for bank in banks:
            response_message = response_message + str(i) + ". " + bank.bank_name + "\n"
            i += 1
            bank_list.append((bank.bank_name))
        update_position(client,3)
    elif client.position == 3:
        message_response = ''

        message_response = 'Which bank do you want funds credited in?'
        banks = Banks.query.all()
        i = 1
        for bank in banks:
            message_response = message_response + str(i) + ". " + bank.bank_name + "\n"
            i += 1
            bank_list.append((bank.bank_name))
        successful, message = analyze_input(message, bank_list, message_response )

        if successful:
            client.destination_bank = message
            client.save_to_db()
            update_position(client,4)
        else:
            return message
        response_message = 'Please provide the account number'
    elif client.position == 4:
        client.account_no = message
        client.stage = 'menu'
        response_message = 'Thank you for registering with us. Type "menu" proceed to transact!'
        update_position(client,0)
    return response_message



 
def menu_handler(message, client):
    prop_rate = None
    response_message = ""
    if client.position == 0  or message == 'menu':
        response_message = 'Select any of the options below\n 1) Buy\n 2) Sell'
        update_position(client,1)
    elif client.position == 1: 
        req = Requests()
        req.client_id = client.id
        req.date = datetime.now()
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
            update_position(client,2)
                  
        elif message.lower() == 'sell' or message == '2' : 
            req.action = 'SELL'
            currencies = Currencies.query.all()
            response_message = 'Which currency would you like to sell? \n\n'
            i = 1
            for currency in currencies:
                response_message = response_message + str(i) + ". " + currency.currency_name + '\n'
                i += 1
            currencies = [currency.code for currency in currencies]    
            successful, message = analyze_input(message, currencies, response_message )
        
        req.save_to_db()             
        update_position(client,2)  

    elif client.position == 2:
        currencies = Currencies.query.all() 
        currency_list_pop = []
        currency_code = []
        req = Requests.get_by_id(client.last_request_id)
        i = 1

        response_message = 'Which currency would you want? \n\n'

        for currency in currencies:
            currency_list_pop.append((currency.currency_name))
        currency_list_pop.pop(int(message)-1)
        for currency in currency_list_pop:
            response_message = response_message + str(i) + ". " + currency + '\n'
            i += 1

        message_response = ''

        if req.action == 'BUY':
            message_response = 'Which currency would you like to buy? \n\n'
        elif req.action == 'SELL' :
            message_response = 'Which currency would you like to sell? \n\n' 

        i = 1
        for currency in currencies:
            message_response = message_response + str(i) + ". " + currency.currency_name + '\n'
            i += 1   
            currency_code.append(currency.currency_code)      

        successful, message = analyze_input(message,currency_code,message_response)

        if successful:
            req.currency_a = message
            req.save_to_db()
            update_position(client,3)
        else:
            return message 

    elif client.position == 3:
        currencies = Currencies.query.all() 
        req = Requests.get_by_id(client.last_request_id)
        currency_list = []
        for currency in currencies: 
            currency_list.append(currency.currency_code)

        message_response = "Which Currency Do You Want?"   

        i = 1
        for currency in currencies:
            message_response = message_response + str(i) + ". " + currency.currency_name + '\n'
            i += 1   
            currency_list.append(currency.currency_code)
        currency_list.pop(int(message)-1)    
                
        successful, message = analyze_input(message, currency_list, message_response )
        if successful:
            req.currency_b = message
            req.save_to_db()
            response_message = 'Amount?'
            update_position(client,4)
        else:
            return message    


    elif client.position == 4:
        req = Requests.get_by_id(client.last_request_id)
        response_message = ""
        tran = ""
        if req:
            req.amount = message
            req.save_to_db()
            rate = Rates.query.filter_by(currency_a=req.currency_a.upper()).filter_by(currency_b=req.currency_b.upper()).order_by(desc('rate')).first()  
            if rate is not None:
                prop_rate = round(rate.rate,2)
                total_amt = round((rate.rate * req.amount))
                response_message = f"Hi, I Have Found A Rate Of Based On Your Input. The Amount Will be {total_amt}. Type `Yes` To Accept, `No` To Cancel"

            else:
                response_message = f"There Is No Rate Availabe Matching Your Input "    
        else:
            response_message = "No Request Object Found" 
        update_position(client,5)
    
    elif client.position == 5:
        req = Requests.get_by_id(client.last_request_id)
        response_message = ""
        tran = ""
        prop_rate = Rates.query.filter_by(currency_a=req.currency_a.upper()).filter_by(currency_b=req.currency_b.upper()).order_by(desc('rate')).first()

        if req:
            if message.lower() == 'yes':
                if prop_rate:
                    date = datetime.now()
                    ref_no = 'WBC-' + str(time.time())
                    total_amount = round((req.amount * prop_rate.rate),2)
                    tran_code = encrypt(client.id, prop_rate.bureau_id, total_amount, date, prop_rate.rate)
                    tran = Transaction(client_id=client.id, bureau_id=prop_rate.bureau_id, total_amount=total_amount, rate=prop_rate.rate, transaction_type=req.action, date=datetime.now(), reference_number=ref_no, transaction_code=tran_code, completed=True, amount=req.amount)
                    bureau = Bureau.get_by_id(prop_rate.bureau_id) 
                    tran.save_to_db()
                    if tran:
                        response_message = 'Completed! :Transaction details\n {0}\n{1}\n{2}\n{3}\n{4}' .format(tran.id, bureau.name ,tran.total_amount, tran.transaction_type,tran.reference_number)
                    else:
                        response_message = "Transaction Failed"
                else:
                    response_message = f"No Rate Availabe {prop_rate}"
            elif message.lower() == 'no':
                response_message = f'Request: {req.id}, {req.action} Successfully Cancelled.'        
        else:
            response_message = "No Request Object Found"        
            
    return response_message

def analyze_input(message, list_data, response_message):    
    message = message.upper()
    if message.isdigit():      
        if int(message) > len(list_data):
            error_message = "Your Selected Option Is Not On The List " 
            return False, error_message + response_message
        else:
            code = list_data[int(message)-1]
            return True, code
    else:
        if message in list_data:           
            return True, message
        else:
            error_message = "The Option You Entered Is Invalid" 
            return False, error_message + response_message

def analysis_model(message, client):
    print(message,client)
    response_message = ""
    df = pd.read_csv("my_csv.csv")
    df.columns = ["Sentence","nlp_class"]
    df.dropna(inplace=True)
    # Train the vectorizer
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Sentence, df.nlp_class)))
    # Vectorize sentences
    Sentence_vectors = vectorizer.transform(df.Sentence)    
    input_message = vectorizer.transform([message])
    # Compute similarities
    similarities = cosine_similarity(input_message, Sentence_vectors)
    # Find the closest sentence
    closest = np.argmax(similarities, axis=1)
    nlp_class = df.nlp_class.iloc[closest].values[0]
    client.nlp_stage = nlp_class 
    client.stage = 'proc_handler'
    client.position == 1
    client.save_to_db()
    response_message = proc_handler(message, client)  
    return response_message
        