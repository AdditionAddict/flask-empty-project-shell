from . import api
from ..models import Order
from .. import db
from flask import jsonify

@api.route('/orders/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify({
      'orders': [o.to_json() for o in orders]
    })

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
