# Module: routes.py
# Purpose: Defines API routes for the Order Management Service.
# Author: Architect Agent
# Created: 2024-03-02

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from .models import db, Order, OrderItem, get_inventory_collection
import uuid

order_bp = Blueprint('order_management', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    """
    Creates a new room service order.
    Expects JSON data with guest_id, items (list of item_id, quantity), and optional delivery_instructions.
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['guest_id', 'items']):
        return jsonify({'error': 'Missing required fields: guest_id, items'}), 400

    guest_id = data['guest_id']
    items_data = data['items']
    delivery_instructions = data.get('delivery_instructions')

    if not isinstance(items_data, list) or not items_data:
        return jsonify({'error': 'Items must be a non-empty list'}), 400

    inventory_collection = get_inventory_collection()
    if not inventory_collection:
        return jsonify({'error': 'Inventory service not available'}), 500

    order_items = []
    total_cost = 0
    for item_data in items_data:
        if not all(k in item_data for k in ['item_id', 'quantity']):
            return jsonify({'error': 'Each item must have item_id and quantity'}), 400
        
        item_id = item_data['item_id']
        quantity = item_data['quantity']

        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({'error': f'Quantity for item {item_id} must be a positive integer'}), 400

        # Check inventory
        inventory_item = inventory_collection.find_one({'item_id': item_id})
        if not inventory_item:
            return jsonify({'error': f'Item {item_id} not found in inventory'}), 404
        
        if inventory_item['stock_level'] < quantity:
            return jsonify({'error': f'Insufficient stock for item {item_id}. Available: {inventory_item['stock_level']}'}), 400
        
        item_price = inventory_item.get('price', 0.0)
        order_items.append(OrderItem(item_id=item_id, quantity=quantity, price=item_price))
        total_cost += item_price * quantity

        # Deduct from inventory (this should ideally be part of a distributed transaction)
        inventory_collection.update_one(
            {'item_id': item_id},
            {'$inc': {'stock_level': -quantity}}
        )

    order_id = str(uuid.uuid4())
    new_order = Order(
        order_id=order_id,
        guest_id=guest_id,
        delivery_instructions=delivery_instructions,
        status='Pending'
    )
    db.session.add(new_order)
    
    for item in order_items:
        item.order_id = order_id
        db.session.add(item)

    try:
        db.session.commit()
        return jsonify(new_order.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to create order due to data integrity issue.'}), 500
    except Exception as e:
        db.session.rollback()
        # Revert inventory changes if order creation fails
        for item_data in items_data:
            inventory_collection.update_one(
                {'item_id': item_data['item_id']},
                {'$inc': {'stock_level': item_data['quantity']}}
            )
        return jsonify({'error': str(e)}), 500

@order_bp.route('/orders', methods=['GET'])
def get_all_orders():
    """
    Retrieves a list of all room service orders.
    """\n    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200

@order_bp.route('/orders/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Retrieves details of a specific room service order.
    """
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.to_dict()), 200

@order_bp.route('/orders/<string:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Updates an existing room service order.
    Allows updating status, delivery_instructions, and items.
    """
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400

    # Update status
    if 'status' in data:
        order.status = data['status']
    
    # Update delivery instructions
    if 'delivery_instructions' in data:
        order.delivery_instructions = data['delivery_instructions']

    # Update items (this is a more complex operation, requiring inventory checks and potential reverts)
    if 'items' in data:
        new_items_data = data['items']
        if not isinstance(new_items_data, list):
            return jsonify({'error': 'Items must be a list'}), 400

        inventory_collection = get_inventory_collection()
        if not inventory_collection:
            return jsonify({'error': 'Inventory service not available'}), 500

        # Track changes for potential rollback
        old_items_map = {item.item_id: item for item in order.items}
        new_items_map = {item_data['item_id']: item_data for item_data in new_items_data}
        inventory_changes = [] # (item_id, quantity_change)

        # Process existing items and new items
        items_to_add = []
        items_to_update = []
        items_to_delete = []

        for old_item in order.items:
            if old_item.item_id in new_items_map:
                # Item exists in both, check for quantity change
                new_item_data = new_items_map[old_item.item_id]
                new_quantity = new_item_data['quantity']
                quantity_diff = new_quantity - old_item.quantity

                if quantity_diff != 0:
                    inventory_item = inventory_collection.find_one({'item_id': old_item.item_id})
                    if not inventory_item:
                        return jsonify({'error': f'Item {old_item.item_id} not found in inventory'}), 404
                    
                    if quantity_diff > 0 and inventory_item['stock_level'] < quantity_diff:
                        return jsonify({'error': f'Insufficient stock for item {old_item.item_id}. Need {quantity_diff}, Available: {inventory_item['stock_level']}'}), 400
                    
                    inventory_changes.append((old_item.item_id, -quantity_diff))
                    inventory_collection.update_one(
                        {'item_id': old_item.item_id},
                        {'$inc': {'stock_level': -quantity_diff}}
                    )
                    old_item.quantity = new_quantity
                    items_to_update.append(old_item)
            else:
                # Item removed from order
                inventory_changes.append((old_item.item_id, old_item.quantity))
                inventory_collection.update_one(
                    {'item_id': old_item.item_id},
                    {'$inc': {'stock_level': old_item.quantity}}
                )
                items_to_delete.append(old_item)
        
        for new_item_data in new_items_data:
            if new_item_data['item_id'] not in old_items_map:
                # New item added to order
                item_id = new_item_data['item_id']
                quantity = new_item_data['quantity']

                inventory_item = inventory_collection.find_one({'item_id': item_id})
                if not inventory_item:
                    # Revert previous inventory changes before returning error
                    for item_id_change, qty_change in inventory_changes:
                        inventory_collection.update_one(
                            {'item_id': item_id_change},
                            {'$inc': {'stock_level': -qty_change}}
                        )
                    return jsonify({'error': f'New item {item_id} not found in inventory'}), 404
                
                if inventory_item['stock_level'] < quantity:
                    # Revert previous inventory changes before returning error
                    for item_id_change, qty_change in inventory_changes:
                        inventory_collection.update_one(
                            {'item_id': item_id_change},
                            {'$inc': {'stock_level': -qty_change}}
                        )
                    return jsonify({'error': f'Insufficient stock for new item {item_id}. Available: {inventory_item['stock_level']}'}), 400
                
                inventory_changes.append((item_id, -quantity))
                inventory_collection.update_one(
                    {'item_id': item_id},
                    {'$inc': {'stock_level': -quantity}}
                )
                items_to_add.append(OrderItem(order_id=order_id, item_id=item_id, quantity=quantity, price=inventory_item.get('price', 0.0)))
        
        for item in items_to_delete:
            db.session.delete(item)
        for item in items_to_add:
            db.session.add(item)

    try:
        db.session.commit()
        return jsonify(order.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        # Rollback inventory changes
        for item_id_change, qty_change in inventory_changes:
            inventory_collection.update_one(
                {'item_id': item_id_change},
                {'$inc': {'stock_level': -qty_change}}
            )
        return jsonify({'error': str(e)}), 500

@order_bp.route('/orders/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Cancels a room service order and restores inventory.
    """\n    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    inventory_collection = get_inventory_collection()
    if not inventory_collection:
        return jsonify({'error': 'Inventory service not available'}), 500

    # Restore inventory for items in the cancelled order
    for item in order.items:
        inventory_collection.update_one(
            {'item_id': item.item_id},
            {'$inc': {'stock_level': item.quantity}}
        )
    
    db.session.delete(order)
    try:
        db.session.commit()
        return jsonify({'message': f'Order {order_id} cancelled and inventory restored'}), 200
    except Exception as e:
        db.session.rollback()
        # If DB commit fails, try to revert inventory restoration (best effort)
        for item in order.items:
            inventory_collection.update_one(
                {'item_id': item.item_id},
                {'$inc': {'stock_level': -item.quantity}}
            )
        return jsonify({'error': str(e)}), 500
