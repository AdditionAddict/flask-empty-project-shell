from sqlalchemy.orm import joinedload, selectinload

from .models import Order, Product, OrderLine
from .schema import OrderSchema, ProductSchema, OrderLineSchema

from app import db

class OrderListService:
    '''
    This service intended for use exclusively by /api/orders
    '''
    def __init__(self, _session=None):
        # your unit tests can pass in _session=MagicMock()
        self.session = _session or db.session

    def _parents(self):
        return ( self.session.query(Order)
            .options(selectinload(Order.products_sold))
            .all() )

    def get(self):
        # [{"address": "59 Arcubus Avenue", "city": "Sheffield",
        # "country": "United Kingdom", "name": "Andrew", "order_id": 17,
        # "products_sold": [{ "product": { "category": "Technology",
        # "description": "A small computer", "name": "Calculator",
        #  "price": 15.35, "product_id": 1 }, "quantity": 10 }, ...]}]
        schema = OrderSchema()
        return schema.dump(self._parents(), many=True).data
