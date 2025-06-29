const devices = [
    {
        "id": 1,
        "name": "Router Alpha",
        "type": "Router",
        "ip": "10.0.0.1",
        "vlan": 1,
        "cpu_load": 10,
        "mem_load": 20,
        "status": "online",
        "lat": 52.5200,
        "lon": 13.4050,
        "connected_to": [2, 3],
        "redundancy_group": 1
    },
    {
        "id": 2,
        "name": "Switch Beta",
        "type": "Switch",
        "ip": "10.0.0.2",
        "vlan": 1,
        "cpu_load": 15,
        "mem_load": 25,
        "status": "online",
        "lat": 52.5205,
        "lon": 13.4060,
        "connected_to": [1, 4]
    },
    {
        "id": 3,
        "name": "Firewall Gamma",
        "type": "Firewall",
        "ip": "10.0.1.1",
        vlan: 2,
        cpu_load: 30,
        mem_load: 40,
        status: "online",
        lat: 52.5210,
        lon: 13.4070,
        connected_to: [1]
    },
    {
        "id": 4,
        "name": "Server Delta",
        "type": "Server",
        "ip": "10.0.1.2",
        vlan: 2,
        cpu_load: 50,
        mem_load: 60,
        status: "online",
        lat: 52.5215,
        lon: 13.4080,
        connected_to: [2]
    },
];

export default devices;