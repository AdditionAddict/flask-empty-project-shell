from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from .models import Order, Product, OrderLine

class OrderSchema(ModelSchema):
    products_sold = fields.Nested('OrderLineSchema', many=True)
    class Meta:
        model = Order

class ProductSchema(ModelSchema):
    price = fields.Float(data_key='price') # Decimal to float
    class Meta:
        model = Product


class OrderLineSchema(ModelSchema):
    product = fields.Nested('ProductSchema', exclude=('products',))
    class Meta:
        model = OrderLine
        fields = ('product', 'quantity')
