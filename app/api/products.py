from . import api
from ..models import Product
from .. import db
from flask import jsonify, request
from .authentication import auth
from flask_cors import cross_origin


@api.route('/products/', methods=['GET'])
@cross_origin()
def get_products():
    print('get_products')
    products = Product.query.all()
    return jsonify([p.to_json() for p in products]), 200

@api.route('/products/', methods=['POST'])
@cross_origin(allow_headers=['Content-Type', 'Authorization'], supports_credentials=True)
@auth.login_required
def new_product():
    product = Product.from_json(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201

@api.route('/products/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"success": True}), 200

@api.route('/products/<int:id>', methods=['PUT'])
@auth.login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    product.name = request.json.get('name')
    product.category = request.json.get('category')
    product.description = request.json.get('description')
    product.price = request.json.get('price')

    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 200
