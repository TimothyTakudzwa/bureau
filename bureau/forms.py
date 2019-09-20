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
   password_hash = PasswordField('password')
   submit = SubmitField('Submit')

   def __init__(self, *args, **kwargs):
        super(BureauLogin, self).__init__(*args, **kwargs)

   def validate(self):
        initial_validation = super(BureauLogin, self).validate()
        if not initial_validation:
            return False
        bureau = Bureau.query.filter_by(username=self.username.data).first()
        if not bureau:
            self.username.errors.append('Unknown username')
            return False
        if not bureau.verify_password(self.password_hash.data):
            self.password_hash.errors.append('Invalid password')
            return False
        return True

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
   account_no = IntegerField('Account Number', [validators.Required("please enter a numeric account number")])
   destination_bank = SelectField('Destination Bank',choices=[('cbz','CBZ'), ('zb','ZB'), ('nmb','NMB'), ('fbc','FBC'), ('stnbk','StanBic'), ('abs','ABS')])
   username = StringField('Username')
   password_hash = PasswordField('Password')

   password_hash = PasswordField('Password',[validators.Length(min=2), EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat password')
   submit = SubmitField('submit')

   def validate_email(self, email):
        """Email validation."""
        bureau = Bureau.query.filter_by(email=email.data).first()
        if bureau is not None:
            raise ValidationError('Email already in use, please use a different email address.')

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


   