def get_routing_table(device_id):
    return [{"prefix": "10.0.0.0/24", "next_hop": "192.168.1.254"}]

def simulate_ospf(device_id, network, area):
    return True
