import json
import requests
import time

url = 'http://localhost:5000'


def Config_Router():
    # Add router
    router0_data = {
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
    full_url = url + '/router/add'
    response = requests.post(full_url, data=router0_data)
    time.sleep(0.2)
    return response


def Config_Switch():
    # Add switch
    switch1_data = {"switch-config": {
        "hostname": "switch1",
        "vlan_id": [],
        "interface": [
            {
                "name": "FastEthernet0/0/0",
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
                "name": "GigabitEthernet0/0/0",
                "description": "Main Ethernet interface",
                "enabled": "true",
                "connected_to": ""
            }
        ]
    }
    }
    full_url = url + '/switch/add/switch1'
    response = requests.post(full_url, switch1_data)

    if response.status_code != 201:
        return response
    time.sleep(0.2)

    switch2_data = {"switch-config": {
        "hostname": "switch2",
        "vlan_id": [],
        "interface": [
            {
                "name": "FastEthernet0/0/0",
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
                "name": "GigabitEthernet0/0/0",
                "description": "Main Ethernet interface",
                "enabled": "true",
                "connected_to": ""
            }
        ]
    }
    }
    full_url = url + '/switch/add/switch2'
    response = requests.post(full_url, switch2_data)

    if response.status_code != 201:
        return response
    time.sleep(0.2)

    ################################################################################################
    # Add VLANs to switches

    vlan_data = {
        "vlan_id": 10,
        "name": "VLAN-Ingenieria"
    }

    vlan_struct = {
        "vlan_id": "10"
    }

    full_url = url + '/switch/add/vlan/switch1'
    response = requests.post(full_url, vlan_data)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    full_url = url + '/switch/assign/vlan/switch1?interface=FastEthernet0/0/0'
    response = requests.post(full_url, vlan_struct)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_data["vlan_id"] = "20"
    full_url = url + '/switch/add/vlan/switch1'
    response = requests.post(full_url, vlan_data)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_struct["vlan_id"] = "20"
    full_url = url + '/switch/assign/vlan/switch1?interface=FastEthernet0/0/1'
    response = requests.post(full_url, vlan_struct)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_data["vlan_id"] = "30"
    full_url = url + '/switch/add/vlan/switch1'
    response = requests.post(full_url, vlan_data)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_struct["vlan"] = "30"
    full_url = url + '/switch/assign/vlan/switch1?interface=FastEthernet0/0/2'
    response = requests.post(full_url, vlan_struct)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    ########################################################################################
    # Switch 2

    vlan_data["vlan_id"] = "10"
    full_url = url + '/switch/add/vlan/switch2'
    response = requests.post(full_url, vlan_data)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_struct["vlan_id"] = "10"
    full_url = url + '/switch/assign/vlan/switch2?interface=FastEthernet0/0/0'
    response = requests.post(full_url, vlan_struct)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_data["vlan_id"] = "20"
    full_url = url + '/switch/add/vlan/switch2'
    response = requests.post(full_url, vlan_data)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_struct["vlan_id"] = "20"
    full_url = url + '/switch/assign/vlan/switch2?interface=FastEthernet0/0/1'
    response = requests.post(full_url, vlan_struct)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_data["vlan_id"] = "30"
    full_url = url + '/switch/add/vlan/switch2'
    response = requests.post(full_url, vlan_data)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    vlan_struct["vlan"] = "30"
    full_url = url + '/switch/assign/vlan/switch1?interface=FastEthernet0/0/2'
    response = requests.post(full_url, vlan_struct)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    ##################################################################################################

    return response

def Config_PC():

    full_url = url + '/pc/add/PC0'
    response = requests.post(full_url)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    full_url = url + '/pc/add/PC1'
    response = requests.post(full_url)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    full_url = url + '/pc/add/PC2'
    response = requests.post(full_url)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    full_url = url + '/pc/add/PC3'
    response = requests.post(full_url)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    full_url = url + '/pc/add/PC4'
    response = requests.post(full_url)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    full_url = url + '/pc/add/PC5'
    response = requests.post(full_url)
    if response.status_code != 201:
        return response
    time.sleep(0.2)

    return response

def Tests():

    full_url = url + '/pc/ping/PC0/PC3'
    response = requests.get(full_url)
    if response.status_code != 200:
        return response
    time.sleep(0.2)

    response1 = response.json()

    full_url = url + '/pc/ping/PC1/PC4'
    response = requests.get(full_url)
    if response.status_code != 200:
        return response
    time.sleep(0.2)

    response2 = response.json()

    full_url = url + '/pc/ping/PC2/PC5'
    response = requests.get(full_url)
    if response.status_code != 200:
        return response
    time.sleep(0.2)

    response3 = response.json()

    full_url = url + '/pc/ping/PC3/PC5'
    response = requests.get(full_url)
    if response.status_code != 200:
        return response
    time.sleep(0.2)

    response4 = response.json()

    return response1, response2, response3, response4

def main():
    print("Configuring devices...")
    Config_Router()
    print("Router configured")
    print("Configuring switches...")
    Config_Switch()
    print("Switches configured")
    print("Configuring PCs...")
    Config_PC()
    print("PCs configured")
    print("Running tests...")
    results = Tests()
    for result in results:
        print(result)
    print("Tests finished")

main()
