from flask import Blueprint, jsonify, request
import json

switch_bp = Blueprint('switch', __name__)

# List of switches added to the configuration.
switches = []

# Switch configuration to be added from the API.
switch_config = {
    "switch-config": {
        "hostname": "example-switch",
        "vlan_id": [],
        "interface": [
            {
                "name": "FastEthernet0/0/0",
                "description": "Main Ethernet interface",
                "enabled": "true",
                "connected_to": ""
            },
            
            {
                "name": "GigabitEthernet0/0/0",
                "description": "Main Ethernet interface",
                "enabled": "true",
                "connected_to": ""
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

# Scheme for the switch body to be added from the API.
switch_scheme = {
    "hostname": "",
}

# Scheme for the interface body to be added from the API.
interface_scheme = {
    "name": "",
    "description": "",
    "enabled": ""
}

# Scheme for the VLAN body to be added from the API.
vlan_scheme = {
    "vlan_id": "",
    "name": ""
}

switch_vlans = {
    "VLAN-Ingenieria": {
        "vlan_id": 10,
        "subnet": "192.168.0.0/24"
    },
    "VLAN-Mercadeo": {
        "vlan_id": 20,
        "subnet": "192.168.1.0/24"
    },
    "VLAN-Legal": {
        "vlan_id": 30,
        "subnet": "192.168.2.0/24"
    }
}

# Conexiones entre dispositivos
switch_connections = {
    "switch1": {
        "GigabitEthernet0/0/0": "router"
    },
    "switch2": {
        "GigabitEthernet0/0/0": "switch1"
    }    
    
}

"""
Add a switch to the configuration. The hostname is passed as a parameter in the URL.
"""
@switch_bp.route('/add/<hostname>', methods=['POST'])
def add_switch(hostname):

    for switch in switches:
        if switch['switch-config']['hostname'] == hostname:
            return jsonify({'Error': 'Switch already exists'}), 400

    new_switch = request.get_json()

    # Conectar el switch al router
    for device, connections in switch_connections.items():
        if device == hostname:
            for intf, connected_device in connections.items():
                for interface in new_switch['switch-config']['interface']:
                    if interface['name'] == intf:
                        interface['connected_to'] = connected_device

    switches.append(new_switch)
    return jsonify({'Success':'Switch added to configuration'}), 201

"""
Get all switches in the configuration.
"""
@switch_bp.route('/get', methods=['GET'])
def get_switches():
    return jsonify(switches)

"""
Add a VLAN to the configuration. The switch hostname is passed as a parameter in the URL.
"""
@switch_bp.route('/add/vlan/<hostname>', methods=['POST'])
def add_vlan(hostname):
    temp_vlan = request.get_json()
    if not temp_vlan:
        return jsonify({'error': 'Invalid input'}), 400

    for switch in switches:
        if switch['switch-config']['hostname'] == hostname:
            if temp_vlan not in switch['switch-config']['vlan_id']:
                switch['switch-config']['vlan_id'].append(temp_vlan)
                return jsonify({'Success':'VLAN added to configuration'}), 201
            else:
                return jsonify({'Error': 'VLAN already exists'}), 400

    return jsonify({'Error': 'Switch not found'}), 404

"""
Change switch interface configuration. The switch hostname and interface name are passed as parameters in the URL.
"""
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


@switch_bp.route('/assign/vlan/<hostname>', methods=['POST'])
def assign_vlan(hostname):
    interface = request.args.get('interface')
    vlan_id = request.json.get('vlan_id')

    if not interface or not vlan_id:
        return jsonify({'error': 'Invalid input'}), 400

    for switch in switches:
        if switch['switch-config']['hostname'] == hostname:
            for intf in switch['switch-config']['interface']:
                if intf['name'] == interface:
                    intf['vlan_id'] = vlan_id
                    return jsonify({'Success': 'VLAN assigned to interface'}), 201

    return jsonify({'Error': 'Switch or interface not found'}), 404