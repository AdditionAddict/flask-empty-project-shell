from . import api
from ..models import Order, OrderLine, Product
from .. import db
from flask import jsonify, request
from .authentication import auth
from ..services import OrderListService

from ..schema import OrderSchema, OrderLineSchema

@api.route('/orders/', methods=['GET'])
def get_orders():
    service = OrderListService({}, db.session)

    print(OrderLineSchema._declared_fields)
    return jsonify(service.get())

@api.route('/orders/', methods=['POST'])
def new_order():
    order = Order.from_json(request.json)
    db.session.add(order)
    db.session.flush()
    order_id = order.order_id
    for line in request.json.get('lines'):
        order_line = OrderLine.add_line(order_id, line)
        db.session.add(order_line)
    db.session.commit()
    return jsonify(order.to_json()), 201

@api.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"success": True})

@api.route('/orders/<int:id>', methods=['PUT'])
def edit_order(id):
    order = Order.query.get_or_404(id)

    order.order_id = request.json.get('order_id')
    order.name = request.json.get('name')
    order.address = request.json.get('address')
    order.city = request.json.get('city')
    order.state = request.json.get('state')
    order.zip = request.json.get('zip')
    order.country = request.json.get('country')

    db.session.add(order)
    db.session.commit()
