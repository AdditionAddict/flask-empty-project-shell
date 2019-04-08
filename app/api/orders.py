from marshmallow import ValidationError
from . import api
from ..models import Order, OrderLine, Product
from .. import db
from flask import jsonify, request
from .authentication import auth
from ..services import OrderListService

from ..schema import OrderSchema, OrderLineSchema

@api.route('/orders/', methods=['GET'])
def get_orders():
    service = OrderListService()
    return jsonify(service.get())

@api.route('/orders/', methods=['POST'])
def new_order():
    schema = OrderSchema()
    try:
        order = schema.load(request.get_json())
    except ValidationError as err:
        print('Validation Error: ', err.messages)
    db.session.add(order.data)
    db.session.commit()
    return jsonify(schema.dump(order)), 201

@api.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"success": True})

@api.route('/orders/<int:id>', methods=['PUT'])
def edit_order(id):
    # get order
    order = Order.query.get_or_404(id)
    # update order and commit
    schema = OrderSchema()
    schema.load(request.get_json(), instance=order)
    db.session.commit()
    return jsonify(schema.dump(order))
