from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import app,db
#from . import login_manager
#from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Transaction(db.Model):
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer())
    bureau_id = db.Column(db.Integer())
    amount = db.Column(db.Float)    
    rate = db.Column(db.Float)
    total_amount = db.Column(db.Float)    
    transaction_type = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.now())
    reference_number = db.Column(db.String(30))
    transaction_code = db.Column(db.String(100))    
    completed = db.Column(db.Boolean, default=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_total_amount(self):
        return self.total_amount

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()  

'''
Model For Client 
'''
    
class Client(db.Model):
    __tablename__ = 'Clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    is_blocked = db.Column(db.Boolean)
    destination_bank = db.Column(db.String(50))
    account_no = db.Column(db.String(50))
    stage = db.Column(db.String(50))
    position = db.Column(db.Integer)
    is_required = db.Column(db.Boolean)

    # def block_unblock_toggle(self):
    #     if self.is_blocked:
    #         return self.is_blocked = False
    #     else:
    #         return self.is_blocked = True    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()   
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Bureau(UserMixin,db.Model):
    __tablename__ = 'Bureaus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    email = db.Column(db.String(100))    
    phone = db.Column(db.String(100))    
    # phone_number = db.Column(db.String(50))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    account_no = db.Column(db.String(100))
    destination_bank = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))
    is_blocked = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()   
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_bureau_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  

    def hash_password(self, password):
        return generate_password_hash(password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 


'''
Model for Exchange Rates
'''
class Rates(db.Model):
    __tablename__ = 'Rates'
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float)
    bureau_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.now().date())
    currency_a = db.Column(db.String(70))
    currency_b = db.Column(db.String(70))
    action = db.Column(db.String(70))

    def __str__(self):
        return 'Client',self.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    @staticmethod
    def get_buy_rate(rate):
    	return Rates.query.filter_by(rate=rate).first() 
    
    @staticmethod
    def get_db_currencies(currency_a, currency_b):
        return Rates.query.filter_by(currency_a=currency_a).filter_by(currency_b=currency_b).all()

'''
Model for Audit Trails
'''
class AuditTrail(db.Model):
    __tablename__ = 'AuditTrails'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    action = db.Column(db.String(100))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Requests(db.Model):
    __tablename___= 'Requests'
    id = db.Column(db.Integer, primary_key=True)
    currency_a = db.Column(db.String(70))
    currency_b = db.Column(db.String(70))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)
    action = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    

    @classmethod
    def get_by_id(self,id):
        return Requests.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

class Offer(db.Model):
    __tablename__='Offers'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    rate = db.Column(db.Float)


    @classmethod
    def get_by_id(self,id):
        return Offer.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Currencies(db.Model):
    __tablename__='Currencies'
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(3))
    currency_name = db.Column(db.String(100))

    @classmethod
    def get_by_id(self,id):
        return Currencies.query.filter_by(id=id).first()

 