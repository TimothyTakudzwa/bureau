
from flask_wtf import Form  
from wtforms import TextField, IntegerField, IntegerField, TextAreaField, SubmitField, FloatField, RadioField, SelectField, PasswordField, StringField, DateField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms import validators
from .models import *
from sqlalchemy import desc, asc

class ClientForm(Form):
   name = TextField("client Name ",[validators.Required("Please enter your name.")]) 
   address = TextAreaField('Address')
   email = TextField("Client Email",[validators.Required("Please enter your email.")])
   account_no = TextField('Account Number')
   submit = SubmitField('submit')

class BureauForm2(Form):
   username = TextField("Client Username", [validators.Required("please enter your username")])
   password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat Password')

class BureauSelectForm(Form):
   bureau_list = []
   bureaus = Bureau.query.all()
   for item in bureaus: 
      bureau_list.append((item.id, item.name))

   currencies = Currencies.query.order_by(Currencies.currency_code.asc()).all() 
   currency_list1 = []
   for item in currencies:
      currency_list1.append((item.id, item.currency_code))

   currencies = Currencies.query.order_by(Currencies.currency_code.desc()).all() 
   currency_list = []
   for item in currencies:
      currency_list.append((item.id, item.currency_code))

   bureau_name= SelectField('Bureau Name', choices=bureau_list)
   currency_a= SelectField('From', choices=currency_list)
   currency_b =  SelectField('To', choices=currency_list1)
   submit = SubmitField('Submit')

class LoginForm(Form):
   username = TextField('Username')
   password = PasswordField('Password')
   submit = SubmitField('Submit')

class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
   password = PasswordField('New Password',
                             validators=[DataRequired(message='Please enter a password.'),
                                         Length(min=8, message=('Please select a stronger password.')),
                                         EqualTo('confirm', message='Passwords must match')])  
   confirm = PasswordField('Repeat Password')
   submit = SubmitField('Submit')



class SignupForm(Form):
   name = StringField('Company Name',
                       validators=[DataRequired(message=('Enter a fake name or something.'))])
   address = TextAreaField('Address')
   email = StringField('Email', [
        Length(min=4, message=(u'Little short for an email address?')),
        Email(message=('That\'s not a valid email address.')),
        DataRequired(message=('That\'s not a valid email address.'))
    ])
   longitude = StringField('longitude')
   latitude = StringField('latitude')
   account_no = IntegerField('Account Number', [validators.Required("please enter a numeric account number")])
   destination_bank = SelectField('Destination Bank',choices=[('cbz','CBZ'), ('zb','ZB'), ('nmb','NMB'), ('fbc','FBC'), ('stnbk','StanBic'), ('abs','ABS')])
   username = StringField('Username')

   password_hash = PasswordField('Password',
                             validators=[DataRequired(message='Please enter a password.'),
                                         Length(min=8, message=('Please select a stronger password.')),
                                         EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat password')
   submit = SubmitField('Submit')

   def validate_username(self, username):
        """Username validation."""
        bureau = Bureau.query.filter_by(username=username.data).first()
        if bureau is not None:
            raise ValidationError('Username already in use, please use a different username.')


class RatesForm(Form):
   bureaus = Bureau.query.all()
   bureau_list = []   
   for item in bureaus: 
      bureau_list.append((item.id, item.name))

   currencies = Currencies.query.order_by(Currencies.currency_code.asc()).all() 
   currency_list1 = []
   for item in currencies:
      currency_list1.append((item.id, item.currency_code))

   currencies = Currencies.query.order_by(Currencies.currency_code.desc()).all() 
   currency_list = []
   for item in currencies:
      currency_list.append((item.id, item.currency_code))

   name= SelectField('Bureau Name', choices=bureau_list)
   currency_a= SelectField('From', choices=currency_list)
   currency_b =  SelectField('To', choices=currency_list1)
   action =  SelectField('Action', choices=[('BUY', 'BUY'), ('SELL', 'SELL')])
   rate =  StringField('Rate')
   bureau_id =  IntegerField('Bureau_id')
   submit = SubmitField('Submit')

class OfferForm(Form):
   request_id = HiddenField()
   offer_amount = StringField('Offer Amount')   
   rate = FloatField()
   submit = SubmitField('Submit')


class RatesToday(Form):
   currencies = Currencies.query.order_by(Currencies.currency_code.asc()).all() 
   currency_list1 = []
   for item in currencies:
      currency_list1.append((item.id, item.currency_code))

   currencies = Currencies.query.order_by(Currencies.currency_code.desc()).all() 
   currency_list = []
   for item in currencies:
      currency_list.append((item.id, item.currency_code))

   currency_a= SelectField('From', choices=currency_list)
   currency_b =  SelectField('To', choices=currency_list1)
   submit = SubmitField('')

class ResponseForm(Form):
   request = StringField('Request')
   response = TextAreaField('Response')
   submit = SubmitField('Submit')
