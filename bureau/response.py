from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db

@app.route('/response', methods=['GET', 'POST'])
def response():
    form = ResponseForm()
    phone_number = '2637774231343'
    response_message = "Hello"
    if request.method == 'POST':
        client = Client.get_by_phone_number(phone_number)
        if client is None: 
            client = Client(stage='initial', position=1, phone_number=phone_number)
            client.save_to_db()
            response_message = 'Hie this is our first time talking. Before we proceed might i know your name'
        
    return render_template('response.html', form = form, response=response_message)