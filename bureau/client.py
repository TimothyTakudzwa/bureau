
from flask import Flask, render_template, request, flash
from functools import wraps
from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ClientForm
from .models import *
from . import app,db


@app.route('/client_register', methods=['GET', 'POST'])
def client_cegister():
    form = ClientForm(request.form)
    if request.method == 'POST' and form.validate():
      client = Client ( name = form.name.data,
                        address = form.address.data,
                        account_no = form.account_no.data,
                        )
      client.save_to_db()
      flash('Registration Process Complete')
    return render_template('client_register.html', form = form)

