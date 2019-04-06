from . import api
from ..models import Order, OrderLine, Product
from .. import db
from flask import jsonify, request
from .authentication import auth

import sqlalchemy
from sqlalchemy.sql import func, literal_column, select

# Helper function:
# Pulls Postgres SQL function json_agg
# See - https://trvrm.github.io/using-sqlalchemy-and-postgres-functions-to-produce-json-tree-structures-from-sql-joins.html
def json_agg(table):
    return func.json_agg(literal_column('"'+table.name+'"'))

def order_details(db):

    OrderProducts = (
        db.session.query(
            func.json_agg(func.json_build_object(
                'name', Product.name,
                'category', Product.category,
                'quantity', OrderLine.quantity
            ).label('products')),
                Order.order_id)
        .group_by(Order.order_id)
    ).cte('order_products')

    query = (
        db.session.query(
            func.json_build_object(
                'order_id', Order.order_id,
                'name', Order.name,
                'address', Order.address,
                'city', Order.city,
                'state', Order.state,
                'zip', Order.zip,
                'country', Order.country,
                'quantity', OrderLine.quantity),
            OrderProducts)
        .join(OrderLine, OrderLine.order_id == Order.order_id)
        .join(OrderProducts)
    )
    # Common Table Expressions (CTEs)
    results = query.all()
    return results

@api.route('/orders/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    # TODO: add cart lines
    import pprint
    pprint.pprint(order_details(db))
    return jsonify([
        o.to_json()
        for o in orders])

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
