"""
Device Genie Ops Object Outputs for Cat9k.
"""
from genie.conf.base.utils import QDict

class DeviceOutput:

    ShowBoot = QDict({
        'current_boot_variable': 'flash:packages.conf;',
        'next_reload_boot_variable': 'flash:packages.conf;',
        'manual_boot': False,
        'enable_break': False,
        'boot_mode': 'device',
        'ipxe_timeout': 0
    })

    ShowBoot.raw_output = [{
        'command': 'show boot',
        'output': """
        ---------------------------
        Switch 2
        ---------------------------
        Current Boot Variables:
        BOOT variable = flash:packages.conf;

        Boot Variables on next reload:
        BOOT variable = flash:packages.conf;
        Manual Boot = no
        Enable Break = no
        Boot Mode = DEVICE
        iPXE Timeout = 0
        """
    }]

    ShowCdpNeighborsDetail = QDict({
        "total_entries_displayed": 2,
        "index": {
            1: {
                "advertisement_ver": 2,
                "capabilities": "Router Source-Route-Bridge",
                "device_id": "R8",
                "duplex_mode": "",
                "entry_addresses": {"172.16.1.205": {}},
                "hold_time": 143,
                "local_interface": "GigabitEthernet0/0",
                "management_addresses": {"172.16.1.205": {}},
                "native_vlan": "",
                "platform": "Cisco ",
                "port_id": "GigabitEthernet0/0",
                "software_version": "Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.7(3)M3, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2018 by Cisco Systems, Inc.\nCompiled Wed 01-Aug-18 16:45 by prod_rel_team",
                "vtp_management_domain": "",
            },
            2: {
                "advertisement_ver": 2,
                "capabilities": "Router Source-Route-Bridge",
                "device_id": "R9",
                "duplex_mode": "",
                "entry_addresses": {"172.16.1.206": {}},
                "hold_time": 151,
                "local_interface": "GigabitEthernet0/0",
                "management_addresses": {"172.16.1.206": {}},
                "native_vlan": "",
                "platform": "Cisco ",
                "port_id": "GigabitEthernet0/0",
                "software_version": "Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.7(3)M3, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2018 by Cisco Systems, Inc.\nCompiled Wed 01-Aug-18 16:45 by prod_rel_team",
                "vtp_management_domain": "",
            },
        },
    })
    ShowCdpNeighborsDetail.raw_output = [{
        'command': 'show cdp neighbors detail',
        'output': """
        Device ID: R8
        Entry address(es):
        IP address: 172.16.1.205
        Platform: Cisco ,  Capabilities: Router Source-Route-Bridge
        Interface: GigabitEthernet0/0,  Port ID (outgoing port): GigabitEthernet0/0
        Holdtime : 143 sec

        Version :
        Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.7(3)M3, RELEASE SOFTWARE (fc2)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Wed 01-Aug-18 16:45 by prod_rel_team

        advertisement version: 2
        Management address(es):
        IP address: 172.16.1.205

        -------------------------
        Device ID: R9
        Entry address(es):
        IP address: 172.16.1.206
        Platform: Cisco ,  Capabilities: Router Source-Route-Bridge
        Interface: GigabitEthernet0/0,  Port ID (outgoing port): GigabitEthernet0/0
        Holdtime : 151 sec

        Version :
        Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.7(3)M3, RELEASE SOFTWARE (fc2)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Wed 01-Aug-18 16:45 by prod_rel_team

        advertisement version: 2
        Management address(es):
        IP address: 172.16.1.206

        Total cdp entries displayed : 2
        """
    }]

    ShowEnvAll = QDict({
        'switch': {
            "1": {
                'fan': {
                    "1": {
                        'state': 'ok'
                    },
                    "2": {
                        'state': 'ok'
                    },
                    "3": {
                        'state': 'ok'
                    }
                },
                'power_supply': {
                    "1": {
                        'state': 'ok',
                        'temperature': 'ok',
                        'pid': 'PWR-C2-1025WAC',
                        'serial_number': 'DCB1636C003',
                        'status': 'ok',
                        'system_power': 'good',
                        'poe_power': 'good',
                        'watts': '250/775'
                    },
                    "2": {
                        'status': 'not present',
                        'temperature': 'not present',
                        'state': 'not present'
                    }
                },
                'system_temperature_state': 'ok',
                'system_temperature': {
                    'value': "41",
                    'state': 'green',
                    'yellow_threshold': "66",
                    'red_threshold': "76"
                },
                'redundant_power_system': {
                    '<>': {
                        'status': 'not present'
                    }
                }
            }
        }
    })
    ShowEnvAll.raw_output = [{
        'command': 'show env all',
        'output': """
        Switch 1 FAN 1 is OK
        Switch 1 FAN 2 is OK
        Switch 1 FAN 3 is OK
        FAN PS-1 is OK
        FAN PS-2 is NOT PRESENT
        SYSTEM TEMPERATURE is OK
        System Temperature Value: 41 Degree Celsius
        System Temperature State: GREEN
        Yellow Threshold : 66 Degree Celsius
        Red Threshold    : 76 Degree Celsius
        POWER SUPPLY 1A TEMPERATURE: OK
        POWER SUPPLY 1B TEMPERATURE: Not Present
        SW   PID                 Serial#     Status           Sys Pwr  PoE Pwr  Watts
        ---  ------------------  ----------  ---------------  -------  -------  -----
        1A   PWR-C2-1025WAC      DCB1636C003 OK               Good     Good     250/775
        1B   Not Present
        SW   Status          RPS Name          RPS Serial#  RPS Port#
        --   -------------   ----------------  -----------  ---------
        1    Not Present     <>
        """
    }]

    ShowLldpNeighborsDetail = QDict({
        "interfaces": {
            "GigabitEthernet2/0/15": {
                "if_name": "GigabitEthernet2/0/15",
                "port_id": {
                    "GigabitEthernet1/0/4": {
                        "neighbors": {
                            "R5": {
                                "neighbor_id": "R5",
                                "chassis_id": "843d.c6ff.f1b8",
                                "port_id": "GigabitEthernet1/0/4",
                                "port_description": "GigabitEthernet1/0/4",
                                "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                                "system_name": "R5",
                                "time_remaining": 112,
                                "capabilities": {
                                    "mac_bridge": {
                                        "name": "mac_bridge",
                                        "system": True,
                                        "enabled": True,
                                    },
                                    "router": {
                                        "name": "router",
                                        "system": True,
                                        "enabled": True,
                                    },
                                },
                                "management_address": "10.9.1.1",
                                "auto_negotiation": "supported, enabled",
                                "physical_media_capabilities": [
                                    "1000baseT(FD)",
                                    "100base-TX(FD)",
                                    "100base-TX(HD)",
                                    "10base-T(FD)",
                                    "10base-T(HD)",
                                ],
                                "unit_type": 30,
                                "vlan_id": 1,
                            }
                        }
                    }
                },
            },
            "GigabitEthernet1/0/16": {
                "if_name": "GigabitEthernet1/0/16",
                "port_id": {
                    "GigabitEthernet1/0/2": {
                        "neighbors": {
                            "R5": {
                                "neighbor_id": "R5",
                                "chassis_id": "843d.c6ff.f1b8",
                                "port_id": "GigabitEthernet1/0/2",
                                "port_description": "GigabitEthernet1/0/2",
                                "system_name": "R5",
                                "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                                "time_remaining": 111,
                                "capabilities": {
                                    "mac_bridge": {
                                        "name": "mac_bridge",
                                        "system": True,
                                        "enabled": True,
                                    },
                                    "router": {
                                        "name": "router",
                                        "system": True,
                                        "enabled": True,
                                    },
                                },
                                "management_address": "10.9.1.1",
                                "auto_negotiation": "supported, enabled",
                                "physical_media_capabilities": [
                                    "1000baseT(FD)",
                                    "100base-TX(FD)",
                                    "100base-TX(HD)",
                                    "10base-T(FD)",
                                    "10base-T(HD)",
                                ],
                                "unit_type": 30,
                                "vlan_id": 1,
                            }
                        }
                    }
                },
            },
            "GigabitEthernet1/0/17": {
                "if_name": "GigabitEthernet1/0/17",
                "port_id": {
                    "GigabitEthernet1/0/3": {
                        "neighbors": {
                            "R5": {
                                "neighbor_id": "R5",
                                "chassis_id": "843d.c6ff.f1b8",
                                "port_id": "GigabitEthernet1/0/3",
                                "port_description": "GigabitEthernet1/0/3",
                                "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                                "system_name": "R5",
                                "time_remaining": 108,
                                "capabilities": {
                                    "mac_bridge": {
                                        "name": "mac_bridge",
                                        "system": True,
                                        "enabled": True,
                                    },
                                    "router": {
                                        "name": "router",
                                        "system": True,
                                        "enabled": True,
                                    },
                                },
                                "management_address": "10.9.1.1",
                                "auto_negotiation": "supported, enabled",
                                "physical_media_capabilities": [
                                    "1000baseT(FD)",
                                    "100base-TX(FD)",
                                    "100base-TX(HD)",
                                    "10base-T(FD)",
                                    "10base-T(HD)",
                                ],
                                "unit_type": 30,
                                "vlan_id": 1,
                            }
                        }
                    }
                },
            },
            "GigabitEthernet1/0/15": {
                "if_name": "GigabitEthernet1/0/15",
                "port_id": {
                    "GigabitEthernet1/0/1": {
                        "neighbors": {
                            "R5": {
                                "neighbor_id": "R5",
                                "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                                "chassis_id": "843d.c6ff.f1b8",
                                "port_id": "GigabitEthernet1/0/1",
                                "port_description": "GigabitEthernet1/0/1",
                                "system_name": "R5",
                                "time_remaining": 108,
                                "capabilities": {
                                    "mac_bridge": {
                                        "name": "mac_bridge",
                                        "system": True,
                                        "enabled": True,
                                    },
                                    "router": {
                                        "name": "router",
                                        "system": True,
                                        "enabled": True,
                                    },
                                },
                                "management_address": "10.9.1.1",
                                "auto_negotiation": "supported, enabled",
                                "physical_media_capabilities": [
                                    "1000baseT(FD)",
                                    "100base-TX(FD)",
                                    "100base-TX(HD)",
                                    "10base-T(FD)",
                                    "10base-T(HD)",
                                ],
                                "unit_type": 30,
                                "vlan_id": 1,
                            }
                        }
                    }
                },
            },
        },
        "total_entries": 4,
    })
    ShowLldpNeighborsDetail.raw_output = [{
        'command': 'show lldp neighbors detail',
        'output': """
        Capability codes:
            (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
            (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
        ------------------------------------------------
        Local Intf: Gi2/0/15
        Chassis id: 843d.c6ff.f1b8
        Port id: Gi1/0/4
        Port Description: GigabitEthernet1/0/4
        System Name: R5

        System Description: 
        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2011 by Cisco Systems, Inc.
        Compiled Thu 21-Jul-11 01:23 by prod_rel_team

        Time remaining: 112 seconds
        System Capabilities: B,R
        Enabled Capabilities: B,R
        Management Addresses:
            IP: 10.9.1.1
        Auto Negotiation - supported, enabled
        Physical media capabilities:
            1000baseT(FD)
            100base-TX(FD)
            100base-TX(HD)
            10base-T(FD)
            10base-T(HD)
        Media Attachment Unit type: 30
        Vlan ID: 1

        ------------------------------------------------
        Local Intf: Gi1/0/16
        Chassis id: 843d.c6ff.f1b8
        Port id: Gi1/0/2
        Port Description: GigabitEthernet1/0/2
        System Name: R5

        System Description: 
        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2011 by Cisco Systems, Inc.
        Compiled Thu 21-Jul-11 01:23 by prod_rel_team

        Time remaining: 111 seconds
        System Capabilities: B,R
        Enabled Capabilities: B,R
        Management Addresses:
            IP: 10.9.1.1
        Auto Negotiation - supported, enabled
        Physical media capabilities:
            1000baseT(FD)
            100base-TX(FD)
            100base-TX(HD)
            10base-T(FD)
            10base-T(HD)
        Media Attachment Unit type: 30
        Vlan ID: 1

        ------------------------------------------------
        Local Intf: Gi1/0/17
        Chassis id: 843d.c6ff.f1b8
        Port id: Gi1/0/3
        Port Description: GigabitEthernet1/0/3
        System Name: R5

        System Description: 
        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2011 by Cisco Systems, Inc.
        Compiled Thu 21-Jul-11 01:23 by prod_rel_team

        Time remaining: 108 seconds
        System Capabilities: B,R
        Enabled Capabilities: B,R
        Management Addresses:
            IP: 10.9.1.1
        Auto Negotiation - supported, enabled
        Physical media capabilities:
            1000baseT(FD)
            100base-TX(FD)
            100base-TX(HD)
            10base-T(FD)
            10base-T(HD)
        Media Attachment Unit type: 30
        Vlan ID: 1

        ------------------------------------------------
        Local Intf: Gi1/0/15
        Chassis id: 843d.c6ff.f1b8
        Port id: Gi1/0/1
        Port Description: GigabitEthernet1/0/1
        System Name: R5

        System Description: 
        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2011 by Cisco Systems, Inc.
        Compiled Thu 21-Jul-11 01:23 by prod_rel_team

        Time remaining: 108 seconds
        System Capabilities: B,R
        Enabled Capabilities: B,R
        Management Addresses:
            IP: 10.9.1.1
        Auto Negotiation - supported, enabled
        Physical media capabilities:
            1000baseT(FD)
            100base-TX(FD)
            100base-TX(HD)
            10base-T(FD)
            10base-T(HD)
        Media Attachment Unit type: 30
        Vlan ID: 1


        Total entries displayed: 4
        """
    }]

    ShowMacAddressTable = QDict({
        "mac_table": {
            "vlans": {
                "100": {
                    "mac_addresses": {
                        "11aa.22ff.ee88": {
                            "interfaces": {
                                "Router": {
                                    "entry": "*",
                                    "interface": "Router",
                                    "entry_type": "static",
                                    "learn": "No",
                                }
                            },
                            "mac_address": "11aa.22ff.ee88",
                        }
                    },
                    "vlan": 100,
                },
                "101": {
                    "mac_addresses": {
                        "44dd.eeff.55bb": {
                            "interfaces": {
                                "GigabitEthernet1/40": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/40",
                                    "entry_type": "dynamic",
                                    "learn": "Yes",
                                    "age": 10,
                                }
                            },
                            "mac_address": "44dd.eeff.55bb",
                        }
                    },
                    "vlan": 101,
                },
                "102": {
                    "mac_addresses": {
                        "aa11.bbff.ee55": {
                            "interfaces": {
                                "GigabitEthernet1/2": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/2",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/4": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/4",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/5": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/5",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/6": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/6",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/9": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/9",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/10": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/10",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/11": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/11",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "GigabitEthernet1/12": {
                                    "entry": "*",
                                    "interface": "GigabitEthernet1/12",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "Router": {
                                    "entry": "*",
                                    "interface": "Router",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "Switch": {
                                    "entry": "*",
                                    "interface": "Switch",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                            },
                            "mac_address": "aa11.bbff.ee55",
                        }
                    },
                    "vlan": 102,
                },
                "200": {
                    "mac_addresses": {
                        "dd44.55ff.55ee": {
                            "interfaces": {
                                "TenGigabitEthernet1/1": {
                                    "entry": "*",
                                    "interface": "TenGigabitEthernet1/1",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "TenGigabitEthernet1/2": {
                                    "entry": "*",
                                    "interface": "TenGigabitEthernet1/2",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "TenGigabitEthernet1/4": {
                                    "entry": "*",
                                    "interface": "TenGigabitEthernet1/4",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                                "TenGigabitEthernet1/8": {
                                    "entry": "*",
                                    "interface": "TenGigabitEthernet1/8",
                                    "entry_type": "static",
                                    "learn": "Yes",
                                },
                            },
                            "mac_address": "dd44.55ff.55ee",
                        }
                    },
                    "vlan": 200,
                },
                "300": {
                    "mac_addresses": {
                        "11aa.22ff.ee88": {
                            "interfaces": {
                                "Router": {
                                    "interface": "Router",
                                    "entry_type": "static",
                                    "learn": "No",
                                }
                            },
                            "mac_address": "11aa.22ff.ee88",
                        }
                    },
                    "vlan": 300,
                },
                "301": {
                    "mac_addresses": {
                        "11aa.22ff.ee88": {
                            "drop": {"drop": True, "entry_type": "static"},
                            "mac_address": "11aa.22ff.ee88",
                        }
                    },
                    "vlan": 301,
                },
                "---": {
                    "mac_addresses": {
                        "0000.0000.0000": {
                            "interfaces": {
                                "Router": {
                                    "entry": "*",
                                    "interface": "Router",
                                    "entry_type": "static",
                                    "learn": "No",
                                }
                            },
                            "mac_address": "0000.0000.0000",
                        }
                    },
                    "vlan": "---",
                },
                "400": {
                    "mac_addresses": {
                        "0000.0000.0000": {
                            "interfaces": {
                                "vPC Peer-Link": {
                                    "entry": "*",
                                    "interface": "vPC Peer-Link",
                                    "entry_type": "static",
                                    "learn": "No",
                                },
                                "Router": {
                                    "entry": "*",
                                    "interface": "Router",
                                    "entry_type": "static",
                                    "learn": "No",
                                },
                            },
                            "mac_address": "0000.0000.0000",
                        }
                    },
                    "vlan": 400,
                },
            }
        },
        "total_mac_addresses": 8,
    })
    ShowMacAddressTable.raw_output = [{
        'command': 'show mac address-table', 
        'output': """
        Legend: * - primary entry
                age - seconds since last seen
                n/a - not available

        vlan   mac address     type    learn     age              ports
        ------+----------------+--------+-----+----------+--------------------------
        *  100  11aa.22ff.ee88    static  No           -   Router
        *  101  44dd.eeff.55bb   dynamic  Yes         10   Gi1/40
        *  102  aa11.bbff.ee55    static  Yes          -   Gi1/2,Gi1/4,Gi1/5,Gi1/6
                                                        Gi1/9,Gi1/10,Gi1/11,Gi1/12
                                                        Router,Switch
        *  200  dd44.55ff.55ee    static  Yes          -   Te1/1,Te1/2,Te1/4,Te1/8
        300  11aa.22ff.ee88    static  No           -   Router
        301  11aa.22ff.ee88    static  No           -   Drop
        *  ---  0000.0000.0000    static  No           -   Router
        *  400  0000.0000.0000    static  No           -   vPC Peer-Link
                                                        Router
                                                            
                Total Mac Addresses for this criterion: 8
        """
    }]

    ShowInterfaces = QDict({
        "GigabitEthernet1/0/2": {
            "arp_timeout": "04:00:00",
            "arp_type": "arpa",
            "bandwidth": 1000000,
            "connected": False,
            "counters": {
                "in_broadcast_pkts": 831,
                "in_crc_errors": 0,
                "in_errors": 0,
                "in_frame": 0,
                "in_giants": 0,
                "in_ignored": 0,
                "in_mac_pause_frames": 0,
                "in_multicast_pkts": 830,
                "in_no_buffer": 0,
                "in_octets": 80868,
                "in_overrun": 0,
                "in_pkts": 972,
                "in_runts": 0,
                "in_throttles": 0,
                "in_watchdog": 0,
                "in_with_dribble": 0,
                "last_clear": "never",
                "out_babble": 0,
                "out_broadcast_pkts": 0,
                "out_buffer_failure": 0,
                "out_buffers_swapped": 0,
                "out_collision": 0,
                "out_deferred": 0,
                "out_errors": 0,
                "out_interface_resets": 2,
                "out_late_collision": 0,
                "out_lost_carrier": 0,
                "out_mac_pause_frames": 0,
                "out_multicast_pkts": 55,
                "out_no_carrier": 0,
                "out_octets": 7040,
                "out_pkts": 55,
                "out_underruns": 0,
                "out_unknown_protocl_drops": 49,
                "rate": {
                    "in_rate": 0,
                    "in_rate_pkts": 0,
                    "load_interval": 300,
                    "out_rate": 0,
                    "out_rate_pkts": 0
                }
            },
            "delay": 10,
            "description": "test",
            "duplex_mode": "full",
            "enabled": True,
            "encapsulations": {
                "encapsulation": "arpa"
            },
            "err_disabled": False,
            "flow_control": {
                "receive": True,
                "send": False
            },
            "keepalive": 10,
            "last_input": "00:00:00",
            "last_output": "00:00:07",
            "line_protocol": "down",
            "mac_address": "643a.eaaa.4402",
            "media_type": "10/100/1000BaseTX",
            "mtu": 1500,
            "oper_status": "down",
            "output_hang": "never",
            "phys_address": "643a.eaaa.4402",
            "port_channel": {
                "port_channel_member": False
            },
            "port_speed": "1000mb/s",
            "queues": {
                "input_queue_drops": 0,
                "input_queue_flushes": 0,
                "input_queue_max": 2000,
                "input_queue_size": 0,
                "output_queue_max": 40,
                "output_queue_size": 0,
                "queue_strategy": "fifo",
                "total_output_drop": 0
            },
            "reliability": "255/255",
            "rxload": "1/255",
            "suspended": True,
            "txload": "1/255",
            "type": "Gigabit Ethernet"
        }
    })
    ShowInterfaces.raw_output = [{
        'command': 'show interfaces',
        'output': """
        GigabitEthernet1/0/2 is up, line protocol is down (suspended)
        Hardware is Gigabit Ethernet, address is 643a.eaaa.4402 (bia 643a.eaaa.4402)
        Description: test
        MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
            reliability 255/255, txload 1/255, rxload 1/255
        Encapsulation ARPA, loopback not set
        Keepalive set (10 sec)
        Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
        input flow-control is on, output flow-control is unsupported
        ARP type: ARPA, ARP Timeout 04:00:00
        Last input 00:00:00, output 00:00:07, output hang never
        Last clearing of "show interface" counters never
        Input queue: 0/2000/0/0 (size/max/drops/flushes); Total output drops: 0
        Queueing strategy: fifo
        Output queue: 0/40 (size/max)
        5 minute input rate 0 bits/sec, 0 packets/sec
        5 minute output rate 0 bits/sec, 0 packets/sec
            972 packets input, 80868 bytes, 0 no buffer
            Received 831 broadcasts (830 multicasts)
            0 runts, 0 giants, 0 throttles
            0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
            0 watchdog, 830 multicast, 0 pause input
            0 input packets with dribble condition detected
            55 packets output, 7040 bytes, 0 underruns
            Output 0 broadcasts (55 multicasts)
            0 output errors, 0 collisions, 2 interface resets
            49 unknown protocol drops
            0 babbles, 0 late collision, 0 deferred
            0 lost carrier, 0 no carrier, 0 pause output
            0 output buffer failures, 0 output buffers swapped out
        """
    }]

    ShowInventoryRaw = QDict({
        "name": {
            "Gi2/0/1": {
                "description": "Gi2/0/1"
            },
            "Switch 3": {
                "description": "C9300-48U - Provisioned",
                "pid": "C9300-48U"
            },
            "Twe2/1/1 Container": {
                "description": "Twe2/1/1 Container",
                "pid": "UnknownPID"
            },
            "usbflash1": {
                "description": "usbflash1-2",
                "pid": "SSD-120G",
                "sn": "1234",
                "vid": "3.10"
            }
        }
    })
    ShowInventoryRaw.raw_output = [{
        'command': 'show inventory raw',
        'output': """
        NAME: "Gi2/0/1", DESCR: "Gi2/0/1"
        PID:                   , VID:      , SN:

        NAME: "Switch 3", DESCR: "C9300-48U - Provisioned"
        PID: C9300-48U         , VID:      , SN:

        NAME: "Twe2/1/1 Container", DESCR: "Twe2/1/1 Container"
        PID: Unknown PID       , VID:      , SN:

        NAME: "usbflash1", DESCR: "usbflash1-2"
        PID: SSD-120G          , VID: 3.10 , SN: 1234
        """
    }]

    ShowPowerInline = QDict({
        "watts": {
            "0": {
                "module": "0", 
                "available": 1170.0, 
                "used": 212.2, 
                "remaining": 957.8}
        },
        "interface": {
            "GigabitEthernet0/1": {
                "power": 0.0,
                "max": 30.0,
                "admin_state": "auto",
                "oper_state": "off",
            },
            "GigabitEthernet0/2": {
                "power": 6.4,
                "max": 30.0,
                "admin_state": "auto",
                "oper_state": "on",
                "device": "IP Phone 8945",
                "class": "2",
            },
            "GigabitEthernet0/3": {
                "power": 6.4,
                "max": 30.0,
                "admin_state": "auto",
                "oper_state": "on",
                "device": "IP Phone 8845",
                "class": "2",
            },
            "GigabitEthernet0/4": {
                "power": 0.0,
                "max": 30.0,
                "admin_state": "auto",
                "oper_state": "off",
            }
        }
    })
    ShowPowerInline.raw_output = [{
        'command': 'show power inline',
        'output': """
        Available:1170.0(w)  Used:212.2(w)  Remaining:957.8(w)
        
        Interface Admin  Oper       Power   Device              Class Max
                                    (Watts)                            
        --------- ------ ---------- ------- ------------------- ----- ----
        Gi0/1     auto   off        0.0     n/a                 n/a   30.0 
        Gi0/2     auto   on         6.4     IP Phone 8945       2     30.0 
        Gi0/3     auto   on         6.4     IP Phone 8845       2     30.0 
        Gi0/4     auto   off        0.0     n/a                 n/a   30.0 
        """
    }]

    ShowRunningConfig = {
        'config': "Building configuration..."
    }

    ShowVersion = QDict({
        'version': {
            'xe_version': '17.03.01a',
            'version_short': '17.3',
            'platform': 'Virtual XE',
            'version': '17.3.1a',
            'image_id': 'X86_64_LINUX_IOSD-UNIVERSALK9-M',
            'label': 'RELEASE SOFTWARE (fc3)',
            'os': 'IOS-XE',
            'location': 'Amsterdam',
            'image_type': 'production image',
            'copyright_years': '1986-2020',
            'compiled_date': 'Wed 12-Aug-20 00:16',
            'compiled_by': 'mcpre',
            'rom': 'IOS-XE ROMMON',
            'hostname': 'R1_xe',
            'uptime': '2 days, 23 hours, 10 minutes',
            'uptime_this_cp': '2 days, 23 hours, 13 minutes',
            'returned_to_rom_by': 'reload',
            'system_image': 'bootflash:packages.conf',
            'last_reload_reason': 'factory-reset',
            'license_level': 'ax',
            'license_type': 'N/A(Smart License Enabled)',
            'next_reload_license_level': 'ax',
            'chassis': 'CSR1000V',
            'main_mem': '715705',
            'processor_type': 'VXE',
            'rtr_type': 'CSR1000V',
            'chassis_sn': '9NKCL6JO519',
            'router_operating_mode': 'Autonomous',
            'number_of_intfs': {'Gigabit Ethernet': '7'},
            'mem_size': {'non-volatile configuration': '32768', 'physical': '3012224'},
            'disks': {
                'bootflash:.': {
                    'disk_size': '6188032', 'type_of_disk': 'virtual hard disk'
                }
            },
            'curr_config_register': '0x2102'
        }
    })
    ShowVersion.raw_output = [{
        'command': 'show version',
        'output': """
        Cisco IOS XE Software, Version 17.03.01a
        Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.1a, RELEASE SOFTWARE (fc3)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2020 by Cisco Systems, Inc.
        Compiled Wed 12-Aug-20 00:16 by mcpre


        Cisco IOS-XE software, Copyright (c) 2005-2020 by cisco Systems, Inc.
        All rights reserved.  Certain components of Cisco IOS-XE software are
        licensed under the GNU General Public License ("GPL") Version 2.0.  The
        software code licensed under GPL Version 2.0 is free software that comes
        with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
        GPL code under the terms of GPL Version 2.0.  For more details, see the
        documentation or "License Notice" file accompanying the IOS-XE software,
        or the applicable URL provided on the flyer accompanying the IOS-XE
        software.


        ROM: IOS-XE ROMMON

        R1_xe uptime is 2 days, 23 hours, 10 minutes
        Uptime for this control processor is 2 days, 23 hours, 13 minutes
        System returned to ROM by reload
        System image file is "bootflash:packages.conf"
        Last reload reason: factory-reset



        This product contains cryptographic features and is subject to United
        States and local country laws governing import, export, transfer and
        use. Delivery of Cisco cryptographic products does not imply
        third-party authority to import, export, distribute or use encryption.
        Importers, exporters, distributors and users are responsible for
        compliance with U.S. and local country laws. By using this product you
        agree to comply with applicable laws and regulations. If you are unable
        to comply with U.S. and local laws, return this product immediately.

        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.

        License Level: ax
        License Type: N/A(Smart License Enabled)
        Next reload license Level: ax

        The current throughput level is 1000 kbps


        Smart Licensing Status: UNREGISTERED/No Licenses in Use

        cisco CSR1000V (VXE) processor (revision VXE) with 715705K/3075K bytes of memory.
        Processor board ID 9NKCL6JO519
        Router operating mode: Autonomous
        7 Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        3012224K bytes of physical memory.
        6188032K bytes of virtual hard disk at bootflash:.

        Configuration register is 0x2102
        """
    }]

    # Device Info Structure
    DeviceInfo = {
        'bootvar': {
            'boot_mode': 'device',
            'current_boot_variable': 'flash:packages.conf;',
            'enable_break': False,
            'ipxe_timeout': 0,
            'manual_boot': False,
            'next_reload_boot_variable': 'flash:packages.conf;',
            'raw_data': {
                'show boot': """
        ---------------------------
        Switch 2
        ---------------------------
        Current Boot Variables:
        BOOT variable = flash:packages.conf;

        Boot Variables on next reload:
        BOOT variable = flash:packages.conf;
        Manual Boot = no
        Enable Break = no
        Boot Mode = DEVICE
        iPXE Timeout = 0
        """
            }
        },
        'version': {
            'os': 'iosxe',
            'platform': '',
            'version': '17.3.1a',
            'built_by': 'mcpre',
            'system_image': 'bootflash:packages.conf',
            'built_date': '2020-08-12T00:16:00',
            'raw_data': {
                'show version': '\n        Cisco IOS XE Software, Version 17.03.01a\n        Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.1a, RELEASE SOFTWARE (fc3)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2020 by Cisco Systems, Inc.\n        Compiled Wed 12-Aug-20 00:16 by mcpre\n\n\n        Cisco IOS-XE software, Copyright (c) 2005-2020 by cisco Systems, Inc.\n        All rights reserved.  Certain components of Cisco IOS-XE software are\n        licensed under the GNU General Public License ("GPL") Version 2.0.  The\n        software code licensed under GPL Version 2.0 is free software that comes\n        with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such\n        GPL code under the terms of GPL Version 2.0.  For more details, see the\n        documentation or "License Notice" file accompanying the IOS-XE software,\n        or the applicable URL provided on the flyer accompanying the IOS-XE\n        software.\n\n\n        ROM: IOS-XE ROMMON\n\n        R1_xe uptime is 2 days, 23 hours, 10 minutes\n        Uptime for this control processor is 2 days, 23 hours, 13 minutes\n        System returned to ROM by reload\n        System image file is "bootflash:packages.conf"\n        Last reload reason: factory-reset\n\n\n\n        This product contains cryptographic features and is subject to United\n        States and local country laws governing import, export, transfer and\n        use. Delivery of Cisco cryptographic products does not imply\n        third-party authority to import, export, distribute or use encryption.\n        Importers, exporters, distributors and users are responsible for\n        compliance with U.S. and local country laws. By using this product you\n        agree to comply with applicable laws and regulations. If you are unable\n        to comply with U.S. and local laws, return this product immediately.\n\n        A summary of U.S. laws governing Cisco cryptographic products may be found at:\n        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n\n        If you require further assistance please contact us by sending email to\n        export@cisco.com.\n\n        License Level: ax\n        License Type: N/A(Smart License Enabled)\n        Next reload license Level: ax\n\n        The current throughput level is 1000 kbps\n\n\n        Smart Licensing Status: UNREGISTERED/No Licenses in Use\n\n        cisco CSR1000V (VXE) processor (revision VXE) with 715705K/3075K bytes of memory.\n        Processor board ID 9NKCL6JO519\n        Router operating mode: Autonomous\n        7 Gigabit Ethernet interfaces\n        32768K bytes of non-volatile configuration memory.\n        3012224K bytes of physical memory.\n        6188032K bytes of virtual hard disk at bootflash:.\n\n        Configuration register is 0x2102\n        '
            }
        },
        'environment': {
            '1': {
                'fans': {
                    '1': {'status': 'ok', 'healthy': True},
                    '2': {'status': 'ok', 'healthy': True},
                    '3': {'status': 'ok', 'healthy': True}
                },
                'power_supply': {
                    '1': {'status': 'ok', 'healthy': True},
                    '2': {'status': 'not present', 'healthy': True}
                },
                'temperature': {
                    'status': 'green',
                    'current_temp_celsius': 41,
                    'healthy': True
                }
            },
            'raw_data': {
                'show env all': '\n        Switch 1 FAN 1 is OK\n        Switch 1 FAN 2 is OK\n        Switch 1 FAN 3 is OK\n        FAN PS-1 is OK\n        FAN PS-2 is NOT PRESENT\n        SYSTEM TEMPERATURE is OK\n        System Temperature Value: 41 Degree Celsius\n        System Temperature State: GREEN\n        Yellow Threshold : 66 Degree Celsius\n        Red Threshold    : 76 Degree Celsius\n        POWER SUPPLY 1A TEMPERATURE: OK\n        POWER SUPPLY 1B TEMPERATURE: Not Present\n        SW   PID                 Serial#     Status           Sys Pwr  PoE Pwr  Watts\n        ---  ------------------  ----------  ---------------  -------  -------  -----\n        1A   PWR-C2-1025WAC      DCB1636C003 OK               Good     Good     250/775\n        1B   Not Present\n        SW   Status          RPS Name          RPS Serial#  RPS Port#\n        --   -------------   ----------------  -----------  ---------\n        1    Not Present     <>\n        '
            }
        },
        'interfaces': {
            'GigabitEthernet1/0/2': {
                'enabled': True,
                'mac_address': '643a.eaaa.4402',
                'media_type': '10/100/1000BaseTX',
                'mtu': 1500,
                'duplex': 'full',
                'status': 'down',
                'speed': '1000',
                'speed_unit': 'Mb/s',
                'line_protocol': False
            },
            'raw_data': {
                'show interfaces': '\n        GigabitEthernet1/0/2 is up, line protocol is down (suspended)\n        Hardware is Gigabit Ethernet, address is 643a.eaaa.4402 (bia 643a.eaaa.4402)\n        Description: test\n        MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,\n            reliability 255/255, txload 1/255, rxload 1/255\n        Encapsulation ARPA, loopback not set\n        Keepalive set (10 sec)\n        Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX\n        input flow-control is on, output flow-control is unsupported\n        ARP type: ARPA, ARP Timeout 04:00:00\n        Last input 00:00:00, output 00:00:07, output hang never\n        Last clearing of "show interface" counters never\n        Input queue: 0/2000/0/0 (size/max/drops/flushes); Total output drops: 0\n        Queueing strategy: fifo\n        Output queue: 0/40 (size/max)\n        5 minute input rate 0 bits/sec, 0 packets/sec\n        5 minute output rate 0 bits/sec, 0 packets/sec\n            972 packets input, 80868 bytes, 0 no buffer\n            Received 831 broadcasts (830 multicasts)\n            0 runts, 0 giants, 0 throttles\n            0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored\n            0 watchdog, 830 multicast, 0 pause input\n            0 input packets with dribble condition detected\n            55 packets output, 7040 bytes, 0 underruns\n            Output 0 broadcasts (55 multicasts)\n            0 output errors, 0 collisions, 2 interface resets\n            49 unknown protocol drops\n            0 babbles, 0 late collision, 0 deferred\n            0 lost carrier, 0 no carrier, 0 pause output\n            0 output buffer failures, 0 output buffers swapped out\n        '
            }
        },
        'neighbors': {
            '1': {
                'name': 'R9',
                'local_interface': 'GigabitEthernet0/0',
                'interface': 'GigabitEthernet0/0',
                'addresses': ['172.16.1.206']
            },
            '2': {
                'name': 'R8',
                'local_interface': 'GigabitEthernet0/0',
                'interface': 'GigabitEthernet0/0',
                'addresses': ['172.16.1.205']
            },
            '3': {
                'name': 'R5',
                'interface': 'GigabitEthernet1/0/1'
            },
            'raw_data': {
                'show cdp neighbors detail': '\n        Device ID: R8\n        Entry address(es):\n        IP address: 172.16.1.205\n        Platform: Cisco ,  Capabilities: Router Source-Route-Bridge\n        Interface: GigabitEthernet0/0,  Port ID (outgoing port): GigabitEthernet0/0\n        Holdtime : 143 sec\n\n        Version :\n        Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.7(3)M3, RELEASE SOFTWARE (fc2)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2018 by Cisco Systems, Inc.\n        Compiled Wed 01-Aug-18 16:45 by prod_rel_team\n\n        advertisement version: 2\n        Management address(es):\n        IP address: 172.16.1.205\n\n        -------------------------\n        Device ID: R9\n        Entry address(es):\n        IP address: 172.16.1.206\n        Platform: Cisco ,  Capabilities: Router Source-Route-Bridge\n        Interface: GigabitEthernet0/0,  Port ID (outgoing port): GigabitEthernet0/0\n        Holdtime : 151 sec\n\n        Version :\n        Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.7(3)M3, RELEASE SOFTWARE (fc2)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2018 by Cisco Systems, Inc.\n        Compiled Wed 01-Aug-18 16:45 by prod_rel_team\n\n        advertisement version: 2\n        Management address(es):\n        IP address: 172.16.1.206\n\n        Total cdp entries displayed : 2\n        ', 'show lldp neighbors detail': '\n        Capability codes:\n            (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device\n            (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other\n        ------------------------------------------------\n        Local Intf: Gi2/0/15\n        Chassis id: 843d.c6ff.f1b8\n        Port id: Gi1/0/4\n        Port Description: GigabitEthernet1/0/4\n        System Name: R5\n\n        System Description: \n        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2011 by Cisco Systems, Inc.\n        Compiled Thu 21-Jul-11 01:23 by prod_rel_team\n\n        Time remaining: 112 seconds\n        System Capabilities: B,R\n        Enabled Capabilities: B,R\n        Management Addresses:\n            IP: 10.9.1.1\n        Auto Negotiation - supported, enabled\n        Physical media capabilities:\n            1000baseT(FD)\n            100base-TX(FD)\n            100base-TX(HD)\n            10base-T(FD)\n            10base-T(HD)\n        Media Attachment Unit type: 30\n        Vlan ID: 1\n\n        ------------------------------------------------\n        Local Intf: Gi1/0/16\n        Chassis id: 843d.c6ff.f1b8\n        Port id: Gi1/0/2\n        Port Description: GigabitEthernet1/0/2\n        System Name: R5\n\n        System Description: \n        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2011 by Cisco Systems, Inc.\n        Compiled Thu 21-Jul-11 01:23 by prod_rel_team\n\n        Time remaining: 111 seconds\n        System Capabilities: B,R\n        Enabled Capabilities: B,R\n        Management Addresses:\n            IP: 10.9.1.1\n        Auto Negotiation - supported, enabled\n        Physical media capabilities:\n            1000baseT(FD)\n            100base-TX(FD)\n            100base-TX(HD)\n            10base-T(FD)\n            10base-T(HD)\n        Media Attachment Unit type: 30\n        Vlan ID: 1\n\n        ------------------------------------------------\n        Local Intf: Gi1/0/17\n        Chassis id: 843d.c6ff.f1b8\n        Port id: Gi1/0/3\n        Port Description: GigabitEthernet1/0/3\n        System Name: R5\n\n        System Description: \n        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2011 by Cisco Systems, Inc.\n        Compiled Thu 21-Jul-11 01:23 by prod_rel_team\n\n        Time remaining: 108 seconds\n        System Capabilities: B,R\n        Enabled Capabilities: B,R\n        Management Addresses:\n            IP: 10.9.1.1\n        Auto Negotiation - supported, enabled\n        Physical media capabilities:\n            1000baseT(FD)\n            100base-TX(FD)\n            100base-TX(HD)\n            10base-T(FD)\n            10base-T(HD)\n        Media Attachment Unit type: 30\n        Vlan ID: 1\n\n        ------------------------------------------------\n        Local Intf: Gi1/0/15\n        Chassis id: 843d.c6ff.f1b8\n        Port id: Gi1/0/1\n        Port Description: GigabitEthernet1/0/1\n        System Name: R5\n\n        System Description: \n        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\n        Technical Support: http://www.cisco.com/techsupport\n        Copyright (c) 1986-2011 by Cisco Systems, Inc.\n        Compiled Thu 21-Jul-11 01:23 by prod_rel_team\n\n        Time remaining: 108 seconds\n        System Capabilities: B,R\n        Enabled Capabilities: B,R\n        Management Addresses:\n            IP: 10.9.1.1\n        Auto Negotiation - supported, enabled\n        Physical media capabilities:\n            1000baseT(FD)\n            100base-TX(FD)\n            100base-TX(HD)\n            10base-T(FD)\n            10base-T(HD)\n        Media Attachment Unit type: 30\n        Vlan ID: 1\n\n\n        Total entries displayed: 4\n        '
            }
        },
        'inventory': {
            '1': {
                'name': 'usbflash1',
                'description': 'usbflash1-2',
                'pid': 'SSD-120G',
                'vid': '3.10',
                'sn': '1234'
            },
            '2': {
                'name': 'Twe2/1/1 Container',
                'description': 'Twe2/1/1 Container',
                'pid': 'UnknownPID'
            },
            '3': {
                'name': 'Switch 3',
                'description': 'C9300-48U - Provisioned',
                'pid': 'C9300-48U'
            },
            '4': {
                'name': 'Gi2/0/1',
                'description': 'Gi2/0/1'
            },
            'raw_data': {
                'show inventory raw': '\n        NAME: "Gi2/0/1", DESCR: "Gi2/0/1"\n        PID:                   , VID:      , SN:\n\n        NAME: "Switch 3", DESCR: "C9300-48U - Provisioned"\n        PID: C9300-48U         , VID:      , SN:\n\n        NAME: "Twe2/1/1 Container", DESCR: "Twe2/1/1 Container"\n        PID: Unknown PID       , VID:      , SN:\n\n        NAME: "usbflash1", DESCR: "usbflash1-2"\n        PID: SSD-120G          , VID: 3.10 , SN: 1234\n        '
            }
        },
        'mac_table': {
            'vlans': {
                '101': {
                    'mac_addresses': {
                        '44dd.eeff.55bb': {
                            'interfaces': {
                                'GigabitEthernet1/40': {
                                    'age': '10',
                                    'type': 'dynamic'
                                }
                            }
                        }
                    }
                },
                '400': {
                    'mac_addresses': {
                        '0000.0000.0000': {
                            'interfaces': {
                                'Router': {'type': 'static'},
                                'vPC Peer-Link': {'type': 'static'}
                            }
                        }
                    }
                },
                '---': {
                    'mac_addresses': {
                        '0000.0000.0000': {
                            'interfaces': {
                                'Router': {'type': 'static'}
                            }
                        }
                    }
                },
                '300': {
                    'mac_addresses': {
                        '11aa.22ff.ee88': {
                            'interfaces': {
                                'Router': {'type': 'static'}
                            }
                        }
                    }
                },
                '200': {
                    'mac_addresses': {
                        'dd44.55ff.55ee': {
                            'interfaces': {
                                'TenGigabitEthernet1/8': {'type': 'static'},
                                'TenGigabitEthernet1/4': {'type': 'static'},
                                'TenGigabitEthernet1/2': {'type': 'static'},
                                'TenGigabitEthernet1/1': {'type': 'static'}
                            }
                        }
                    }
                },
                '102': {
                    'mac_addresses': {
                        'aa11.bbff.ee55': {
                            'interfaces': {
                                'Switch': {'type': 'static'},
                                'Router': {'type': 'static'},
                                'GigabitEthernet1/12': {'type': 'static'},
                                'GigabitEthernet1/11': {'type': 'static'},
                                'GigabitEthernet1/10': {'type': 'static'},
                                'GigabitEthernet1/9': {'type': 'static'},
                                'GigabitEthernet1/6': {'type': 'static'},
                                'GigabitEthernet1/5': {'type': 'static'},
                                'GigabitEthernet1/4': {'type': 'static'},
                                'GigabitEthernet1/2': {'type': 'static'}
                            }
                        }
                    }
                },
                '100': {
                    'mac_addresses': {
                        '11aa.22ff.ee88': {
                            'interfaces': {
                                'Router': {'type': 'static'}
                            }
                        }
                    }
                }
            },
            'raw_data': {
                'show mac address-table': '\n        Legend: * - primary entry\n                age - seconds since last seen\n                n/a - not available\n\n        vlan   mac address     type    learn     age              ports\n        ------+----------------+--------+-----+----------+--------------------------\n        *  100  11aa.22ff.ee88    static  No           -   Router\n        *  101  44dd.eeff.55bb   dynamic  Yes         10   Gi1/40\n        *  102  aa11.bbff.ee55    static  Yes          -   Gi1/2,Gi1/4,Gi1/5,Gi1/6\n                                                        Gi1/9,Gi1/10,Gi1/11,Gi1/12\n                                                        Router,Switch\n        *  200  dd44.55ff.55ee    static  Yes          -   Te1/1,Te1/2,Te1/4,Te1/8\n        300  11aa.22ff.ee88    static  No           -   Router\n        301  11aa.22ff.ee88    static  No           -   Drop\n        *  ---  0000.0000.0000    static  No           -   Router\n        *  400  0000.0000.0000    static  No           -   vPC Peer-Link\n                                                        Router\n                                                            \n                Total Mac Addresses for this criterion: 8\n        '
            }
        },
        'config': {
            'running': 'Building configuration...'
        },
        'power_inline': {
            'interface': {
                'GigabitEthernet0/4': {
                    'admin_state': 'auto',
                    'oper_state': 'off',
                    'power': 0.0,
                    'max': 30.0,
                    'healthy': False
                },
                'GigabitEthernet0/3': {
                    'admin_state': 'auto',
                    'oper_state': 'on',
                    'power': 6.4,
                    'device': 'IP Phone 8845',
                    'class': '2',
                    'max': 30.0,
                    'healthy': True
                },
                'GigabitEthernet0/2': {
                    'admin_state': 'auto',
                    'oper_state': 'on',
                    'power': 6.4,
                    'device': 'IP Phone 8945',
                    'class': '2',
                    'max': 30.0,
                    'healthy': True
                },
                'GigabitEthernet0/1': {
                    'admin_state': 'auto',
                    'oper_state': 'off',
                    'power': 0.0,
                    'max': 30.0,
                    'healthy': False
                }
            },
            'watts': {
                '0': {
                    'module': '0',
                    'available': 1170.0,
                    'used': 212.2,
                    'remaining': 957.8
                }
            },
            'raw_data': {
                'show power inline': '\n        Available:1170.0(w)  Used:212.2(w)  Remaining:957.8(w)\n        \n        Interface Admin  Oper       Power   Device              Class Max\n                                    (Watts)                            \n        --------- ------ ---------- ------- ------------------- ----- ----\n        Gi0/1     auto   off        0.0     n/a                 n/a   30.0 \n        Gi0/2     auto   on         6.4     IP Phone 8945       2     30.0 \n        Gi0/3     auto   on         6.4     IP Phone 8845       2     30.0 \n        Gi0/4     auto   off        0.0     n/a                 n/a   30.0 \n        '
            }
        }
    }