from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db

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
            rqs = ''
            reqs = Requests.query.filter_by(action='BUY').all()
            for req in reqs:
                rqs += str(req.id)+ ") " + str(req.currency_a) + " : " + str(req.currency_b) + " ," + str(req.amount) + " **** "
            response_message = "You Have Selected Buy Option. Please Select By Typing 'buy' Followed By The Number" + " \n" + rqs
            menu_options_handler(client, message)
        elif message.startswith("buy"):
            reqs = Requests.query.filter_by(action='BUY').all()
            req = Requests.query.filter_by(id=message.split()[-1]).filter_by(action="BUY").first()
            if req == None:
                return "The Entry You Tried To Buy Does not Exist, Try Again Using A Different Number"
            req = str(req.currency_a) + " : " + str(req.currency_b) + " " +"Amount :{}".format(req.amount) + " " + "Successful!"
            return f"Buying {req}"    
        elif message == "2":
            rqs = ''
            reqs = Requests.query.filter_by(action='SELL').all()
            for req in reqs:
                rqs += str(req.id)+ ") " + str(req.currency_a) + " : " + str(req.currency_b) + " ," + str(req.amount) + " **** "
            response_message = "You Have Selected Sell Option. Please Select By Typing sell Followed By The Number" + " \n" + rqs
            menu_options_handler(client, message)
        elif message.startswith("sell"):
            reqs = Requests.query.filter_by(action='SELL').all()
            req = Requests.query.filter_by(id=message.split()[-1]).filter_by(action="SELL").first()
            if req == None:
                return "The Entry You Tried To Sell Does not Exist, Try Again Using A Different Number"
            req = str(req.currency_a) + " : " + str(req.currency_b) + " " +"Amount :{}".format(req.amount) + " " + "Successful!"
            return f"Selling {req}"      
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

