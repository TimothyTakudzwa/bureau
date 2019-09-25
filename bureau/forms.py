
from flask_wtf import Form  
from wtforms import TextField, IntegerField, IntegerField, TextAreaField, SubmitField, FloatField, RadioField, SelectField, PasswordField, StringField 
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms import validators
from .models import *

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
 
class LoginForm(Form):
   username = TextField('Username')
   password = PasswordField('password')
   submit = SubmitField('Submit')

class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Email', validators=[DataRequired()])   


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
   mylist = []   
   for item in bureaus: 
      mylist.append((item.id, item.name))         
   name= SelectField('Bureau Name', choices=mylist)
   currency_a= SelectField('Currency1', choices=[('USD', 'USD'), ('ZWL', 'ZWL')])
   currency_b =  SelectField('Currency2', choices=[('ZWL', 'ZWL'), ('USD', 'USD')])
   rate =  StringField('Rate')
   submit = SubmitField('Submit')


class OfferForm(Form):
   request_id = StringField('Request_id')
   offer_amount = StringField('Offer Amount')
   rate = IntegerField('Rate')
   submit = SubmitField('Submit') 



