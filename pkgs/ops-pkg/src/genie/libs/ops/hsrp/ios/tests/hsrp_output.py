class HsrpOutput(object):

    # 'show standby all' output
    showStandbyAllOutput = {
        "GigabitEthernet1/0/1": {
            "address_family": {
                "ipv4": {
                    "version": {
                        2: {
                            "groups": {
                                0: {
                                    "active_router": "local",
                                    "authentication": "5",
                                    "authentication_type": "MD5",
                                    "default_priority": 100,
                                    "group_number": 0,
                                    "hsrp_router_state": "active",
                                    "last_state_change": "1w0d",
                                    "local_virtual_mac_address": "0000.0c9f.f000",
                                    "local_virtual_mac_address_conf": "v2 " "default",
                                    "preempt": True,
                                    "preempt_min_delay": 5,
                                    "preempt_reload_delay": 10,
                                    "preempt_sync_delay": 20,
                                    "primary_ipv4_address": {
                                        "address": "192.168.1.254"
                                    },
                                    "priority": 100,
                                    "session_name": "hsrp-Gi1/0/1-0",
                                    "standby_ip_address": "192.168.1.2",
                                    "standby_router": "192.168.1.2",
                                    "standby_priority": 100,
                                    "standby_expires_in": 10.624,
                                    "statistics": {"num_state_changes": 8},
                                    "timers": {
                                        "hello_msec_flag": False,
                                        "hello_sec": 5,
                                        "hold_msec_flag": False,
                                        "hold_sec": 20,
                                        "next_hello_sent": 2.848,
                                    },
                                    "virtual_mac_address": "0000.0c9f.f000",
                                    "virtual_mac_address_mac_in_use": True,
                                }
                            }
                        }
                    }
                }
            },
            "interface": "GigabitEthernet1/0/1",
            "redirects_disable": False,
            "use_bia": False,
        },
        "GigabitEthernet1/0/2": {
            "address_family": {
                "ipv4": {
                    "version": {
                        1: {
                            "groups": {
                                10: {
                                    "active_router": "unknown",
                                    "authentication": "cisco123",
                                    "authentication_type": "MD5",
                                    "configured_priority": 110,
                                    "group_number": 10,
                                    "hsrp_router_state": "disabled",
                                    "local_virtual_mac_address": "0000.0c07.ac0a",
                                    "local_virtual_mac_address_conf": "v1 " "default",
                                    "preempt": True,
                                    "primary_ipv4_address": {"address": "unknown"},
                                    "priority": 110,
                                    "session_name": "hsrp-Gi1/0/2-10",
                                    "standby_ip_address": "unknown",
                                    "standby_router": "unknown",
                                    "timers": {
                                        "hello_msec_flag": False,
                                        "hello_sec": 3,
                                        "hold_msec_flag": False,
                                        "hold_sec": 10,
                                    },
                                    "virtual_mac_address": "unknown",
                                    "virtual_mac_address_mac_in_use": False,
                                }
                            }
                        }
                    }
                }
            },
            "interface": "GigabitEthernet1/0/2",
            "redirects_disable": False,
            "use_bia": False,
        },
        "GigabitEthernet3": {
            "address_family": {
                "ipv4": {
                    "version": {
                        1: {
                            "groups": {
                                10: {
                                    "active_expires_in": 0.816,
                                    "active_ip_address": "10.1.2.1",
                                    "active_router": "10.1.2.1",
                                    "active_router_priority": 120,
                                    "configured_priority": 110,
                                    "group_number": 10,
                                    "hsrp_router_state": "standby",
                                    "local_virtual_mac_address": "0000.0c07.ac0a",
                                    "local_virtual_mac_address_conf": "v1 " "default",
                                    "preempt": True,
                                    "primary_ipv4_address": {"address": "10.1.2.254"},
                                    "priority": 110,
                                    "session_name": "hsrp-Gi3-10",
                                    "standby_router": "local",
                                    "timers": {
                                        "hello_msec_flag": False,
                                        "hello_sec": 3,
                                        "hold_msec_flag": False,
                                        "hold_sec": 10,
                                        "next_hello_sent": 2.096,
                                    },
                                    "virtual_mac_address": "0050.568e.3a40",
                                    "virtual_mac_address_mac_in_use": False,
                                }
                            }
                        }
                    }
                }
            },
            "interface": "GigabitEthernet3",
            "redirects_disable": False,
            "use_bia": False,
        },
    }

    showStandbyAllOutput_golden = """
        GigabitEthernet1/0/1 - Group 0 (version 2)
          State is Active
            8 state changes, last state change 1w0d
            Track object 1 (unknown)
          Virtual IP address is 192.168.1.254
          Active virtual MAC address is 0000.0c9f.f000 (MAC In Use)
            Local virtual MAC address is 0000.0c9f.f000 (v2 default)
          Hello time 5 sec, hold time 20 sec
            Next hello sent in 2.848 secs
          Authentication MD5, key-chain "5"
          Preemption enabled, delay min 5 secs, reload 10 secs, sync 20 secs
          Active router is local
          Standby router is 192.168.1.2, priority 100 (expires in 10.624 sec)
          Priority 100 (default 100)
          Group name is "hsrp-Gi1/0/1-0" (default)
        GigabitEthernet1/0/2 - Group 10
          State is Disabled
          Virtual IP address is unknown
          Active virtual MAC address is unknown (MAC Not In Use)
            Local virtual MAC address is 0000.0c07.ac0a (v1 default)
          Hello time 3 sec, hold time 10 sec
          Authentication MD5, key-chain "cisco123"
          Preemption enabled
          Active router is unknown
          Standby router is unknown
          Priority 110 (configured 110)
          Group name is "hsrp-Gi1/0/2-10" (default)
        GigabitEthernet3 - Group 10
          State is Standby
            1 state change, last state change 00:00:08
          Virtual IP address is 10.1.2.254
          Active virtual MAC address is 0050.568e.3a40 (MAC Not In Use)
            Local virtual MAC address is 0000.0c07.ac0a (v1 default)
          Hello time 3 sec, hold time 10 sec
            Next hello sent in 2.096 secs
          Preemption enabled
          Active router is 10.1.2.1, priority 120 (expires in 0.816 sec)
          Standby router is local
          Priority 110 (configured 110)
          Group name is "hsrp-Gi3-10" (default)
        """

    # 'show standby internal' output
    showStandbyInternalOutput = {
        "hsrp_common_process_state": "not running",
        "hsrp_ha_state": "capable",
        "hsrp_ipv4_process_state": "not running",
        "hsrp_ipv6_process_state": "not running",
        "hsrp_timer_wheel_state": "running",
        "mac_address_table": {
            166: {"group": 10, "interface": "gi2/0/3", "mac_address": "0000.0c07.ac0a"},
            169: {"group": 5, "interface": "gi1/0/1", "mac_address": "0000.0c07.ac05"},
            172: {"group": 0, "interface": "gi2/0/3", "mac_address": "0000.0c07.ac00"},
            173: {"group": 1, "interface": "gi2/0/3", "mac_address": "0000.0c07.ac01"},
        },
        "msgQ_max_size": 0,
        "msgQ_size": 0,
        "v3_to_v4_transform": "disabled",
        "virtual_ip_hash_table": {
            "ipv6": {
                78: {"group": 20, "interface": "gi1", "ip": "2001:DB8:10:1:1::254"}
            },
            "ipv4": {
                103: {"group": 0, "interface": "gi1/0/1", "ip": "192.168.1.254"},
                106: {"group": 10, "interface": "gi1/0/2", "ip": "192.168.2.254"},
            },
        },
    }

    showStandbyInternalOutput_golden = """
        HSRP common process not running
          MsgQ size 0, max 0
        HSRP IPv4 process not running
        HSRP IPv6 process not running
        HSRP Timer wheel running
        HSRP HA capable, v3 to v4 transform disabled

        HSRP virtual IP Hash Table (global)
        103 192.168.1.254                    Gi1/0/1    Grp 0
        106 192.168.2.254                    Gi1/0/2    Grp 10

        HSRP virtual IPv6 Hash Table (global)
        78  2001:DB8:10:1:1::254             Gi1        Grp 20

        HSRP MAC Address Table
        169 Gi1/0/1 0000.0c07.ac05
            Gi1/0/1 Grp 5
        166 Gi2/0/3 0000.0c07.ac0a
            Gi2/0/3 Grp 10
        172 Gi2/0/3 0000.0c07.ac00
            Gi2/0/3 Grp 0
        173 Gi2/0/3 0000.0c07.ac01
            Gi2/0/3 Grp 1
    """

    showStandbyDelayOutput = {
        "GigabitEthernet1": {"delay": {"minimum_delay": 99, "reload_delay": 888}}
    }

    showStandbyDelayOutput_golden = """
        Interface          Minimum Reload 
        GigabitEthernet1   99      888   
    """

    # Hsrp Ops Object final output
    hsrpOpsOutput = {
        "GigabitEthernet1": {"delay": {"minimum_delay": 99, "reload_delay": 888}},
        "GigabitEthernet3": {
            "address_family": {
                "ipv4": {
                    "version": {
                        1: {
                            "groups": {
                                10: {
                                    "timers": {
                                        "hello_msec_flag": False,
                                        "hello_sec": 3,
                                        "hold_msec_flag": False,
                                        "hold_sec": 10,
                                    },
                                    "primary_ipv4_address": {"address": "10.1.2.254"},
                                    "priority": 110,
                                    "preempt": True,
                                    "session_name": "hsrp-Gi3-10",
                                    "virtual_mac_address": "0050.568e.3a40",
                                    "group_number": 10,
                                    "active_ip_address": "10.1.2.1",
                                    "hsrp_router_state": "standby",
                                    "active_router": "10.1.2.1",
                                    "standby_router": "local",
                                }
                            }
                        }
                    }
                }
            },
            "use_bia": False,
            "redirects_disable": False,
            "interface": "GigabitEthernet3",
        },
        "GigabitEthernet1/0/2": {
            "address_family": {
                "ipv4": {
                    "version": {
                        1: {
                            "groups": {
                                10: {
                                    "timers": {
                                        "hello_msec_flag": False,
                                        "hello_sec": 3,
                                        "hold_msec_flag": False,
                                        "hold_sec": 10,
                                    },
                                    "primary_ipv4_address": {"address": "unknown"},
                                    "authentication": "cisco123",
                                    "priority": 110,
                                    "preempt": True,
                                    "session_name": "hsrp-Gi1/0/2-10",
                                    "virtual_mac_address": "unknown",
                                    "group_number": 10,
                                    "standby_ip_address": "unknown",
                                    "hsrp_router_state": "disabled",
                                    "active_router": "unknown",
                                    "standby_router": "unknown",
                                }
                            }
                        }
                    }
                }
            },
            "use_bia": False,
            "redirects_disable": False,
            "interface": "GigabitEthernet1/0/2",
        },
        "GigabitEthernet1/0/1": {
            "address_family": {
                "ipv4": {
                    "version": {
                        2: {
                            "groups": {
                                0: {
                                    "timers": {
                                        "hello_msec_flag": False,
                                        "hello_sec": 5,
                                        "hold_msec_flag": False,
                                        "hold_sec": 20,
                                    },
                                    "primary_ipv4_address": {
                                        "address": "192.168.1.254"
                                    },
                                    "authentication": "5",
                                    "priority": 100,
                                    "preempt": True,
                                    "session_name": "hsrp-Gi1/0/1-0",
                                    "virtual_mac_address": "0000.0c9f.f000",
                                    "group_number": 0,
                                    "standby_ip_address": "192.168.1.2",
                                    "hsrp_router_state": "active",
                                    "active_router": "local",
                                    "standby_router": "192.168.1.2",
                                }
                            }
                        }
                    }
                }
            },
            "use_bia": False,
            "redirects_disable": False,
            "interface": "GigabitEthernet1/0/1",
        },
    }
