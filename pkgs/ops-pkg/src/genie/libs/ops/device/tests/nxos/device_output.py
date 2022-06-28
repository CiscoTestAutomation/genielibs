"""
Device Genie Ops Object Outputs for NXOS.
"""
from genie.conf.base.utils import QDict


class DeviceOutput:

    ShowCdpNeighborsDetail = QDict({
        "index": {
            1: {
                "advertisement_ver": 2,
                "capabilities": "Router Switch IGMP Filtering",
                "device_id": "PYATS1234",
                "duplex_mode": "full",
                "hold_time": 129,
                "interface_addresses": {"172.16.3.2": {}},
                "local_interface": "Ethernet1/5",
                "management_addresses": {"172.16.3.2": {}},
                "native_vlan": "",
                "physical_location": "",
                "platform": "ISR4451-X/K9",
                "port_id": "GigabitEthernet0/0/2",
                "software_version": "Cisco IOS Software [Everest], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.4, RELEASE SOFTWARE (fc3)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2018 by Cisco Systems, Inc.\nCompiled Sun 08-Jul-18 04:33 by mcpre",
                "system_name": "",
                "vtp_management_domain": "",
            }
        },
        "total_entries_displayed": 1,
    })
    ShowCdpNeighborsDetail.raw_output = [{
        'command': 'show cdp neighbors detail',
        'output': """        
        Device ID:PYATS1234
        VTP Management Domain Name: null

        Interface address(es):
            IPv4 Address: 172.16.3.2
        Platform: ISR4451-X/K9, Capabilities: Router Switch IGMP Filtering
        Interface: Ethernet1/5, Port ID (outgoing port): GigabitEthernet0/0/2
        Holdtime: 129 sec

        Version:
        Cisco IOS Software [Everest], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.4, RELEASE SOFTWARE (fc3)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Sun 08-Jul-18 04:33 by mcpre

        Advertisement Version: 2
        Duplex: full
        Mgmt address(es):
            IPv4 Address: 172.16.3.2    
        """
    }]

    ShowLldpNeighborsDetail = QDict({
        'interfaces': {
            'mgmt0': {
                'port_id': {
                    'mgmt0': {
                        'neighbors': {
                            'System1': {
                                'chassis_id': '547f.eeff.9526',
                                'port_description': 'mgmt0',
                                'system_name': 'System1',
                                'system_description': 'Cisco NX-OS n5000, Software (n5000-uk9), Version 7.3(2)N1(1), RELEASE SOFTWARE Copyright (c) 2002-2012, 2016-2017 by Cisco Systems, Inc. Compiled 5/12/2017 23:00:00',
                                'time_remaining': 116,
                                'capabilities': {
                                    'bridge': {
                                        'name': 'bridge',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address_v4': '10.0.0.7',
                                'vlan_id': 'not advertised'
                            }
                        }
                    }
                }
            }
        },
        'total_entries': 1
    })
    ShowLldpNeighborsDetail.raw_output = [{
        'command': 'show lldp neighbors detail',
        'output': """
        Capability codes:
        (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
        (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
        Device ID            Local Intf      Hold-time  Capability  Port ID  
        Chassis id: 547f.eeff.9526
        Port id: mgmt:0
        Local Port id: mgmt0
        Port Description: mgmt0
        System Name: System1
        System Description: Cisco NX-OS n5000, Software (n5000-uk9), Version 7.3(2)N1(1), RELEASE SOFTWARE Copyright (c) 2002-2012, 2016-2017 by Cisco Systems, Inc. Compiled 5/12/2017 23:00:00
        Time remaining: 116 seconds
        System Capabilities: B
        Enabled Capabilities: B
        Management Address: 10.0.0.7
        Vlan ID: not advertised
        Total entries displayed: 1   
        """
    }]

    ShowMacAddressTable = QDict({
        'mac_table': {
            'vlans': {
                '-': {
                    'vlan': '-',
                    'mac_addresses': {
                        '5254.001a.e759': {
                            'mac_address': '5254.001a.e759',
                            'entry': 'G',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'mac_type': 'static',
                                    'age': '-'
                                }
                            },
                            'secure': 'F',
                            'ntfy': 'F'
                        }
                    }
                }
            }
        }
    })
    ShowMacAddressTable.raw_output = [{
        'command': 'show mac address-table',
        'output': """
        Note: MAC table entries displayed are getting read from software.
         Use the 'hardware-age' keyword to get information related to 'Age' 
        
         Legend: 
                * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
                        age - seconds since last seen,+ - primary entry using vPC Peer-Link, E - EVPN entry 
                        (T) - True, (F) - False ,  ~~~ - use 'hardware-age' keyword to retrieve age info 
                  VLAN/BD   MAC Address      Type      age     Secure NTFY Ports/SWID.SSID.LID
                ---------+-----------------+--------+---------+------+----+------------------
                G     -    5254.001a.e759    static       -       F    F  sup-eth1(R)"
        """
    }]

    ShowInterface = QDict({
        "Vlan1": {
            "link_state": "down",
            "autostate": True,
            "rxload": "1/255",
            "line_protocol": "down",
            "txload": "1/255",
            "oper_status": "down",
            'port_channel': {'port_channel_member': False},
            "enabled": False,
            "mtu": 1500,
            "encapsulations": {
                "encapsulation": "arpa"
            },
            "last_clear_counters": "never",
            "bandwidth": 1000000,
            "reliability": "255/255",
            "mac_address": "000c.29ff.f8a2",
            "types": "EtherSVI",
            "delay": 10
        },
        "Vlan200": {
            "link_state": "down",
            "autostate": True,
            "rxload": "1/255",
            "line_protocol": "down",
            "txload": "1/255",
            "oper_status": "down",
            'port_channel': {'port_channel_member': False},
            "enabled": True,
            "mtu": 1500,
            "encapsulations": {
                "encapsulation": "arpa"
            },
            "last_clear_counters": "never",
            "bandwidth": 1000000,
            "reliability": "255/255",
            "mac_address": "000c.29ff.f8a2",
            "types": "EtherSVI",
            "delay": 10
        }
    })
    ShowInterface.raw_output = [{
        'command': 'show interface',
        'output': """
        Vlan1 is down (Administratively down), line protocol is down, autostate enabled
        Hardware is EtherSVI, address is  000c.29ff.f8a2
        MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,

        reliability 255/255, txload 1/255, rxload 1/255
        Encapsulation ARPA, loopback not set
        Keepalive not supported
        ARP type: ARPA
        Last clearing of "show interface" counters never
        L3 in Switched:
        ucast: 0 pkts, 0 bytes

        Vlan200 is down (VLAN/BD is down), line protocol is down, autostate enabled
        Hardware is EtherSVI, address is  000c.29ff.f8a2
        MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,

        reliability 255/255, txload 1/255, rxload 1/255
        Encapsulation ARPA, loopback not set
        Keepalive not supported
        ARP type: ARPA
        Last clearing of "show interface" counters never
        L3 in Switched:
        ucast: 0 pkts, 0 bytes
        """
    }]

    ShowInventory = QDict({
        'name': {
            'Chassis': {
                'description': 'NX-OSv Chassis ', 'slot': 'None', 'pid': 'N7K-C7018', 'vid': 'V00', 'serial_number': '12345'
            },
            'Slot 1': {
                'description': 'NX-OSv Supervisor Module', 'slot': '1', 'pid': 'N7K-SUP1', 'vid': 'V00', 'serial_number': '23456'
            },
            'Slot 2': {
                'description': 'NX-OSv Ethernet Module', 'slot': '2', 'pid': 'N7K-F248XP-25', 'vid': 'V00', 'serial_number': '34567'
            },
            'Slot 3': {
                'description': 'NX-OSv Ethernet Module', 'slot': '3', 'pid': 'N7K-F248XP-25', 'vid': 'V00', 'serial_number': '45678'
            },
            'Slot 4': {
                'description': 'NX-OSv Ethernet Module', 'slot': '4', 'pid': 'N7K-F248XP-25', 'vid': 'V00', 'serial_number': '56789'
            }, 'Slot 33': {
                'description': 'NX-OSv Chassis Power Supply', 'slot': '33', 'vid': 'V00'
            }, 'Slot 35': {
                'description': 'NX-OSv Chassis Fan Module', 'slot': '35', 'vid': 'V00'
            }
        }
    })
    ShowInventory.raw_output = [{
        'command': 'show inventory',
         'output': """
         NAME: "Chassis",  DESCR: "NX-OSv Chassis "
         PID: N7K-C7018           ,  VID: V00 ,  SN: 12345          
         
         NAME: "Slot 1",  DESCR: "NX-OSv Supervisor Module"              
         PID: N7K-SUP1            ,  VID: V00 ,  SN: 23456          
         
         NAME: "Slot 2",  DESCR: "NX-OSv Ethernet Module"                
         PID: N7K-F248XP-25       ,  VID: V00 ,  SN: 34567          
         
         NAME: "Slot 3",  DESCR: "NX-OSv Ethernet Module"                
         PID: N7K-F248XP-25       ,  VID: V00 ,  SN: 45678          
         
         NAME: "Slot 4",  DESCR: "NX-OSv Ethernet Module"                
         PID: N7K-F248XP-25       ,  VID: V00 ,  SN: 56789          
         
         NAME: "Slot 33",  DESCR: "NX-OSv Chassis Power Supply"           
         PID:                     ,  VID: V00 ,  SN:                      
         
         NAME: "Slot 35",  DESCR: "NX-OSv Chassis Fan Module"             
         PID:                     ,  VID: V00 ,  SN:
         """
    }]

    ShowRunningConfig = {
        'config': "Building configuration..."
    }

    ShowVersion = QDict({
        'platform': {
            'name': 'Nexus',
            'os': 'NX-OS',
            'software': {
                'kickstart_version': '7.3(0)D1(1)',
                'system_version': '7.3(0)D1(1)',
                'kickstart_image_file': 'bootflash:///titanium-d1-kickstart.7.3.0.D1.1.bin',
                'kickstart_compile_time': '1/11/2016 16:00:00 [02/11/2016 10:30:12]',
                'system_image_file': 'bootflash:///titanium-d1.7.3.0.D1.1.bin',
                'system_compile_time': '1/11/2016 16:00:00 [02/11/2016 13:08:11]'
            },
            'hardware': {
                'model': 'NX-OSv',
                'chassis': 'NX-OSv',
                'slots': 'None',
                'rp': 'NX-OSv Supervisor Module',
                'cpu': 'Intel(R) Xeon(R) CPU E5-2695',
                'memory': '3064740 kB',
                'processor_board_id': 'TM00186CC6B',
                'device_name': 'nx-osv-1',
                'bootflash': '3184776 kB'
            },
            'kernel_uptime': {
                'days': 3,
                'hours': 2,
                'minutes': 55,
                'seconds': 18
            }
        }
    })
    ShowVersion.raw_output = [{
        'command': 'show version',
        'output': """
        Cisco Nexus Operating System (NX-OS) Software
        TAC support: http://www.cisco.com/tac
        Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html
        Copyright (c) 2002-2016, Cisco Systems, Inc. All rights reserved.
        The copyrights to certain works contained herein are owned by
        other third parties and are used and distributed under license.
        Some parts of this software are covered under the GNU Public
        License. A copy of the license is available at
        http://www.gnu.org/licenses/gpl.html.

        NX-OSv is a demo version of the Nexus Operating System

        Software
        loader:    version N/A
        kickstart: version 7.3(0)D1(1)
        system:    version 7.3(0)D1(1)
        kickstart image file is: bootflash:///titanium-d1-kickstart.7.3.0.D1.1.bin
        kickstart compile time:  1/11/2016 16:00:00 [02/11/2016 10:30:12]
        system image file is:    bootflash:///titanium-d1.7.3.0.D1.1.bin
        system compile time:     1/11/2016 16:00:00 [02/11/2016 13:08:11]


        Hardware
        cisco NX-OSv Chassis ("NX-OSv Supervisor Module")
        Intel(R) Xeon(R) CPU E5-2695 with 3064740 kB of memory.
        Processor Board ID TM00186CC6B

        Device name: nx-osv-1
        bootflash:    3184776 kB

        Kernel uptime is 5 day(s), 23 hour(s), 50 minute(s), 38 second(s)


        plugin
        Core Plugin, Ethernet Plugin

        Active Package(s)
        """
    }]

    # Device Info Structure
    DeviceInfo = {
        'version': {
            'version': '7.3(0)D1(1)',
            'system_image': 'bootflash:///titanium-d1.7.3.0.D1.1.bin',
            'built_date': '2016-02-11T13:08:11',
            'os': 'nxos',
            'platform': '',
            'raw_data': {
                'show version': '\n        Cisco Nexus Operating System (NX-OS) Software\n        TAC support: http://www.cisco.com/tac\n        Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\n        Copyright (c) 2002-2016, Cisco Systems, Inc. All rights reserved.\n        The copyrights to certain works contained herein are owned by\n        other third parties and are used and distributed under license.\n        Some parts of this software are covered under the GNU Public\n        License. A copy of the license is available at\n        http://www.gnu.org/licenses/gpl.html.\n\n        NX-OSv is a demo version of the Nexus Operating System\n\n        Software\n        loader:    version N/A\n        kickstart: version 7.3(0)D1(1)\n        system:    version 7.3(0)D1(1)\n        kickstart image file is: bootflash:///titanium-d1-kickstart.7.3.0.D1.1.bin\n        kickstart compile time:  1/11/2016 16:00:00 [02/11/2016 10:30:12]\n        system image file is:    bootflash:///titanium-d1.7.3.0.D1.1.bin\n        system compile time:     1/11/2016 16:00:00 [02/11/2016 13:08:11]\n\n\n        Hardware\n        cisco NX-OSv Chassis ("NX-OSv Supervisor Module")\n        Intel(R) Xeon(R) CPU E5-2695 with 3064740 kB of memory.\n        Processor Board ID TM00186CC6B\n\n        Device name: nx-osv-1\n        bootflash:    3184776 kB\n\n        Kernel uptime is 5 day(s), 23 hour(s), 50 minute(s), 38 second(s)\n\n\n        plugin\n        Core Plugin, Ethernet Plugin\n\n        Active Package(s)\n        '
            }
        },
        'interfaces': {
            'Vlan200': {
                'enabled': True,
                'mac_address': '000c.29ff.f8a2',
                'mtu': 1500,
                'status': 'down',
                'line_protocol': False,
                'link_state': False
            },
            'Vlan1': {
                'enabled': False,
                'mac_address': '000c.29ff.f8a2',
                'mtu': 1500,
                'status': 'down',
                'line_protocol': False,
                'link_state': False
            },
            'raw_data': {
                'show interface': '\n        Vlan1 is down (Administratively down), line protocol is down, autostate enabled\n        Hardware is EtherSVI, address is  000c.29ff.f8a2\n        MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,\n\n        reliability 255/255, txload 1/255, rxload 1/255\n        Encapsulation ARPA, loopback not set\n        Keepalive not supported\n        ARP type: ARPA\n        Last clearing of "show interface" counters never\n        L3 in Switched:\n        ucast: 0 pkts, 0 bytes\n\n        Vlan200 is down (VLAN/BD is down), line protocol is down, autostate enabled\n        Hardware is EtherSVI, address is  000c.29ff.f8a2\n        MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,\n\n        reliability 255/255, txload 1/255, rxload 1/255\n        Encapsulation ARPA, loopback not set\n        Keepalive not supported\n        ARP type: ARPA\n        Last clearing of "show interface" counters never\n        L3 in Switched:\n        ucast: 0 pkts, 0 bytes\n        '
            }
        },
        'neighbors': {
            '1': {
                'name': 'PYATS1234',
                'local_interface': 'Ethernet1/5',
                'interface': 'GigabitEthernet0/0/2',
                'addresses': ['172.16.3.2']
            },
            '2': {
                'name': 'System1',
                'interface': 'mgmt0'
            },
            'raw_data': {
                'show lldp neighbors detail': '\n        Capability codes:\n        (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device\n        (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other\n        Device ID            Local Intf      Hold-time  Capability  Port ID  \n        Chassis id: 547f.eeff.9526\n        Port id: mgmt:0\n        Local Port id: mgmt0\n        Port Description: mgmt0\n        System Name: System1\n        System Description: Cisco NX-OS n5000, Software (n5000-uk9), Version 7.3(2)N1(1), RELEASE SOFTWARE Copyright (c) 2002-2012, 2016-2017 by Cisco Systems, Inc. Compiled 5/12/2017 23:00:00\n        Time remaining: 116 seconds\n        System Capabilities: B\n        Enabled Capabilities: B\n        Management Address: 10.0.0.7\n        Vlan ID: not advertised\n        Total entries displayed: 1   \n        ',
                'show cdp neighbors detail': '        \n        Device ID:PYATS1234\n        VTP Management Domain Name: null\n\n        Interface address(es):\n            IPv4 Address: 172.16.3.2\n        Platform: ISR4451-X/K9, Capabilities: Router Switch IGMP Filtering\n        Interface: Ethernet1/5, Port ID (outgoing port): GigabitEthernet0/0/2\n        Holdtime: 129 sec\n\n        Version:\n        Cisco IOS Software [Everest], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.4, RELEASE SOFTWARE (fc3)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2018 by Cisco Systems, Inc.\n        Compiled Sun 08-Jul-18 04:33 by mcpre\n\n        Advertisement Version: 2\n        Duplex: full\n        Mgmt address(es):\n            IPv4 Address: 172.16.3.2    \n        '
            }
        },
        'inventory': {
            '1': {
                'name': 'Slot 4',
                'sn': '56789',
                'description': 'NX-OSv Ethernet Module',
                'pid': 'N7K-F248XP-25',
                'vid': 'V00'
            },
            '2': {
                'name': 'Slot 3',
                'sn': '45678',
                'description': 'NX-OSv Ethernet Module',
                'pid': 'N7K-F248XP-25',
                'vid': 'V00'
            },
            '3': {
                'name': 'Slot 2',
                'sn': '34567',
                'description': 'NX-OSv Ethernet Module',
                'pid': 'N7K-F248XP-25',
                'vid': 'V00'
            },
            '4': {
                'name': 'Slot 1',
                'sn': '23456',
                'description': 'NX-OSv Supervisor Module',
                'pid': 'N7K-SUP1',
                'vid': 'V00'
            },
            '5': {
                'name': 'Chassis',
                'sn': '12345',
                'description': 'NX-OSv Chassis ',
                'pid': 'N7K-C7018',
                'vid': 'V00'
            },
            '6': {
                'name': 'Slot 35',
                'description': 'NX-OSv Chassis Fan Module',
                'vid': 'V00'
            },
            '7': {
                'name': 'Slot 33',
                'description': 'NX-OSv Chassis Power Supply',
                'vid': 'V00'
            },
            'raw_data': {
                'show inventory': '\n         NAME: "Chassis",  DESCR: "NX-OSv Chassis "\n         PID: N7K-C7018           ,  VID: V00 ,  SN: 12345          \n         \n         NAME: "Slot 1",  DESCR: "NX-OSv Supervisor Module"              \n         PID: N7K-SUP1            ,  VID: V00 ,  SN: 23456          \n         \n         NAME: "Slot 2",  DESCR: "NX-OSv Ethernet Module"                \n         PID: N7K-F248XP-25       ,  VID: V00 ,  SN: 34567          \n         \n         NAME: "Slot 3",  DESCR: "NX-OSv Ethernet Module"                \n         PID: N7K-F248XP-25       ,  VID: V00 ,  SN: 45678          \n         \n         NAME: "Slot 4",  DESCR: "NX-OSv Ethernet Module"                \n         PID: N7K-F248XP-25       ,  VID: V00 ,  SN: 56789          \n         \n         NAME: "Slot 33",  DESCR: "NX-OSv Chassis Power Supply"           \n         PID:                     ,  VID: V00 ,  SN:                      \n         \n         NAME: "Slot 35",  DESCR: "NX-OSv Chassis Fan Module"             \n         PID:                     ,  VID: V00 ,  SN:\n         '
            }
        },
        'mac_table': {
            'vlans': {
                '-': {
                    'mac_addresses': {
                        '5254.001a.e759': {
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'age': '-'
                                }
                            }
                        }
                    }
                }
            },
            'raw_data': {
                'show mac address-table': '\n        Note: MAC table entries displayed are getting read from software.\n         Use the \'hardware-age\' keyword to get information related to \'Age\' \n        \n         Legend: \n                * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC\n                        age - seconds since last seen,+ - primary entry using vPC Peer-Link, E - EVPN entry \n                        (T) - True, (F) - False ,  ~~~ - use \'hardware-age\' keyword to retrieve age info \n                  VLAN/BD   MAC Address      Type      age     Secure NTFY Ports/SWID.SSID.LID\n                ---------+-----------------+--------+---------+------+----+------------------\n                G     -    5254.001a.e759    static       -       F    F  sup-eth1(R)"\n        '
            }
        },
        'config': {
            'running': "Building configuration..."
        },
    }
