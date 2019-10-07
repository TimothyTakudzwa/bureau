from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db
from sqlalchemy import desc

@app.route('/response/', methods=['GET', 'POST'])
def response():
    form = ResponseForm()
    phone_number = '2637774234490'
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


def bot_action(message,client):
    print(client)
    if client.stage == 'initial':
        print("Got in here")
        response_message = initial_handler(message, client)
    else:
        #response_message = "Test response"
        response_message = initial_handler(message, client)
    return response_message

def initial_handler(message, client):
    if client.position == 1:
        client.name = message
        client.position = 2
        client.save_to_db()
        response_message = 'Whats your physical address'
    elif client.position == 2:
        client.address = message
        client.position = 3
        client.save_to_db()
        response_message = 'May I know the bank you wish to transfer the funds'
    elif client.position == 3:
        client.destionation_bank = message
        client.position = 4
        client.save_to_db()
        response_message = 'Please provide the account number'
    elif client.position == 4:
        client.account_no = message
        client.stage = 'menu'
        client.position = 0
        client.save_to_db()
        response_message = 'Thank you for registering with us. Type "menu" proceed to transact!'
    elif client.position == 0:
        if message == "menu":
            response_message = "Welcome To The Options Menu. Please Press (1) To Select Buy and (2) To Sell"
        elif message == "1":
            '''rqs = ''
            reqs = Requests.query.filter_by(action='BUY').all()
            for req in reqs:
                rqs += str(req.id)+ ") " + str(req.currency_a) + " : " + str(req.currency_b) + " ," + str(req.amount) + " **** "'''
            response_message = "You Have Selected Buy Option. Please  Transact by typing `buy` Followed The Two Currencies You Wish To Trade and amount. Eg `buy USD ZWL 1000`"
            menu_options_handler(client, message)
        elif message.startswith("buy"):
            if len(message.split()) < 4:
                return "Your Command Is Incomplete! Follow this example `Eg buy USD ZWL 1000` "
            currency_a = message.split()[1]
            currency_b = message.split()[2]
            amount = message.split()[3]
            rates = Rates.query.filter_by(currency_a=currency_a).filter_by(currency_b=currency_b).filter_by(action='BUY').order_by('rate').all()
            if not rates :
                return "Sorry No Entries Exist for this query"
            rate = rates[0]    
            req = str(rate.currency_a) + " : " + str(rate.currency_b) + " " +"Rate :{}".format(rate.rate) + " " + "Successful!"
            try:
                request_obj = Requests(currency_a=rate.currency_a, currency_b=rate.currency_b, amount=amount, date=datetime.today(), action='BUY', rating=2)
                request_obj.save_to_db()
                return f"Buying {req}"
            except Exception as e:
                raise e    
                return f"Error Creating Request{req}"   
        elif message == "2":
            response_message = "You Have Selected Sell Option. Initiate Transaction by typing 'sell', Followed The Two Currencies You Wish To Trade and amount. Eg `sell USD ZWL 1000`" 
            menu_options_handler(client, message)
        elif message.startswith("sell"):
            currency_a = message.split()[1]
            currency_b = message.split()[2]
            amount = message.split()[3]
            rates = Rates.query.filter_by(currency_a=currency_a).filter_by(currency_b=currency_b).filter_by(action='SELL').order_by(desc('rate')).all()
            if not rates:
                return "Sorry No Entries Exist for this query"
            rate = rates[0]      
            req = str(rate.currency_a) + " : " + str(rate.currency_b) + " " +"Rate :{}".format(rate.rate) + " " + "Successful!"

            try:
                request_obj = Requests(currency_a=rate.currency_a, currency_b=rate.currency_b, amount=amount, date=datetime.today(), action='SELL', rating=2)
                request_obj.save_to_db()
                return f"Selling {req}" 
            except Exception as e:
                raise e
                return f"Error Creating Request{req}"        
        else:
            response_message = "Please Enter Either (1) To Select Sale or (2) To Select Buy "

    return response_message
    # if client.position == 1 :
    #     ask the user for the address 
    #     update the user position to position 2 
    #     response_message = ''
    # elif position == 2 :
    #     save the address which is coming with the message 
    #     update the position of the user to position 3 
    #     ask the user for their destination bank 
    # elif positon 3 
    #     save the destination bank 
    #     update positon = 4 
    #     request for the account nmber 
    # elif positon 4 
    #     update stage = menu 
    #     set position = 0 
    #     congratulate the user for succesful registration 
    # else:
    #     pass

def menu_options_handler(client, message):
    if message == "1":
        return "\nInitiating Your Option To Buy\n Your Acocount {0} to {1}".format(client.account_no, client.destination_bank)
        # initiate purchase here
    if message == "2":
        "\nYou Have Selected The Option To Buy\n Your Account {0} to {1}".format(client.account_no, client.destination_bank)
        # initiate sale here

