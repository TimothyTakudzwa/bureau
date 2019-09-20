from flask import Flask, render_template, request, flash, url_for, redirect
from .models import *
from . import app,db


@app.route('/transactions', methods=['GET'])
def transactions():
    transactions = Transaction.query.all()
    return render_template('dashboard/my_transactions.html', transactions=transactions)
