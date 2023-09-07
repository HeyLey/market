from sqlalchemy import Integer, String, DateTime, Boolean
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True)
    password = db.Column(String(50), unique=False)
    email = db.Column(String(50), unique=True)
    balance = db.Column(Integer)
    created_on = db.Column(DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.balance = 0
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return f"<{self.username}>"


class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(Integer, primary_key=True)
    _user_id = db.Column('user_id', Integer, nullable=False)
    about = db.Column(String(50), unique=False)
    pic = db.Column(String(50), unique=False)
    price = db.Column(Integer)
    is_in_stock = db.Column(Boolean)
    created_on = db.Column(DateTime)

    @hybrid_property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("Can't set user_id attribute in Item")

    def __init__(self, user_id, about, pic='0.png', price=0):
        self.user_id = user_id
        self.about = about
        self.pic = pic
        self.price = price
        self.is_in_stock = True
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return f"<{self.about}>"


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(Integer, primary_key=True)
    _user_id = db.Column('user_id', Integer, nullable=False)
    item_id = db.Column(Integer)
    price = db.Column(Integer)
    created_on = db.Column(DateTime)
    is_ret = db.Column(Boolean)
    returned_on = db.Column(DateTime)

    @hybrid_property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        raise AttributeError("Can't set user_id attribute in Order")

    def __init__(self, user_id, item_id, price):
        self.user_id = user_id
        self.item_id = item_id
        self.price = price
        self.created_on = datetime.datetime.now()
        self.is_ret = False

    def __repr__(self):
        return f"<Order # {self.order_id}>"


