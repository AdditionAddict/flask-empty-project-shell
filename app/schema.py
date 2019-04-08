from marshmallow import fields, post_load
from marshmallow_sqlalchemy import ModelSchema

from app import db
from .models import Order, Product, OrderLine

class OrderSchema(ModelSchema):
    products_sold = fields.Nested('OrderLineSchema', many=True)
    class Meta(ModelSchema.Meta):
        model = Order
        sqla_session = db.session

    @post_load
    def make_order(self, data):
        if type(data) == Order:
            return data
        return Order(**data)

class ProductSchema(ModelSchema):
    price = fields.Float(data_key='price') # Decimal to float
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session

    @post_load
    def make_product(self, data):
        if type(data) == Product:
            return data
        return Product(**data)

class OrderLineSchema(ModelSchema):
    product = fields.Nested('ProductSchema', exclude=('products',))
    class Meta(ModelSchema.Meta):
        model = OrderLine
        sqla_session = db.session

    @post_load
    def make_order_line(self, data):
        db.session.flush()
        if type(data) == OrderLine:
            return data
        return OrderLine(**data)
