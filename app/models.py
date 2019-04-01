from app import db
from sqlalchemy import Column

class Product(db.Model):
    __tablename__ = 'products'

    product_id = Column(db.Integer(), primary_key = True)
    name = Column(db.String(30))
    category = Column(db.String(50))
    description = Column(db.String(200))
    price = Column(db.Numeric(12, 2))

    def to_json(self):
        json_product = {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'price': float(self.price) # Decimal to float
        }
        return json_product

    @staticmethod
    def from_json(json_product):
        name = json_product.get('name')
        category = json_product.get('category')
        description = json_product.get('description')
        price = json_product.get('price')
        return Product(name=name, category=category,
            description=description, price=price)

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = Column(db.Integer(), primary_key = True)
    name = Column(db.String(30))
    address = Column(db.String(100))
    city = Column(db.String(50))
    state = Column(db.String(20))
    zip = Column(db.String(7))
    country = Column(db.String(20))

    def to_json(self):
        json_order = {
            'order_id': self.order_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'country': self.country
        }
        return json_order

class OrderLine(db.Model):
    __tablename__ = 'order_lines'

    order_line_id = Column(db.Integer(), primary_key = True)
    order_id = Column(db.Integer())
    product_id = Column(db.Integer())
    quantity = Column(db.Integer())
