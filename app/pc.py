import copy
from flask import Blueprint, jsonify, request
import json

pc_bp = Blueprint('pc', __name__)

# List of PCs added to the configuration.
pcs = []

# PC configuration to be added from the API.
pc_config = {
  "pc-config": {
    "hostname": "",
    "ipv4": {
      "address": "0.0.0.0",
      "netmask": "0.0.0.0",
      "gateway": "0.0.0.0"
    },
    "vlan": ""
  }
}

# Scheme for the PC body to be added from the API.
pc_scheme = {
    "hostname": ""
}

# Scheme for the IPv4 body to be added from the API.
ipv4_scheme = {
    "address": "",
    "netmask": "",
    "gateway": ""
}

# VLANs configuration
pc_vlans = {
    "PC0": {
        "address": "192.168.0.2",
        "netmask": "255.255.255.0",
        "gateway": "192.168.0.1",
        "vlan": "VLAN Ingenieria"
    },
    "PC3": {
        "address": "192.168.0.3",
        "netmask": "255.255.255.0",
        "gateway": "192.168.0.1",
        "vlan": "VLAN Ingenieria"
    },
    "PC1": {
        "address": "192.168.1.2",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "vlan": "VLAN Mercadeo"
    },
    "PC4": {
        "address": "192.168.1.3",
        "netmask": "255.255.255.0",
        "gateway": "192.168.1.1",
        "vlan": "VLAN Mercadeo"
    },
    "PC2": {
        "address": "192.168.2.2",
        "netmask": "255.255.255.0",
        "gateway": "192.168.2.1",
        "vlan": "VLAN Legal"
    },
    "PC5": {
        "address": "192.168.2.3",
        "netmask": "255.255.255.0",
        "gateway": "192.168.2.1",
        "vlan": "VLAN Legal"
    }
}

"""
Add a PC to the configuration. The hostname is passed as a parameter in the URL. 
The function checks if the PC already exists in the configuration. 
If it does, it returns a message saying that the PC already exists. 
If it doesn't, it adds the PC to the configuration and returns the PC configuration with a status code of 201.
"""
@pc_bp.route('/add/<hostname>', methods=['POST'])
def add_pc(hostname):

    for pc in pcs:
        if pc['pc-config']['hostname'] == hostname:
            return jsonify({'message': 'PC already exists'}), 400

    if hostname not in pc_vlans:
        return jsonify({'message': 'Invalid PC hostname'}), 400

    new_pc = copy.deepcopy(pc_config)  # Crea una copia profunda de pc_config
    new_pc['pc-config']['hostname'] = hostname
    new_pc['pc-config']['ipv4']['address'] = pc_vlans[hostname]['address']
    new_pc['pc-config']['ipv4']['netmask'] = pc_vlans[hostname]['netmask']
    new_pc['pc-config']['ipv4']['gateway'] = pc_vlans[hostname]['gateway']
    new_pc['pc-config']['vlan'] = pc_vlans[hostname]['vlan']
    pcs.append(new_pc)


    return jsonify(new_pc), 201

"""
Return all PCs in the configuration.
"""
@pc_bp.route('/get', methods=['GET'])
def get_pcs():
    return jsonify(pcs)

"""
Modify the IPv4 address of a PC. The hostname is passed as a parameter in the URL.
"""
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
