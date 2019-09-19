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
 
class BureauLogin(Form):
   username = TextField('Username')
   password = PasswordField('password')
   submit = SubmitField('Submit')

class BureauForm(Form):
   name = StringField('Company Name')
   address = TextAreaField('Address')
   email = StringField('Email', [
        Length(min=4, message=(u'Little short for an email address?')),
        Email(message=('That\'s not a valid email address.')),
        DataRequired(message=('That\'s not a valid email address.'))
    ])
   longitude = StringField('longitude')
   latitude = StringField('latitude')
   account_no = IntegerField('Account Number')
   destination_bank = SelectField('Destination Bank',choices=[('cbz','CBZ'), ('zb','ZB'), ('nmb','NMB'), ('fbc','FBC'), ('stnbk','StanBic'), ('abs','ABS')])
   username = StringField('Username')
   password_hash = PasswordField('Password')
   submit = SubmitField('submit')

   def validate_email(self, email):
        """Email validation."""
        bureau = Bureau.query.filter_by(email=email.data).first()
        if bureau is not None:
            raise ValidationError('Please use a different email address.')


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
  
   






   