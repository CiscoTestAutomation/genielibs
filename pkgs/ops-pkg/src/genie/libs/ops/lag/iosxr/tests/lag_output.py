'''LAG Genie Ops Object Outputs for IOSXR.'''


class LagOutput(object):

    ShowLacpSystemId = {
        "system_priority": 100,
        "system_id_mac": "00-1b-0c-10-5a-26"
    }

    ShowBundle = {
        "interfaces": {
            "Bundle-Ether1": {
                "name": "Bundle-Ether1",
                "bundle_id": 1,
                "oper_status": "up",
                "local_links": {
                    "active": 2,
                    "standby": 0,
                    "configured": 2
                },
                "local_bandwidth_kbps": {
                    "effective": 2000000,
                    "available": 2000000
                },
                "mac_address": "001b.0c10.5a25",
                "mac_address_source": "Chassis pool",
                "inter_chassis_link": "No",
                "min_active_link": 1,
                "min_active_bw_kbps": 1,
                "max_active_link": 8,
                "wait_while_timer_ms": 2000,
                "load_balance": {
                    "link_order_signaling": "Not configured",
                    "hash_type": "Default",
                    "locality_threshold": "None"
                },
                "lacp": {
                    "lacp": "Operational",
                    "flap_suppression_timer": "Off",
                    "cisco_extensions": "Disabled",
                    "non_revertive": "Disabled"
                },
                "mlacp": {
                    "mlacp": "Not configured"
                },
                "ipv4_bfd": {
                    "ipv4_bfd": "Not configured"
                },
                "ipv6_bfd": {
                    "ipv6_bfd": "Not configured"
                },
                "port": {
                    "GigabitEthernet0/0/0/0": {
                        "interface": "GigabitEthernet0/0/0/0",
                        "device": "Local",
                        "state": "Active",
                        "port_id": "0x000a, 0x0001",
                        "bw_kbps": 1000000,
                        "link_state": "Active"
                    },
                    "GigabitEthernet0/0/0/1": {
                        "interface": "GigabitEthernet0/0/0/1",
                        "device": "Local",
                        "state": "Active",
                        "port_id": "0x8000, 0x0002",
                        "bw_kbps": 1000000,
                        "link_state": "Active"
                    }
                }
            },
            "Bundle-Ether2": {
                "name": "Bundle-Ether2",
                "bundle_id": 2,
                "oper_status": "up",
                "local_links": {
                    "active": 2,
                    "standby": 1,
                    "configured": 3
                },
                "local_bandwidth_kbps": {
                    "effective": 2000000,
                    "available": 2000000
                },
                "mac_address": "001b.0c10.5a24",
                "mac_address_source": "Chassis pool",
                "inter_chassis_link": "No",
                "min_active_link": 2,
                "min_active_bw_kbps": 1,
                "max_active_link": 2,
                "wait_while_timer_ms": 2000,
                "load_balance": {
                    "link_order_signaling": "Not configured",
                    "hash_type": "Default",
                    "locality_threshold": "None"
                },
                "lacp": {
                    "lacp": "Operational",
                    "flap_suppression_timer": "Off",
                    "cisco_extensions": "Disabled",
                    "non_revertive": "Disabled"
                },
                "mlacp": {
                    "mlacp": "Not configured"
                },
                "ipv4_bfd": {
                    "ipv4_bfd": "Not configured"
                },
                "ipv6_bfd": {
                    "ipv6_bfd": "Not configured"
                },
                "port": {
                    "GigabitEthernet0/0/0/2": {
                        "interface": "GigabitEthernet0/0/0/2",
                        "device": "Local",
                        "state": "Standby",
                        "port_id": "0x8000, 0x0005",
                        "bw_kbps": 1000000,
                        "link_state": "Standby due to maximum-active links configuration"
                    },
                    "GigabitEthernet0/0/0/3": {
                        "interface": "GigabitEthernet0/0/0/3",
                        "device": "Local",
                        "state": "Active",
                        "port_id": "0x8000, 0x0004",
                        "bw_kbps": 1000000,
                        "link_state": "Active"
                    },
                    "GigabitEthernet0/0/0/4": {
                        "interface": "GigabitEthernet0/0/0/4",
                        "device": "Local",
                        "state": "Active",
                        "port_id": "0x8000, 0x0003",
                        "bw_kbps": 1000000,
                        "link_state": "Active"
                    }
                }
            }
        }
    }

    ShowLacp = {
        "interfaces": {
            "Bundle-Ether1": {
                "name": "Bundle-Ether1",
                "bundle_id": 1,
                "lacp_mode": "active",
                "port": {
                    "GigabitEthernet0/0/0/0": {
                        "interface": "GigabitEthernet0/0/0/0",
                        "bundle_id": 1,
                        "rate": 30,
                        "state": "ascdA---",
                        "port_id": "0x000a,0x0001",
                        "key": "0x0001",
                        "system_id": "0x0064,00-1b-0c-10-5a-26",
                        "aggregatable": True,
                        "synchronization": "in_sync",
                        "collecting": True,
                        "distributing": True,
                        "partner": {
                            "rate": 30,
                            "state": "ascdA---",
                            "port_id": "0x000a,0x0001",
                            "key": "0x0001",
                            "system_id": "0x8000,00-0c-86-5e-68-23",
                            "aggregatable": True,
                            "synchronization": "in_sync",
                            "collecting": True,
                            "distributing": True
                        },
                        "receive": "Current",
                        "period": "Slow",
                        "selection": "Selected",
                        "mux": "Distrib",
                        "a_churn": "None",
                        "p_churn": "None"
                    },
                    "GigabitEthernet0/0/0/1": {
                        "interface": "GigabitEthernet0/0/0/1",
                        "bundle_id": 1,
                        "rate": 30,
                        "state": "ascdA---",
                        "port_id": "0x8000,0x0002",
                        "key": "0x0001",
                        "system_id": "0x0064,00-1b-0c-10-5a-26",
                        "aggregatable": True,
                        "synchronization": "in_sync",
                        "collecting": True,
                        "distributing": True,
                        "partner": {
                            "rate": 30,
                            "state": "ascdA---",
                            "port_id": "0x8000,0x0005",
                            "key": "0x0001",
                            "system_id": "0x8000,00-0c-86-5e-68-23",
                            "aggregatable": True,
                            "synchronization": "in_sync",
                            "collecting": True,
                            "distributing": True
                        },
                        "receive": "Current",
                        "period": "Slow",
                        "selection": "Selected",
                        "mux": "Distrib",
                        "a_churn": "None",
                        "p_churn": "None"
                    }
                }
            },
            "Bundle-Ether2": {
                "name": "Bundle-Ether2",
                "bundle_id": 2,
                "lacp_mode": "active",
                "port": {
                    "GigabitEthernet0/0/0/2": {
                        "interface": "GigabitEthernet0/0/0/2",
                        "bundle_id": 2,
                        "rate": 30,
                        "state": "a---A---",
                        "port_id": "0x8000,0x0005",
                        "key": "0x0002",
                        "system_id": "0x0064,00-1b-0c-10-5a-26",
                        "aggregatable": True,
                        "synchronization": "out_sync",
                        "collecting": False,
                        "distributing": False,
                        "partner": {
                            "rate": 30,
                            "state": "as--A---",
                            "port_id": "0x8000,0x0004",
                            "key": "0x0002",
                            "system_id": "0x8000,00-0c-86-5e-68-23",
                            "aggregatable": True,
                            "synchronization": "in_sync",
                            "collecting": False,
                            "distributing": False
                        },
                        "receive": "Current",
                        "period": "Slow",
                        "selection": "Standby",
                        "mux": "Waiting",
                        "a_churn": "Churn",
                        "p_churn": "None"
                    },
                    "GigabitEthernet0/0/0/3": {
                        "interface": "GigabitEthernet0/0/0/3",
                        "bundle_id": 2,
                        "rate": 30,
                        "state": "ascdA---",
                        "port_id": "0x8000,0x0004",
                        "key": "0x0002",
                        "system_id": "0x0064,00-1b-0c-10-5a-26",
                        "aggregatable": True,
                        "synchronization": "in_sync",
                        "collecting": True,
                        "distributing": True,
                        "partner": {
                            "rate": 30,
                            "state": "ascdA---",
                            "port_id": "0x8000,0x0003",
                            "key": "0x0002",
                            "system_id": "0x8000,00-0c-86-5e-68-23",
                            "aggregatable": True,
                            "synchronization": "in_sync",
                            "collecting": True,
                            "distributing": True
                        },
                        "receive": "Current",
                        "period": "Slow",
                        "selection": "Selected",
                        "mux": "Distrib",
                        "a_churn": "None",
                        "p_churn": "None"
                    },
                    "GigabitEthernet0/0/0/4": {
                        "interface": "GigabitEthernet0/0/0/4",
                        "bundle_id": 2,
                        "rate": 30,
                        "state": "ascdA---",
                        "port_id": "0x8000,0x0003",
                        "key": "0x0002",
                        "system_id": "0x0064,00-1b-0c-10-5a-26",
                        "aggregatable": True,
                        "synchronization": "in_sync",
                        "collecting": True,
                        "distributing": True,
                        "partner": {
                            "rate": 30,
                            "state": "ascdA---",
                            "port_id": "0x8000,0x0002",
                            "key": "0x0002",
                            "system_id": "0x8000,00-0c-86-5e-68-23",
                            "aggregatable": True,
                            "synchronization": "in_sync",
                            "collecting": True,
                            "distributing": True
                        },
                        "receive": "Current",
                        "period": "Slow",
                        "selection": "Selected",
                        "mux": "Distrib",
                        "a_churn": "None",
                        "p_churn": "None"
                    }
                }
            }
        }
    }

    LagOpsOutput = {
        "system_priority": 100,
        "interfaces": {
            "Bundle-Ether2": {
                "name": "Bundle-Ether2",
                "bundle_id": 2,
                "oper_status": "up",
                "system_id_mac": "001b.0c10.5a24",
                "system_priority": 100,
                "lacp_max_bundle": 2,
                "lacp_min_bundle": 2,
                "lacp_mode": "active",
                "protocol": "lacp",
                "members": {
                    "GigabitEthernet0/0/0/4": {
                        "interface": "GigabitEthernet0/0/0/4",
                        "synchronization": "in_sync",
                        "aggregatable": True,
                        "collecting": True,
                        "distributing": True,
                        "bundle_id": 2,
                        "bundled": True,
                        "system_id": "001b.0c10.5a26",
                        "oper_key": 2,
                        "port_num": 3,
                        "lacp_port_priority": 32768,
                        "partner_id": "000c.865e.6823",
                        "partner_key": 2,
                        "partner_port_num": 2
                    },
                    "GigabitEthernet0/0/0/3": {
                        "interface": "GigabitEthernet0/0/0/3",
                        "synchronization": "in_sync",
                        "aggregatable": True,
                        "collecting": True,
                        "distributing": True,
                        "bundle_id": 2,
                        "bundled": True,
                        "system_id": "001b.0c10.5a26",
                        "oper_key": 2,
                        "port_num": 4,
                        "lacp_port_priority": 32768,
                        "partner_id": "000c.865e.6823",
                        "partner_key": 2,
                        "partner_port_num": 3
                    },
                    "GigabitEthernet0/0/0/2": {
                        "interface": "GigabitEthernet0/0/0/2",
                        "synchronization": "out_sync",
                        "aggregatable": True,
                        "collecting": False,
                        "distributing": False,
                        "bundle_id": 2,
                        "bundled": False,
                        "system_id": "001b.0c10.5a26",
                        "oper_key": 2,
                        "port_num": 5,
                        "lacp_port_priority": 32768,
                        "partner_id": "000c.865e.6823",
                        "partner_key": 2,
                        "partner_port_num": 4
                    }
                }
            },
            "Bundle-Ether1": {
                "name": "Bundle-Ether1",
                "bundle_id": 1,
                "oper_status": "up",
                "system_id_mac": "001b.0c10.5a25",
                "system_priority": 100,
                "lacp_max_bundle": 8,
                "lacp_min_bundle": 1,
                "lacp_mode": "active",
                "protocol": "lacp",
                "members": {
                    "GigabitEthernet0/0/0/1": {
                        "interface": "GigabitEthernet0/0/0/1",
                        "synchronization": "in_sync",
                        "aggregatable": True,
                        "collecting": True,
                        "distributing": True,
                        "bundle_id": 1,
                        "bundled": True,
                        "system_id": "001b.0c10.5a26",
                        "oper_key": 1,
                        "port_num": 2,
                        "lacp_port_priority": 32768,
                        "partner_id": "000c.865e.6823",
                        "partner_key": 1,
                        "partner_port_num": 5
                    },
                    "GigabitEthernet0/0/0/0": {
                        "interface": "GigabitEthernet0/0/0/0",
                        "synchronization": "in_sync",
                        "aggregatable": True,
                        "collecting": True,
                        "distributing": True,
                        "bundle_id": 1,
                        "bundled": True,
                        "system_id": "001b.0c10.5a26",
                        "oper_key": 1,
                        "port_num": 1,
                        "lacp_port_priority": 10,
                        "partner_id": "000c.865e.6823",
                        "partner_key": 1,
                        "partner_port_num": 1
                    }
                }
            }
        }
    }

