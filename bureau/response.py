from flask import Flask, render_template, request, flash, url_for, redirect
from .forms import ResponseForm
from .models import *
from . import app,db

@app.route('/response', methods=['GET', 'POST'])
def response():
    form = ResponseForm()
    return render_template('response.html', form = form) 