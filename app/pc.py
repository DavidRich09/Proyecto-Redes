from flask import Blueprint, jsonify, request
import json

pc_bp = Blueprint('pc', __name__)

pcs = []

pc_config = {
  "pc-config": {
    "hostname": "",
    "ipv4": {
      "address": "0.0.0.0",
      "netmask": "0.0.0.0",
      "gateway": "0.0.0.0"
    }
  }
}

pc_scheme = {
    "hostname": ""
}

ipv4_scheme = {
    "address": "",
    "netmask": "",
    "gateway": ""
}

@pc_bp.route('/add/<hostname>', methods=['POST'])
def add_pc(hostname):

    for pc in pcs:
        if pc['pc-config']['hostname'] == hostname:
            return jsonify({'message': 'PC already exists'}), 400

    new_pc = pc_config
    new_pc['pc-config']['hostname'] = hostname
    pcs.append(new_pc)

    return jsonify(new_pc), 201

@pc_bp.route('/get', methods=['GET'])
def get_pcs():
    return jsonify(pcs)

@pc_bp.route('/change/ipv4/<hostname>', methods=['POST'])
def change_ipv4(hostname):
    temp_ipv4 = request.get_json()
    if not temp_ipv4:
        return jsonify({'error': 'Invalid input'}), 400

    for pc in pcs:
        if pc['pc-config']['hostname'] == hostname:
            pc['pc-config']['ipv4']['address'] = temp_ipv4['address']
            pc['pc-config']['ipv4']['netmask'] = temp_ipv4['netmask']
            pc['pc-config']['ipv4']['gateway'] = temp_ipv4['gateway']
            return jsonify(pc)

    return jsonify({'error': 'PC not found'}), 404
