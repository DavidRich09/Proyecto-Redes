from flask import Blueprint, jsonify, request
import json

router_bp = Blueprint('router', __name__)

routers = []

router = {
  "router-config": {
    "hostname": "router",
    "type": "router",
    "username": "admin",
    "password": "admin",
    "interface": [
      {
        "name": "GigabitEthernet0/0/0",
        "description": "Main Ethernet interface",
        "enabled": "true",
        "shutdown": "false",
        "ipv4": {
          "address": "0.0.0.0",
          "netmask": "255.255.255.0"
        }
      },
        {
            "name": "GigabitEthernet0/0/1",
            "description": "Ethernet interface 1",
            "enabled": "true",
            "shutdown": "false",
            "ipv4": {
                "address": "0.0.0.0",
                "netmask": "255.255.255.0"
            }
        },
        {
            "name": "GigabitEthernet0/0/2",
            "description": "Ethernet interface 1",
            "enabled": "true",
            "shutdown": "false",
            "ipv4": {
                "address": "0.0.0.0",
                "netmask": "255.255.255.0"
            }
        }
    ]
  }
}

router_scheme = {
    "hostname": "router",
    "type": "router",
    "username": "admin",
    "password": "admin"
}

interface_scheme = {
    "name": "GigabitEthernet0/0/0",
    "description": "Main Ethernet interface",
    "enabled": "true",
    "shutdown": "false"
}

ipv4_scheme = {
    "address": "",
    "netmask": ""
}


@router_bp.route('/get', methods=['GET'])
def get_items():
    return jsonify(routers)

@router_bp.route('/add', methods=['POST'])
def add_router():
    if request.content_type != 'application/yang-data+json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    temp_router = request.get_json()
    if not temp_router:
        return jsonify({'error': 'Invalid input'}), 400

    if CheckHostname(temp_router):
        return jsonify({'error': 'Router with hostname already exists'}), 400

    try:
        serialized = json.dumps(router)
        new_router = json.loads(serialized)
        new_router['router-config']['hostname'] = temp_router['hostname']
        new_router['router-config']['type'] = temp_router['type']
        new_router['router-config']['username'] = temp_router['username']
        new_router['router-config']['password'] = temp_router['password']

        routers.append(new_router)
        return jsonify({'Success':'Router has been added'}), 201

    except (ValueError, KeyError, TypeError) as e:
        print("Error parsing information:", e)
        return jsonify({'error': 'Invalid input, Maybe try checking format?'}), 400


@router_bp.route('/change/interface/<hostname>/<interface>', methods=['PUT'])
def add_interface(hostname, interface_to_change):
    config = request.get_json()
    if not config:
        return jsonify({'error': 'Invalid input'}), 400

    for i in routers:
        if i['router-config']['hostname'] == hostname:
            for interface in i['router-config']['interface']:
                if interface['name'] == interface_to_change:
                    interface['description'] = config['description']
                    interface['enabled'] = config['enabled']
                    interface['shutdown'] = config['shutdown']
                    return jsonify({'Success':'Interface has been updated'}), 201
            return jsonify({'error': 'Interface not found'}), 404
    return jsonify({'error': 'Router not found'}), 404


@router_bp.route('/change/ipv4/<hostname>/<interface>', methods=['PUT'])
def add_ipv4(hostname, interface_to_change):
    config = request.get_json()
    if not config:
        return jsonify({'error': 'Invalid input'}), 400

    for i in routers:
        if i['router-config']['hostname'] == hostname:
            for interface in i['router-config']['interface']:
                if interface['name'] == interface_to_change:
                    interface['ipv4']['address'] = config['address']
                    interface['ipv4']['netmask'] = config['netmask']
                    return jsonify({'Success': 'Interface '+interface_to_change+' has been updated'}), 201
            return jsonify({'error': 'Interface not found'}), 404
    return jsonify({'error': 'Router not found'}), 404

def CheckHostname(router_sch):
    for i in routers:
        if i['router-config']['hostname'] == router_sch['hostname']:
            return True
    return False
