
from flask import Flask, render_template, request, flash, url_for, redirect
from .models import *
from . import app,db
import ast
import json
from collections import defaultdict
# import datetime
from datetime import timedelta
import calendar
from .forms import *

@app.route('/statistics', methods=['GET', 'POST'])
def simple_query():
    form = BureauSelectForm()
    if request.method == 'GET':
        currency_a = 'USD'
        currency_b = 'ZWL'
        mode = 'BUY'
    else:
        currency_a = form.currency_a.data
        currency_b = form.currency_b.data
        mode = 'BUY'
    end_date = datetime.now().strftime("%d %m %Y")
    end = datetime.now().strftime("%Y-%m-%d")
    start_date = datetime.today() - timedelta(days=6)
    i = 0 
    date = start_date
    print(start_date)
    rates =  Rates.query.filter(Rates.date.between((start_date- timedelta(days=1)), end)).filter(Rates.currency_a==currency_a).filter(Rates.currency_b==currency_b).filter(Rates.action==mode).all()
    rates_distinct =  Rates.query.filter(Rates.date.between(start_date, end)).filter(Rates.currency_a==currency_a).filter(Rates.currency_b==currency_b).distinct(Rates.bureau_id).filter(Rates.action==mode).all()
    data = defaultdict(list)
    print(rates)
    days = []     
    for rate_dis in rates_distinct:
        current_bureau_list = []
        highest = 0      
        current_bureau_rates = []
        print(rates)
        for x in rates:
            if x.bureau_id == rate_dis.bureau_id:
                current_bureau_rates.append(x)
        print(current_bureau_rates, rate_dis.bureau_id)
        while i < 7:             
            current_day_rates = [] 
            highest = 0 
            for rate in current_bureau_rates:                
                if rate.date.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
                    current_day_rates.append(rate)
                else:
                    pass
            print(current_day_rates)
            for day in current_day_rates:
                if day.rate > highest:
                    highest = day.rate
                else:
                    highest = 0
            current_bureau_list.append(highest)
            date = date + timedelta(days=1)
            i += 1  
    
        date = start_date
        bureau = Bureau.query.filter_by(id=rate_dis.bureau_id).first()
        highest = 0 
        i = 0
        print(type(current_bureau_list))
        data[bureau.name] = current_bureau_list  
    while i < 7:
        new_date = findDay(str(date.strftime("%d %m %Y"))) 
        days.append(new_date)
        data["days"] = days
        date = date + timedelta(days=1)
        i = i+1
    print(dict(data))
    return render_template('statistics.html',form=form, data=json.dumps(dict(data)))       
    
def findDay(date): 
        born = datetime.strptime(date, '%d %m %Y').weekday() 
        return (calendar.day_name[born])

@app.route('/bureau_stats/<bureau_id>/<currency_a>/<currency_b>', methods=['GET'])
def bureau_query(bureau_id, currency_a, currency_b):
    if request.method == 'GET':
        bureau = Bureau.get_by_id(bureau_id)
        rates = Rates.query.filter_by(bureau_id=bureau_id).filter_by(currency_a=currency_a).filter_by(currency_b=currency_b)
        end_date = datetime.now().strftime("%d %m %Y")
        end = datetime.now().strftime("%Y-%m-%d")
        start_date = datetime.today() - timedelta(days=6)
        i = 0
        date = start_date
        data = {}

        while i < 7:
            new_date = findDay(str(date.strftime("%d %m %Y"))) 
                    
            data[new_date] = {}
            highest = 0
            for rate in rates:
                if rate.rate > highest and rate.date.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
                    highest = rate.rate
            data[new_date][bureau.name] = highest
            highest = 0
            date = date + timedelta(days=1)
            i += 1
        print(data)
        return render_template('dashboard/stats_by_bureau.html', data=json.dumps(dict(data)))
    else:
        form = BureaSelectForm()
        bureau_name = form.bureau_name.data
        currency_a = form.currency_a.data
        currency_b = form.currency_b.data
        return redirect(url_for('bureau', bureau_name=bureau_name, currency_a=currency_b, currency_b=currency_b))
        

@app.route('/transactions', methods=['GET'])
def transactions():
    transactions = Transaction.query.all()
    return render_template('dashboard/my_transactions.html', transactions=transactions)

