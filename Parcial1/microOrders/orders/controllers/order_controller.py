import requests
from flask import Blueprint, request, jsonify, session
from orders.models.order_model import Orders
from db.db import db

order_controller = Blueprint('order_controller', __name__)

# Endpoint para obtener todas las órdenes
@order_controller.route('/api/orders', methods=['GET'])
def get_all_orders():
    orders = Orders.query.all()
    result = [
        {
            'id': order.id,
            'userName': order.userName,
            'userEmail': order.userEmail,
            'saleTotal': str(order.saleTotal),
            'date': order.date
        } for order in orders
    ]
    return jsonify(result)

# Endpoint para obtener una orden por ID
@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Orders.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'userName': order.userName,
        'userEmail': order.userEmail,
        'saleTotal': str(order.saleTotal),
        'date': order.date
    })

# Endpoint para crear una nueva orden
@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    
    user_name = data.get('username')
    user_email = data.get('email')

    
    if not user_name or not user_email:
        user_name = session.get('username')
        user_email = session.get('email')

    
    if not user_name or not user_email:
        return jsonify({'message': 'Información de usuario inválida'}), 400

    products = data.get('products')
    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400

    sale_total = 0
    product_updates = []

    for product in products:
        product_id = product.get('id')
        quantity = product.get('quantity')

        if not product_id or not quantity:
            return jsonify({'message': 'Información de producto inválida'}), 400

        
        product_response = requests.get(f'http://localhost:5003/api/products/{product_id}')

        if product_response.status_code != 200:
            return jsonify({'message': f'Producto {product_id} no encontrado'}), 400

        db_product = product_response.json()

        if db_product['quantity'] < quantity:
            return jsonify({'message': f'Producto {product_id} no disponible o cantidad insuficiente'}), 400

        sale_total += float(db_product['price']) * quantity  

    
        product_updates.append({'id': product_id, 'quantity': db_product['quantity'] - quantity})

    
    update_response = requests.put(
        'http://localhost:5003/api/products/update_quantity',
        json=product_updates
    )

    if update_response.status_code != 200:
        return jsonify({'message': 'Error al actualizar el inventario'}), 50
    db.session.commit()

    return jsonify({'message': 'Orden creada exitosamente'}), 201
