from flask import Blueprint, jsonify, request

items_bp = Blueprint('items', __name__)

# Sample data
data = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'}
]

@items_bp.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

@items_bp.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@items_bp.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    data.append(new_item)
    return jsonify(new_item), 201

@items_bp.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        updates = request.get_json()
        item.update(updates)
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@items_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'})
