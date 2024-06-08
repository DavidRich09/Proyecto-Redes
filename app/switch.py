from flask import Blueprint, jsonify, request
import json

switch_bp = Blueprint('switch', __name__)

switches = []

switch_config = {
    "switch-config": {
        "hostname": "example-switch",
        "vlan": [],
        "interface": [
            {
                "name": "FastEthernet0/0/0",
                "description": "Main Ethernet interface",
                "enabled": "true"
            },
            {
                "name": "FastEthernet0/0/1",
                "description": "Secondary Ethernet interface",
                "enabled": "true"
            },
            {
                "name": "FastEthernet0/0/2",
                "description": "Third Ethernet interface",
                "enabled": "true"
            },
            {
                "name": "FastEthernet0/0/3",
                "description": "Fourth Ethernet interface",
                "enabled": "true"
            },
            {
                "name": "FastEthernet0/0/4",
                "description": "Fifth Ethernet interface",
                "enabled": "true"
            }
        ]
    }
}

switch_scheme = {
    "hostname": "",
}

interface_scheme = {
    "name": "",
    "description": "",
    "enabled": ""
}

vlan_scheme = {
    "vlan_id": "",
    "name": ""
}

@switch_bp.route('/add/<hostname>', methods=['POST'])
def add_switch(hostname):

    for switch in switches:
        if switch['switch-config']['hostname'] == hostname:
            return jsonify({'Error': 'Switch already exists'}), 400

    new_switch = switch_config
    new_switch['switch-config']['hostname'] = hostname
    switches.append(new_switch)
    return jsonify({'Success':'Switch added to configuration'}), 201

@switch_bp.route('/get', methods=['GET'])
def get_switches():
    return jsonify(switches)

@switch_bp.route('/add/vlan/<hostname>', methods=['POST'])
def add_vlan(hostname):
    temp_vlan = request.get_json()
    if not temp_vlan:
        return jsonify({'error': 'Invalid input'}), 400

    for switch in switches:
        if switch['switch-config']['hostname'] == hostname:
            if temp_vlan not in switch['switch-config']['vlan']:
                switch['switch-config']['vlan'].append(temp_vlan)
                return jsonify({'Success':'VLAN added to configuration'}), 201
            else:
                return jsonify({'Error': 'VLAN already exists'}), 400

    return jsonify({'Error': 'Switch not found'}), 404

@switch_bp.route('/change/interface/<hostname>/<interface>', methods=['POST'])
def change_interface(hostname, interface):
    temp_interface = request.get_json()
    if not temp_interface:
        return jsonify({'error': 'Invalid input'}), 400

    for switch in switches:
        if switch['switch-config']['hostname'] == hostname:
            for intf in switch['switch-config']['interface']:
                if intf['name'] == interface:
                    intf.update(temp_interface)
                    return jsonify({'Success':'Interface updated'}), 201

    return jsonify({'Error': 'Switch or interface not found'}), 404