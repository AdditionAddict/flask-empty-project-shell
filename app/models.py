from app import db
from sqlalchemy import Column
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'products'

    product_id = Column(db.Integer(), primary_key = True)
    name = Column(db.String(30))
    category = Column(db.String(50))
    description = Column(db.String(200))
    price = Column(db.Numeric(12, 2))

    # relationships
    products = relationship("OrderLine", back_populates="product")

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = Column(db.Integer(), primary_key = True)
    name = Column(db.String(30))
    address = Column(db.String(100))
    city = Column(db.String(50))
    state = Column(db.String(20))
    zip = Column(db.String(7))
    country = Column(db.String(20))

    # relationships
    products_sold = relationship("OrderLine", back_populates="order")

class OrderLine(db.Model):
    __tablename__ = 'order_lines'

    order_line_id = Column(db.Integer(), primary_key = True)
    order_id = Column(db.Integer(), db.ForeignKey('orders.order_id'))
    product_id = Column(db.Integer(), db.ForeignKey('products.product_id'))
    quantity = Column(db.Integer())

    # relationships
    product = relationship("Product", back_populates="products")
    order = relationship("Order", back_populates="products_sold")


# User model
#

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = Column(db.Integer(), primary_key = True)
    username = Column(db.String(50))
    email = Column(db.String(50))
    password_hash = Column(db.String(128))
    confirmed = Column(db.Boolean, default=False)

    @property
    def password(self):
        """Prevent reading of password setter"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        """Generate signed token that encodes user_id"""
        s = Serializer(current_app.config['SECRET_KEY'],
            expires_in=expiration)
        return s.dumps({'id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        print(data)
        return User.query.get(data['id'])
