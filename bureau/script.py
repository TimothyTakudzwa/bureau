# from bureau import app
from bureau.models import *
import datetime
from datetime import timedelta
import calendar

def simple_query():
    end_date = datetime.datetime.now().strftime("%d %m %Y")
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = datetime.datetime.today() - timedelta(days=6)
    i = 0 
    date = start_date
    rates =  Rates.query.filter(Rates.date.between(start_date, end)).filter(Rates.currency_a=='USD').filter(Rates.currency_b=='ZWL').filter(Rates.action=='BUY').all()
    rates_distinct =  Rates.query.filter(Rates.date.between(start_date, end)).filter(Rates.currency_a=='USD').filter(Rates.currency_b=='ZWL').distinct(Rates.bureau_id).filter(Rates.action=='BUY').all()
    data = {}
    while i < 7:
        new_date = findDay(str(date.strftime("%d %m %Y"))) 
                
        data[new_date] = {}
        for rate_dis in rates_distinct:
            highest = 0            
            for rate in rates:
                if rate.bureau_id == rate_dis.bureau_id:                    
                    if rate.rate > highest and rate.date.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
                        highest = rate.rate            
            bureau = Bureau.query.filter_by(id=rate_dis.bureau_id).first()          
            data[new_date][bureau.name] = highest
            highest = 0        
        date = date + timedelta(days=1)
        i += 1
    print(data)
    
    
    return ''

def findDay(date): 
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return (calendar.day_name[born]) 

print(simple_query())

def bureau_query(bureau_id, currency_a, currency_b):
    bureau = Bureau.get_by_id(bureau_id)
    rates = Rates.query.filter_by(bureau_id=bureau_id).filter_by(currency_a=currency_a).filter_by(currency_b=currency_b)
    end_date = datetime.datetime.now().strftime("%d %m %Y")
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = datetime.datetime.today() - timedelta(days=6)
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

    return ''

    






