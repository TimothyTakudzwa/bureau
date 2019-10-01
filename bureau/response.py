from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db

@app.route('/response/<client_id>', methods=['GET', 'POST'])
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
        response_message = "Test response"
    return response_message

def initial_handler(message, client):
<<<<<<< HEAD
    return 'Test'
=======
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
        response_message = 'Thank you for registering with us. You can now proceed to transact!'
    else:
        pass
    return response_message
>>>>>>> 2b90f9e27ad18384479aa6105661bf747cc1257a
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

def menu_options(client, message):
    select_items = {1: }