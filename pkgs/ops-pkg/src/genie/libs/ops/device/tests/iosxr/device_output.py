"""
Device Genie Ops Object Outputs for IOSXR.
"""
from genie.conf.base.utils import QDict

class DeviceOutput:

    ShowCdpNeighborsDetail = QDict({
        "total_entries_displayed": 1,
        "index": {
            1: {
                "device_id": "R3_nx.cisco.com(972ZZK4REQK)",
                "duplex_mode": "full",
                "system_name": "R3_nx",
                "native_vlan": "1",
                "entry_addresses": {
                    "172.16.1.53": {}
                },
                "capabilities": "Router Switch IGMP",
                "platform": "N9K-9000v",
                "local_interface": "GigabitEthernet0/0/0/5",
                "port_id": "Ethernet1/4",
                "hold_time": 138,
                "software_version": "Cisco Nexus Operating System (NX-OS) Software, Version 9.2(1)",
                "advertisement_ver": 2
            }
        }
    })
    ShowCdpNeighborsDetail.raw_output = [{
        'command': 'show cdp neighbors detail',
        'output': """
        Device ID: R3_nx.cisco.com(972ZZK4REQK)
        SysName : R3_nx
        Entry address(es):
        IPv4 address: 172.16.1.53
        Platform: N9K-9000v,  Capabilities: Router Switch IGMP
        Interface: GigabitEthernet0/0/0/5
        Port ID (outgoing port): Ethernet1/4
        Holdtime : 138 sec

        Version :
        Cisco Nexus Operating System (NX-OS) Software, Version 9.2(1)

        advertisement version: 2
        Native VLAN: 1
        Duplex: full
        """
    }]

    ShowLldpNeighborsDetail = QDict({
        'interfaces': {
            'TenGigE0/0/0/28/0': {
                'port_id': {
                    'xe-0/1/2': {
                        'neighbors': {
                            'switch1': {
                                'capabilities': {
                                    'bridge': {
                                        'enabled': True,
                                        'system': True,
                                    },
                                    'router': {
                                        'enabled': True,
                                        'system': True,
                                    },
                                },
                                'chassis_id': '6464.9bff.6e31',
                                'hold_time': 120,
                                'neighbor_id': 'switch1',
                                'peer_mac': '64:64:9b:ff:6e:66',
                                'port_description': 'port description',
                                'system_description': '',
                                'system_name': 'switch1',
                                'time_remaining': 108,
                            },
                        },
                    },
                },
            },
        },
        'total_entries': 1,
    })
    ShowLldpNeighborsDetail.raw_output = [{
        'command': 'show lldp neighbors detail',
        'output': """
        Tue Oct  6 13:56:33.804 UTC
        Capability codes:
            (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
            (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

        ------------------------------------------------
        Local Interface: TenGigE0/0/0/28/0
        Chassis id: 6464.9bff.6e31
        Port id: xe-0/1/2
        Port Description: port description
        System Name: switch1

        System Description:
        Juniper Networks, Inc. ex4200-48t , version 12.3R9.4 Build date: 2015-02-12 12:01:56 UTC

        Time remaining: 108 seconds
        Hold Time: 120 seconds
        System Capabilities: B,R
        Enabled Capabilities: B,R
        Management Addresses - not advertised
        Peer MAC Address: 64:64:9b:ff:6e:66


        Total entries displayed: 1
        """
    }]

    ShowInterfaces = QDict({
        "Bundle-Ether1": {
            "enabled": True,
            "line_protocol": "up",
            "oper_status": "up",
            "interface_state_transitions": 9,
            "type": "Aggregated Ethernet interface(s)",
            "mac_address": "00bc.60ff.1119",
            "description": "to-ML26-BE1",
            "ipv4": {"192.168.0.25/30": {"ip": "192.168.0.25", "prefix_length": "30"}},
            "mtu": 1514,
            "bandwidth": 100000000,
            "bandwidth_max": 100000000,
            "reliability": "255/255",
            "txload": "0/255",
            "rxload": "0/255",
            "encapsulations": {"encapsulation": "arpa"},
            "duplex_mode": "full",
            "port_speed": "100000Mb/s",
            "loopback": "not set",
            "last_link_flapped": "3w3d",
            "arp_type": "arpa",
            "arp_timeout": "04:00:00",
            "port_channel": {
                "member_count": 1,
                "members": {
                    "HundredGigE0/0/1/2/0": {
                        "interface": "HundredGigE0/0/1/2/0",
                        "duplex_mode": "Full-duplex",
                        "speed": "100000Mb/s",
                        "state": "Active",
                    }
                },
            },
            "last_input": "00:00:00",
            "last_output": "00:00:00",
            "counters": {
                "last_clear": "never",
                "rate": {
                    "load_interval": 30,
                    "in_rate": 1000,
                    "in_rate_pkts": 0,
                    "out_rate": 2000,
                    "out_rate_pkts": 1,
                },
                "in_pkts": 1716386544,
                "in_octets": 751342403591,
                "in_total_drops": 0,
                "in_unknown_protos": 0,
                "in_broadcast_pkts": 6,
                "in_multicast_pkts": 642898,
                "in_runts": 0,
                "in_giants": 0,
                "in_throttles": 0,
                "in_parity": 0,
                "in_errors": 0,
                "in_crc_errors": 0,
                "in_frame": 0,
                "in_overrun": 0,
                "in_ignored": 0,
                "in_abort": 0,
                "out_pkts": 1714349214,
                "out_octets": 754526715390,
                "out_total_drops": 0,
                "out_broadcast_pkts": 12,
                "out_multicast_pkts": 642896,
                "out_errors": 0,
                "out_underruns": 0,
                "out_applique": 0,
                "out_resets": 0,
                "out_buffer_failure": 0,
                "out_buffers_swapped": 0,
                "carrier_transitions": 0,
            },
        }
    })
    ShowInterfaces.raw_output = [{
        'command': 'show interfaces',
        'output': """
        Bundle-Ether1 is up, line protocol is up 
        Interface state transitions: 9
        Hardware is Aggregated Ethernet interface(s), address is 00bc.60ff.1119
        Description: to-ML26-BE1
        Internet address is 192.168.0.25/30
        MTU 1514 bytes, BW 100000000 Kbit (Max: 100000000 Kbit)
            reliability 255/255, txload 0/255, rxload 0/255
        Encapsulation ARPA,
        Full-duplex, 100000Mb/s
        loopback not set,
        Last link flapped 3w3d
        ARP type ARPA, ARP timeout 04:00:00
            No. of members in this bundle: 1
            HundredGigE0/0/1/2/0         Full-duplex  100000Mb/s   Active          
        Last input 00:00:00, output 00:00:00
        Last clearing of "show interface" counters never
        30 second input rate 1000 bits/sec, 0 packets/sec
        30 second output rate 2000 bits/sec, 1 packets/sec
            1716386544 packets input, 751342403591 bytes, 0 total input drops
            0 drops for unrecognized upper-level protocol
            Received 6 broadcast packets, 642898 multicast packets
                    0 runts, 0 giants, 0 throttles, 0 parity
            0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
            1714349214 packets output, 754526715390 bytes, 0 total output drops
            Output 12 broadcast packets, 642896 multicast packets
            0 output errors, 0 underruns, 0 applique, 0 resets
            0 output buffer failures, 0 output buffers swapped out
            0 carrier transitions
        """
    }]

    ShowInventory = QDict({
        'module_name': {
            '0/0': {
                'descr': 'Cisco IOS-XRv 9000 Centralized Line Card',
                'pid': 'R-IOSXRV9000-LC-C',
                'vid': 'V01',
                'sn': '1234'
            },
            '0/0/0': {
                'descr': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '0/0/1': {
                'descr': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '0/0/2': {
                'descr': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '0/0/3': {
                'descr': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '0/0/4': {
                'descr': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'},
            '0/0/5': {
                'descr': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'},
                '0/RP0': {'descr': 'Cisco IOS-XRv 9000 Centralized Route Processor',
                'pid': 'R-IOSXRV9000-RP-C',
                'vid': 'V01',
                'sn': '2345'
            },
            'Rack 0': {
                'descr': 'Cisco IOS-XRv 9000 Centralized Virtual Router',
                'pid': 'R-IOSXRV9000-CC',
                'vid': 'V01',
                'sn': '3456'
            }
        }
    })
    ShowInventory.raw_output = [{
        'command': 'show inventory',
        'output': """
        NAME: "0/0", DESCR: "Cisco IOS-XRv 9000 Centralized Line Card"
        PID: R-IOSXRV9000-LC-C , VID: V01, SN: 1234

        NAME: "0/0/0", DESCR: "N/A"
        PID: PORT-1G-NIC       , VID: N/A, SN: N/A

        NAME: "0/0/1", DESCR: "N/A"
        PID: PORT-1G-NIC       , VID: N/A, SN: N/A

        NAME: "0/0/2", DESCR: "N/A"
        PID: PORT-1G-NIC       , VID: N/A, SN: N/A

        NAME: "0/0/3", DESCR: "N/A"
        PID: PORT-1G-NIC       , VID: N/A, SN: N/A

        NAME: "0/0/4", DESCR: "N/A"
        PID: PORT-1G-NIC       , VID: N/A, SN: N/A

        NAME: "0/0/5", DESCR: "N/A"
        PID: PORT-1G-NIC       , VID: N/A, SN: N/A

        NAME: "0/RP0", DESCR: "Cisco IOS-XRv 9000 Centralized Route Processor"
        PID: R-IOSXRV9000-RP-C , VID: V01, SN: 2345

        NAME: "Rack 0", DESCR: "Cisco IOS-XRv 9000 Centralized Virtual Router"
        PID: R-IOSXRV9000-CC   , VID: V01, SN: 3456
        """
    }]

    ShowRunningConfig = {
        'config': "Building configuration..."
    }

    ShowVersion = QDict({
        'operating_system': 'IOSXR',
        'software_version': '6.6.3',
        'built_by': 'hlo',
        'built_on': 'Fri Dec 13 16:42:11 PST 2019',
        'built_host': 'iox-ucs-033',
        'device_family': 'IOS-XRv 9000',
        'uptime': '2 hours 52 minutes'
    })
    ShowVersion.raw_output = [{
        'command': 'show version',
        'output': """
        Cisco IOS XR Software, Version 6.6.3
        Copyright (c) 2013-2019 by Cisco Systems, Inc.

        Build Information:
        Built By     : hlo
        Built On     : Fri Dec 13 16:42:11 PST 2019
        Built Host   : iox-ucs-033
        Workspace    : /auto/srcarchive15/prod/6.6.3/xrv9k/ws
        Version      : 6.6.3
        Location     : /opt/cisco/XR/packages/

        cisco IOS-XRv 9000 () processor
        System uptime is 2 hours 32 minutes
        """
    }]

    # Device Info Structure
    DeviceInfo = {
        'version': {
            'os': 'iosxr',
            'platform': 'iosxrv9k',
            'version': '6.6.3',
            'built_by': 'hlo',
            'built_date': '2019-12-13T16:42:11',
            'raw_data': {
                'show version': '\n        Cisco IOS XR Software, Version 6.6.3\n        Copyright (c) 2013-2019 by Cisco Systems, Inc.\n\n        Build Information:\n        Built By     : hlo\n        Built On     : Fri Dec 13 16:42:11 PST 2019\n        Built Host   : iox-ucs-033\n        Workspace    : /auto/srcarchive15/prod/6.6.3/xrv9k/ws\n        Version      : 6.6.3\n        Location     : /opt/cisco/XR/packages/\n\n        cisco IOS-XRv 9000 () processor\n        System uptime is 2 hours 32 minutes\n        '
            }
        },
        'interfaces': {
            'Bundle-Ether1': {
                'enabled': True,
                'mac_address': '00bc.60ff.1119',
                'mtu': 1514,
                'duplex': 'full',
                'status': 'up',
                'speed': '100000',
                'speed_unit': 'Mb/s',
                'line_protocol': True
            },
            'raw_data': {
                'show interfaces': '\n        Bundle-Ether1 is up, line protocol is up \n        Interface state transitions: 9\n        Hardware is Aggregated Ethernet interface(s), address is 00bc.60ff.1119\n        Description: to-ML26-BE1\n        Internet address is 192.168.0.25/30\n        MTU 1514 bytes, BW 100000000 Kbit (Max: 100000000 Kbit)\n            reliability 255/255, txload 0/255, rxload 0/255\n        Encapsulation ARPA,\n        Full-duplex, 100000Mb/s\n        loopback not set,\n        Last link flapped 3w3d\n        ARP type ARPA, ARP timeout 04:00:00\n            No. of members in this bundle: 1\n            HundredGigE0/0/1/2/0         Full-duplex  100000Mb/s   Active          \n        Last input 00:00:00, output 00:00:00\n        Last clearing of "show interface" counters never\n        30 second input rate 1000 bits/sec, 0 packets/sec\n        30 second output rate 2000 bits/sec, 1 packets/sec\n            1716386544 packets input, 751342403591 bytes, 0 total input drops\n            0 drops for unrecognized upper-level protocol\n            Received 6 broadcast packets, 642898 multicast packets\n                    0 runts, 0 giants, 0 throttles, 0 parity\n            0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort\n            1714349214 packets output, 754526715390 bytes, 0 total output drops\n            Output 12 broadcast packets, 642896 multicast packets\n            0 output errors, 0 underruns, 0 applique, 0 resets\n            0 output buffer failures, 0 output buffers swapped out\n            0 carrier transitions\n        '
            }
        },
        'neighbors': {
            '1': {
                'name': 'R3_nx.cisco.com(972ZZK4REQK)',
                'local_interface': 'GigabitEthernet0/0/0/5',
                'interface': 'Ethernet1/4',
                'addresses': ['172.16.1.53']
            },
            '2': {
                'name': 'switch1',
                'interface': 'xe-0/1/2'
            },
            'raw_data': {
                'show lldp neighbors detail': '\n        Tue Oct  6 13:56:33.804 UTC\n        Capability codes:\n            (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device\n            (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other\n\n        ------------------------------------------------\n        Local Interface: TenGigE0/0/0/28/0\n        Chassis id: 6464.9bff.6e31\n        Port id: xe-0/1/2\n        Port Description: port description\n        System Name: switch1\n\n        System Description:\n        Juniper Networks, Inc. ex4200-48t , version 12.3R9.4 Build date: 2015-02-12 12:01:56 UTC\n\n        Time remaining: 108 seconds\n        Hold Time: 120 seconds\n        System Capabilities: B,R\n        Enabled Capabilities: B,R\n        Management Addresses - not advertised\n        Peer MAC Address: 64:64:9b:ff:6e:66\n\n\n        Total entries displayed: 1\n        ', 'show cdp neighbors detail': '\n        Device ID: R3_nx.cisco.com(972ZZK4REQK)\n        SysName : R3_nx\n        Entry address(es):\n        IPv4 address: 172.16.1.53\n        Platform: N9K-9000v,  Capabilities: Router Switch IGMP\n        Interface: GigabitEthernet0/0/0/5\n        Port ID (outgoing port): Ethernet1/4\n        Holdtime : 138 sec\n\n        Version :\n        Cisco Nexus Operating System (NX-OS) Software, Version 9.2(1)\n\n        advertisement version: 2\n        Native VLAN: 1\n        Duplex: full\n        '
            }
        },
        'inventory': {
            '1': {
                'name': 'Rack 0',
                'description': 'Cisco IOS-XRv 9000 Centralized Virtual Router',
                'pid': 'R-IOSXRV9000-CC',
                'vid': 'V01',
                'sn': '3456'
            },
            '2': {
                'name': '0/RP0',
                'description': 'Cisco IOS-XRv 9000 Centralized Route Processor',
                'pid': 'R-IOSXRV9000-RP-C',
                'vid': 'V01',
                'sn': '2345'
            },
            '3': {
                'name': '0/0/5',
                'description': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '4': {
                'name': '0/0/4',
                'description': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '5': {
                'name': '0/0/3',
                'description': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '6': {
                'name': '0/0/2',
                'description': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '7': {
                'name': '0/0/1',
                'description': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '8': {
                'name': '0/0/0',
                'description': 'N/A',
                'pid': 'PORT-1G-NIC',
                'vid': 'N/A',
                'sn': 'N/A'
            },
            '9': {
                'name': '0/0',
                'description': 'Cisco IOS-XRv 9000 Centralized Line Card',
                'pid': 'R-IOSXRV9000-LC-C',
                'vid': 'V01',
                'sn': '1234'
            },
            'raw_data': {
                'show inventory': '\n        NAME: "0/0", DESCR: "Cisco IOS-XRv 9000 Centralized Line Card"\n        PID: R-IOSXRV9000-LC-C , VID: V01, SN: 1234\n\n        NAME: "0/0/0", DESCR: "N/A"\n        PID: PORT-1G-NIC       , VID: N/A, SN: N/A\n\n        NAME: "0/0/1", DESCR: "N/A"\n        PID: PORT-1G-NIC       , VID: N/A, SN: N/A\n\n        NAME: "0/0/2", DESCR: "N/A"\n        PID: PORT-1G-NIC       , VID: N/A, SN: N/A\n\n        NAME: "0/0/3", DESCR: "N/A"\n        PID: PORT-1G-NIC       , VID: N/A, SN: N/A\n\n        NAME: "0/0/4", DESCR: "N/A"\n        PID: PORT-1G-NIC       , VID: N/A, SN: N/A\n\n        NAME: "0/0/5", DESCR: "N/A"\n        PID: PORT-1G-NIC       , VID: N/A, SN: N/A\n\n        NAME: "0/RP0", DESCR: "Cisco IOS-XRv 9000 Centralized Route Processor"\n        PID: R-IOSXRV9000-RP-C , VID: V01, SN: 2345\n\n        NAME: "Rack 0", DESCR: "Cisco IOS-XRv 9000 Centralized Virtual Router"\n        PID: R-IOSXRV9000-CC   , VID: V01, SN: 3456\n        '
            }
        },
        'config': {
            'running': "Building configuration..."
        },
    }
