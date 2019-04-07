from sqlalchemy.orm import joinedload, selectinload

from .models import Order, Product, OrderLine
from .schema import OrderSchema, ProductSchema, OrderLineSchema

class OrderListService:
    '''
    This service intended for use exclusively by /api/orders
    '''
    def __init__(self, params, _session=None):
        # your unit tests can pass in _session=MagicMock()
        print('__init__')
        self.session = _session or db.session
        self.params = params

    def _parents(self):
        return ( self.session.query(Order)
            .options(selectinload(Order.products_sold))
            .all() )

    def get(self):
        schema = OrderSchema()
        return schema.dump(self._parents(), many=True).data
