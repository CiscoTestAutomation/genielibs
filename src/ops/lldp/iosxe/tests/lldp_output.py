'''LLDP Genie Ops Object Outputs for IOSXE.'''


class LldpOutput(object):

    ShowLldp = {
        "hello_timer": 30,
        "enabled": True,
        "hold_timer": 120,
        "status": "active",
        "reinit_timer": 2

    }

    ShowLldpNeighborsDetail = {
        "total_entries": 4,
        "interfaces": {
            "GigabitEthernet1/0/15": {
                 "if_name": "GigabitEthernet1/0/15",
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "unit_type": 30,
                           "management_address": "1.2.1.1",
                           "auto_negotiation": "supported, enabled",
                           "physical_media_capabilities": [
                                "1000baseT(FD)",
                                "100base-TX(FD)",
                                "100base-TX(HD)",
                                "10base-T(FD)",
                                "10base-T(HD)"
                           ],
                           "vlan_id": 1,
                           "time_remaining": 108,
                           "system_name": "R5",
                           "neighbor_id": "R5",
                           "port_description": "GigabitEthernet1/0/1",
                           "port_id": "GigabitEthernet1/0/1",
                           "capabilities": {
                                "mac_bridge": {
                                     "system": True,
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "system": True,
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            },
            "GigabitEthernet2/0/15": {
                 "if_name": "GigabitEthernet2/0/15",
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "unit_type": 30,
                           "management_address": "1.2.1.1",
                           "auto_negotiation": "supported, enabled",
                           "physical_media_capabilities": [
                                "1000baseT(FD)",
                                "100base-TX(FD)",
                                "100base-TX(HD)",
                                "10base-T(FD)",
                                "10base-T(HD)"
                           ],
                           "vlan_id": 1,
                           "time_remaining": 112,
                           "system_name": "R5",
                           "neighbor_id": "R5",
                           "port_description": "GigabitEthernet1/0/4",
                           "port_id": "GigabitEthernet1/0/4",
                           "capabilities": {
                                "mac_bridge": {
                                     "system": True,
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "system": True,
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            },
            "GigabitEthernet1/0/17": {
                 "if_name": "GigabitEthernet1/0/17",
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "unit_type": 30,
                           "management_address": "1.2.1.1",
                           "auto_negotiation": "supported, enabled",
                           "physical_media_capabilities": [
                                "1000baseT(FD)",
                                "100base-TX(FD)",
                                "100base-TX(HD)",
                                "10base-T(FD)",
                                "10base-T(HD)"
                           ],
                           "vlan_id": 1,
                           "time_remaining": 108,
                           "system_name": "R5",
                           "neighbor_id": "R5",
                           "port_description": "GigabitEthernet1/0/3",
                           "port_id": "GigabitEthernet1/0/3",
                           "capabilities": {
                                "mac_bridge": {
                                     "system": True,
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "system": True,
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            },
            "GigabitEthernet1/0/16": {
                 "if_name": "GigabitEthernet1/0/16",
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "unit_type": 30,
                           "management_address": "1.2.1.1",
                           "auto_negotiation": "supported, enabled",
                           "physical_media_capabilities": [
                                "1000baseT(FD)",
                                "100base-TX(FD)",
                                "100base-TX(HD)",
                                "10base-T(FD)",
                                "10base-T(HD)"
                           ],
                           "vlan_id": 1,
                           "time_remaining": 111,
                           "system_name": "R5",
                           "neighbor_id": "R5",
                           "port_description": "GigabitEthernet1/0/2",
                           "port_id": "GigabitEthernet1/0/2",
                           "capabilities": {
                                "mac_bridge": {
                                     "system": True,
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "system": True,
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            }
        }
    }

    ShowLldpTraffic = {
        "frame_in": 13315,
        "frame_out": 20372,
        "frame_error_in": 0,
        "frame_discard": 14,
        "tlv_discard": 0,
        'tlv_unknown': 0,
        'entries_aged_out': 34
    }

    ShowLldpInterface = {
        'interfaces': {
            'GigabitEthernet1/0/15': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet1/0/16': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet1/0/17': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet2/0/15': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
        }        
    }

    Lldp_info = {
        "hello_timer": 30,
        "enabled": True,
        "hold_timer": 120,
        "counters": {            
            "frame_in": 13315,
            "frame_out": 20372,
            "frame_error_in": 0,
            "frame_discard": 14,
            "tlv_discard": 0,
            'tlv_unknown': 0,
            'entries_aged_out': 34
        },
        "interfaces": {
            "GigabitEthernet1/0/15": {
                 "if_name": "GigabitEthernet1/0/15",
                 "enabled": True,
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "management_address": "1.2.1.1",
                           "system_name": "R5",
                           "neighbor_id": "R5",
                           "port_description": "GigabitEthernet1/0/1",
                           "port_id": "GigabitEthernet1/0/1",
                           "capabilities": {
                                "mac_bridge": {
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            },
            "GigabitEthernet2/0/15": {
                 "if_name": "GigabitEthernet2/0/15",
                 "enabled": True,
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "management_address": "1.2.1.1",
                           "neighbor_id": "R5",
                           "system_name": "R5",
                           "port_description": "GigabitEthernet1/0/4",
                           "port_id": "GigabitEthernet1/0/4",
                           "capabilities": {
                                "mac_bridge": {
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            },
            "GigabitEthernet1/0/17": {
                 "if_name": "GigabitEthernet1/0/17",
                 "enabled": True,
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "management_address": "1.2.1.1",
                           "neighbor_id": "R5",
                           "system_name": "R5",
                           "port_description": "GigabitEthernet1/0/3",
                           "port_id": "GigabitEthernet1/0/3",
                           "capabilities": {
                                "mac_bridge": {
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            },
            "GigabitEthernet1/0/16": {
                 "if_name": "GigabitEthernet1/0/16",
                 "enabled": True,
                 "neighbors": {
                      "R5": {
                           "chassis_id": "843d.c638.b980",
                           "system_description": "Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\nCompiled Thu 21-Jul-11 01:23 by prod_rel_team",
                           "management_address": "1.2.1.1",
                           "system_name": "R5",
                           "neighbor_id": "R5",
                           "port_description": "GigabitEthernet1/0/2",
                           "port_id": "GigabitEthernet1/0/2",
                           "capabilities": {
                                "mac_bridge": {
                                     "name": "mac_bridge",
                                     "enabled": True
                                },
                                "router": {
                                     "name": "router",
                                     "enabled": True
                                }
                           }
                      }
                 }
            }
        }
    }
