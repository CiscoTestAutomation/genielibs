    
''' 
Interface Genie Ops Object Outputs for IOSXR IOSXE NXOS.
'''


class InterfaceOutput(object):
    IosxrInterfaceOpsOutput_info = {
        "info":{
          "Null0": {
            "mtu": 1500,
            "type": "Null",
            "enabled": True,
            "bandwidth": 0,
            "counters": {
                 "in_octets": 0,
                 "out_broadcast_pkts": 0,
                 "out_pkts": 0,
                 "in_discards": 0,
                 "in_pkts": 0,
                 "in_multicast_pkts": 0,
                 "in_broadcast_pkts": 0,
                 "rate": {
                      "out_rate": 0,
                      "out_rate_pkts": 0,
                      "in_rate_pkts": 0,
                      "load_interval": 5,
                      "in_rate": 0
                 },
                 "last_clear": "never",
                 "out_multicast_pkts": 0,
                 "out_octets": 0
            },
            "encapsulation": {
                 "encapsulation": "Null"
            },
        },
        "MgmtEth0/0/CPU0/0": {
            "mtu": 1514,
            "mac_address": "5254.00c3.6c43",
            "flow_control": {
                 "flow_control_receive": False,
                 "flow_control_send": False
            },
            "type": "Management Ethernet",
            "enabled": False,
            "encapsulation": {
                 "encapsulation": "ARPA"
            },
            "auto_negotiate": True,
            "bandwidth": 0,
            "counters": {
                 "out_broadcast_pkts": 0,
                 "in_multicast_pkts": 0,
                 "in_crc_errors": 0,
                 "in_pkts": 0,
                 "in_errors": 0,
                 "in_broadcast_pkts": 0,
                 "out_multicast_pkts": 0,
                 "out_errors": 0,
                 "in_octets": 0,
                 "rate": {
                      "out_rate": 0,
                      "out_rate_pkts": 0,
                      "in_rate_pkts": 0,
                      "load_interval": 5,
                      "in_rate": 0
                 },
                 "out_pkts": 0,
                 "in_discards": 0,
                 "last_clear": "never",
                 "out_octets": 0
            },
            "duplex_mode": "duplex unknown",
            "port_speed": "0Kb/s",
            "phys_address": "5254.00c3.6c43",
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/5": {
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/4": {
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/0": {
            "mtu": 1600,
            "mac_address": "aaaa.bbbb.cccc",
            "description": "desc",
            "duplex_mode": "full",
            "type": "GigabitEthernet",
            "enabled": False,
            "encapsulation": {
                 "encapsulation": "ARPA"
            },
            "auto_negotiate": True,
            "ipv4": {
                 "10.1.3.1/24": {
                      "ip": "10.1.3.1",
                      "prefix_length": "24",
                    },

            },
            "bandwidth": 768,
            "accounting": {
                 "arp": {
                      "chars_in": 378,
                      "chars_out": 378,
                      "pkts_in": 9,
                      "pkts_out": 9
                 },
                 "ipv4_multicast": {
                      "chars_in": 0,
                      "chars_out": 843700,
                      "pkts_in": 0,
                      "pkts_out": 10514
                 },
                 "ipv4_unicast": {
                      "chars_in": 1226852,
                      "chars_out": 887519,
                      "pkts_in": 19254,
                      "pkts_out": 13117
                 }
            },
            "counters": {
                 "out_broadcast_pkts": 0,
                 "in_multicast_pkts": 0,
                 "in_crc_errors": 0,
                 "in_pkts": 0,
                 "in_errors": 0,
                 "in_broadcast_pkts": 0,
                 "out_multicast_pkts": 0,
                 "out_errors": 0,
                 "in_octets": 0,
                 "rate": {
                      "out_rate": 0,
                      "out_rate_pkts": 0,
                      "in_rate_pkts": 0,
                      "load_interval": 30,
                      "in_rate": 0
                 },
                 "out_pkts": 0,
                 "in_discards": 0,
                 "last_clear": "never",
                 "out_octets": 0
            },
            "flow_control": {
                 "flow_control_receive": False,
                 "flow_control_send": False
            },
            "port_speed": "1000Mb/s",
            "phys_address": "5254.0077.9407",
            "ipv6": {
                 "2001:db8:2:2::2/64": {
                      "status": "tentative",
                      "ip": "2001:db8:2:2::2",
                      "prefix_length": "64"
                 },
                 "2001:db8:1:1::1/64": {
                      "status": "tentative",
                      "ip": "2001:db8:1:1::1",
                      "prefix_length": "64"
                 },
                 "enabled": False,
                 "2001:db8:4:4::4/64": {
                      "status": "tentative",
                      "route_tag": "10",
                      "ip": "2001:db8:4:4::4",
                      "prefix_length": "64"
                 },
                 "2001:db8:3:3:a8aa:bbff:febb:cccc/64": {
                      "status": "tentative",
                      "ip": "2001:db8:3:3:a8aa:bbff:febb:cccc",
                      "prefix_length": "64",
                      "eui64": True
                 }
            }
        },
        "GigabitEthernet0/0/0/1": {
            "vrf": "VRF1",
             "ipv6": {
                  '2001:db8:1:5::1/64': {
                      'ip': '2001:db8:1:5::1',
                      'prefix_length': '64'
                  },
                  'enabled': True},
            'ipv4': {
                '10.1.5.1/24': {
                   'ip': '10.1.5.1',
                         'prefix_length': '24',
                         'route_tag': 50},
                     '10.2.2.2/24': {
                         'ip': '10.2.2.2',
                         'prefix_length': '24',
                         'secondary': True}},

            "accounting": {
                 "arp": {
                      "chars_in": 378,
                      "chars_out": 378,
                      "pkts_in": 9,
                      "pkts_out": 9
                 },
                 "ipv4_multicast": {
                      "chars_in": 0,
                      "chars_out": 844816,
                      "pkts_in": 0,
                      "pkts_out": 10530
                 },
                 "ipv4_unicast": {
                      "chars_in": 843784,
                      "chars_out": 1764,
                      "pkts_in": 10539,
                      "pkts_out": 26
                 }
            }
        },
        "GigabitEthernet0/0/0/6": {
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/0.20": {
            "mtu": 1604,
            "counters": {
                 "in_octets": 0,
                 "out_broadcast_pkts": 0,
                 "out_pkts": 0,
                 "in_discards": 0,
                 "in_pkts": 0,
                 "in_multicast_pkts": 0,
                 "in_broadcast_pkts": 0,
                 "rate": {
                      "out_rate": 0,
                      "out_rate_pkts": 0,
                      "in_rate_pkts": 0,
                      "load_interval": 5,
                      "in_rate": 0
                 },
                 "last_clear": "never",
                 "out_multicast_pkts": 0,
                 "out_octets": 0
            },
            "enabled": False,
            "bandwidth": 768,
            "vlan_id": '20',
            "encapsulation": {
                 "encapsulation": "802.1Q Virtual LAN",
                 "first_dot1q": "20"
            },
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/2": {
            "vrf": "VRF2",
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/3": {
            "ipv6": {
                 "enabled": False
            }
        },
        "GigabitEthernet0/0/0/0.10": {
            "mtu": 1608,
            "counters": {
                 "in_octets": 0,
                 "out_broadcast_pkts": 0,
                 "out_pkts": 0,
                 "in_discards": 0,
                 "in_pkts": 0,
                 "in_multicast_pkts": 0,
                 "in_broadcast_pkts": 0,
                 "rate": {
                      "out_rate": 0,
                      "out_rate_pkts": 0,
                      "in_rate_pkts": 0,
                      "load_interval": 5,
                      "in_rate": 0
                 },
                 "last_clear": "never",
                 "out_multicast_pkts": 0,
                 "out_octets": 0
            },
            "enabled": False,
            "bandwidth": 768,
            "vlan_id": '10',
            "encapsulation": {
                 "encapsulation": "802.1Q Virtual LAN",
                 "first_dot1q": "10",
                 "second_dot1q": "10"
            },
            "ipv6": {
                '2001:db8:1:3::1/64': {
                    'ip': '2001:db8:1:3::1',
                      'prefix_length': '64'},
                 "enabled": False
            }
        }
    }   
    }   
    NxosInterfaceOpsOutput_info={
       'info':
            {
        'Ethernet1/1': {'bandwidth': 100000000,
                          'delay': 10,
                          'enabled': True,
                          'mac_address': '188b.9df3.2a9f',
                          'mtu': 1500,
                        'oper_status': 'down',
                        'phys_address': '188b.9df3.2aa0',
                        'port_channel': {'port_channel_member': False},
                        'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/10': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2ac4',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/11': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2ac8',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/12': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2acc',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/13': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2ad0',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/14': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2ad4',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/15': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2ad8',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/16': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2adc',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/17': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'up',
                         'phys_address': '188b.9df3.2ae0',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet1/18': {'bandwidth': 100000000,
                         'delay': 10,
                         'enabled': True,
                         'mac_address': '188b.9df3.2a9f',
                         'mtu': 1500,
                         'oper_status': 'down',
                         'phys_address': '188b.9df3.2ae4',
                         'port_channel': {'port_channel_member': False},
                         'type': '100/1000/10000/25000/40000/100000 Ethernet'},
        'Ethernet2/1': {'vrf': 'VRF1'},
        'Mgmt0': {'bandwidth': 1000000,
                  'delay': 10,
                  'enabled': True,
                  'mac_address': '188b.9df3.2a98',
                  'mtu': 1500,
                  'oper_status': 'up',
                  'phys_address': '188b.9df3.2a98',
                  'port_channel': {'port_channel_member': False},
                  'type': 'GigabitEthernet',
                  'vrf': 'management'},
        'Null0': {'vrf': 'default'}
    }}  
    IosxeInterfaceOutput_info = {
       'info':{
          'GigabitEthernet0/0/0': {'bandwidth': 1000000,
              'delay': 10,
              'enabled': False,
              'ipv6': {'FE80::72EA:1AFF:FEB5:49B0': {'ip': 'FE80::72EA:1AFF:FEB5:49B0',
                                                      'origin': 'link_layer',
                                                      'status': 'tentative'}},
              'mac_address': '70ea.1ab5.49b0',
              'mtu': 1500,
              'oper_status': 'down',
              'phys_address': '70ea.1ab5.49b0',
              'port_channel': {'port_channel_member': False},
              'switchport_enable': False,
              'type': 'ISR4221-2x1GE'},
          'GigabitEthernet0/0/1': {'bandwidth': 1000000,
              'delay': 10,
              'enabled': False,
              'mac_address': '70ea.1ab5.49b1',
              'mtu': 1500,
              'oper_status': 'down',
              'phys_address': '70ea.1ab5.49b1',
              'port_channel': {'port_channel_member': False},
              'switchport_enable': False,
              'type': 'ISR4221-2x1GE'},
          'GigabitEthernet0/1/0': {'bandwidth': 1000000,
              'delay': 10,
              'enabled': False,
              'mac_address': '70ea.1ab5.49b8',
              'mtu': 1500,
              'oper_status': 'down',
              'phys_address': '70ea.1ab5.49b8',
              'port_channel': {'port_channel_member': False},
              'switchport_enable': False,
              'type': 'NIM-1GE-CU-SFP'},
          'GigabitEthernet0/2/0': {'bandwidth': 1000000,
              'delay': 10,
              'enabled': False,
              'mac_address': '70ea.1ab5.49c0',
              'mtu': 1500,
              'oper_status': 'down',
              'phys_address': '70ea.1ab5.49c0',
              'port_channel': {'port_channel_member': False},
              'switchport_enable': False,
              'type': 'NIM-1GE-CU-SFP'},
          'GigabitEthernet1/0/1': {'switchport_enable': False, 'vrf': 'VRF1'},
          'GigabitEthernet1/0/2': {'switchport_enable': False, 'vrf': 'Mgmt-intf'}}}