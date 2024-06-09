from flask import Blueprint, jsonify, request
import json

router_bp = Blueprint('router', __name__)

# List of routers added to the configuration.
routers = []

router_vlans = {
    "VLAN Ingenieria": {
        "vlan_id": 10,
        "subnet": "192.168.0.0/24"
    },
    "VLAN Mercadeo": {
        "vlan_id": 20,
        "subnet": "192.168.1.0/24"
    },
    "VLAN Legal": {
        "vlan_id": 30,
        "subnet": "192.168.2.0/24"
    }
}
# Router configuration to be added from the API.
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
          "address": "192.168.0.1",
          "netmask": "255.255.255.0"
        }
      },
        {
            "name": "GigabitEthernet0/0/1",
            "description": "Ethernet interface 1",
            "enabled": "true",
            "shutdown": "false",
            "ipv4": {
                "address": "192.168.1.1",
                "netmask": "255.255.255.0"
            }
        },
        {
            "name": "GigabitEthernet0/0/2",
            "description": "Ethernet interface 1",
            "enabled": "true",
            "shutdown": "false",
            "ipv4": {
                "address": "192.168.2.1",
                "netmask": "255.255.255.0"
            }
        }
    ]
  }
}

# Scheme for the router body to be added from the API.
router_scheme = {
    "hostname": "router",
    "type": "router",
    "username": "admin",
    "password": "admin"
}

# Scheme for the interface body to be added from the API.
interface_scheme = {
    "name": "GigabitEthernet0/0/0",
    "description": "Main Ethernet interface",
    "enabled": "true",
    "shutdown": "false"
}

#Scheme for the ipv4 body to be added from the API.
ipv4_scheme = {
    "address": "",
    "netmask": ""
}

# Device connection
router_connections = {
    "router": {
        "GigabitEthernet0/0/0": "switch1"
    }
}
router_interfaces = {
    "GigabitEthernet0/0/0.10": "VLAN Ingenieria",
    "GigabitEthernet0/0/0.20": "VLAN Mercadeo",
    "GigabitEthernet0/0/0": "VLAN Legal"
}

@router_bp.route('/get', methods=['GET'])
def get_items():
    return jsonify(routers)

"""
Add a router to the configuration. Check if the hostname already exists in the configuration.
"""
@router_bp.route('/add', methods=['POST'])
def add_router():
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

        # Assign interfaces to VLANs and connect to the switch
        for interface in new_router['router-config']['interface']:
            vlan_name = router_interfaces.get(interface['name'], None)
            if vlan_name:
                interface['description'] = f"{vlan_name} interface"
                interface['ipv4']['address'] = router_vlans[vlan_name]['subnet'].split('/')[0]
                interface['ipv4']['netmask'] = router_vlans[vlan_name]['subnet'].split('/')[1]
                interface['connected_to'] = router_connections[temp_router['hostname']][interface['name']]

        routers.append(new_router)
        return jsonify({'Success':'Router has been added'}), 201

    except (ValueError, KeyError, TypeError) as e:
        print("Error parsing information:", e)
        return jsonify({'error': 'Invalid input, Maybe try checking format?'}), 400

"""
Allow the user to change the description, enabled, and shutdown status of a specific interface on a router.
"""
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

"""
Allow the user to change the IPv4 address of a specific interface on a router.
"""
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


"""
Check if the hostname already exists between the existing routers.
"""
def CheckHostname(router_sch):
    for i in routers:
        if i['router-config']['hostname'] == router_sch['hostname']:
            return True
    return False

