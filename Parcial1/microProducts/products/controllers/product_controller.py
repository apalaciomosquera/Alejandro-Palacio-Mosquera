from flask import Blueprint, request, jsonify
from products.models.product_model import Products
from db.db import db

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/products', methods=['GET'])
def get_products():
    print("listado de productos")
    products = Products.query.all()
    result = [{'id': product.id, 'name': product.name, 'price': str(product.price), 'quantity': product.quantity} for product in products]
    return jsonify(result)

# Get single product by id
@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    print("obteniendo producto")
    product = Products.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'price': str(product.price), 'quantity': product.quantity})

@product_controller.route('/api/products', methods=['POST'])
def create_product():
    print("creando producto")
    data = request.json
    new_product = Products(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# Update an existing product
@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    print("actualizando producto")
    product = Products.query.get_or_404(product_id)
    data = request.json
    product.name = data['name']
    product.price = data['price']
    product.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@product_controller.route('/api/products/update_quantity', methods=['PUT'])
def update_product_quantity():
    print("actualizando cantidades de productos")
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Se espera una lista de productos para actualizar'}), 400

    for product_update in data:
        product_id = product_update.get('id')
        new_quantity = product_update.get('quantity')

        if product_id is None or new_quantity is None:
            return jsonify({'message': 'Cada producto debe tener un id y una cantidad'}), 400

        product = Products.query.get_or_404(product_id)
        product.quantity = new_quantity
        db.session.commit()

    return jsonify({'message': 'Cantidades de productos actualizadas exitosamente'}), 200

# Delete an existing product
@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    print("eliminando producto")
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
