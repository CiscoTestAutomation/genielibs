class PlatformOutput(object):
    showVersionCat6k = {
    'version': {
        'bootldr_version': 's72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)',
        'chassis': 'WS-C6503-E',
        'compiled_by': 'kellythw',
        'compiled_date': 'Thu 23-Nov-06 06:26',
        'cpu': {
            'implementation': '0x504',
            'l2_cache': '512KB',
            'name': 'SR71000',
            'rev': '1.2',
            'speed': '600Mhz',
        },
        'curr_config_register': '0x2102',
        'hostname': 'cat6k_tb1',
        'image': {
            'data_base': '0x42D98000',
            'text_base': '0x40101040',
        },
        'image_id': 's72033_rp-ADVENTERPRISEK9_WAN-M',
        'interfaces': {
            'gigabit_ethernet': 50,
            'virtual_ethernet': 1,
        },
        'last_reset': 's/w',
        'main_mem': '983008',
        'memory': {
            'flash_internal_SIMM': 65536,
            'non_volatile_conf': 1917,
            'packet_buffer': 8192,
        },
        'os': 'IOS',
        'platform': 's72033_rp',
        'processor_board_id': 'FXS1821Q2H9',
        'processor_type': 'R7000',
        'returned_to_rom_by': 'power cycle at 21:57:23 UTC Sat Aug 28 2010 (SP by power on)',
        'rom': 'System Bootstrap, Version 12.2(17r)S4, RELEASE SOFTWARE',
        'rom_version': '(fc1)',
        'softwares': ['SuperLAT software (copyright 1990 by Meridian Technology Corp).', 'X.25 software, Version 3.0.0.', 'Bridging software.', 'TN3270 Emulation software.'],
        'system_image': 'disk0:s72033-adventerprisek9_wan-mz.122-18.SXF7',
        'uptime': '21 weeks, 5 days, 41 minutes',
        'version': '12.2(18)SXF7',
    },
}

    dirCat6k = {
    'dir': {
        'dir': 'disk0:/',
        'disk0:/': {
            'bytes_free': '27852800',
            'bytes_total': '512065536',
            'files': {
                'cat6k_tb1-confg': {
                    'index': '4',
                    'last_modified_date': 'Jul 21 2015 14:11:10 +00:00',
                    'permissions': '-rw-',
                    'size': '4485',
                },
                'config_cat6k_tb1_native': {
                    'index': '5',
                    'last_modified_date': 'Nov 27 2017 21:32:46 +00:00',
                    'permissions': '-rw-',
                    'size': '4734',
                },
                's72033-adventerprisek9_wan-mz.122-18.SXF7': {
                    'index': '1',
                    'last_modified_date': 'Oct 28 2009 19:07:04 +00:00',
                    'permissions': '-rw-',
                    'size': '82524740',
                },
                's72033-adventerprisek9_wan_dbg-vz.CARSON_INTEG_100202': {
                    'index': '2',
                    'last_modified_date': 'Feb 3 2010 22:27:04 +00:00',
                    'permissions': '-rw-',
                    'size': '200200276',
                },
                's72033-adventerprisek9_wan_dbg-vz.SIERRA_INTEG_100202': {
                    'index': '3',
                    'last_modified_date': 'Feb 3 2010 23:18:40 +00:00',
                    'permissions': '-rw-',
                    'size': '201459508',
                },
            },
        },
    },
}

    dirEmptyCat6k = {}

    showRedundancyCat6k = {
    'red_sys_info': {
        'available_system_uptime': '21 weeks, 5 days, 1 hour, 3 minutes',
        'communications': 'Down',
        'communications_reason': 'Simplex mode',
        'conf_red_mode': 'sso',
        'hw_mode': 'Simplex',
        'last_switchover_reason': 'none',
        'maint_mode': 'Disabled',
        'oper_red_mode': 'sso',
        'standby_failures': '0',
        'switchovers_system_experienced': '0',
    },
    'slot': {
        'slot 1': {
            'compiled_by': 'kellythw',
            'compiled_date': 'Thu 23-Nov-06 06:26',
            'config_register': '0x2102',
            'curr_sw_state': 'ACTIVE',
            'image_id': 's72033_rp-ADVENTERPRISEK9_WAN-M',
            'image_ver': 'Cisco Internetwork Operating System Software',
            'os': 'IOS',
            'platform': 's72033_rp',
            'uptime_in_curr_state': '21 weeks, 5 days, 1 hour, 2 minutes',
            'version': '12.2(18)SXF7',
        },
    },
}

    showInventoryCat6k = {
    'index': {
        1: {
            'descr': 'Cisco Systems Catalyst 6500 3-slot Chassis System',
            'name': 'WS-C6503-E',
            'pid': 'WS-C6503-E',
            'sn': 'FXS1821Q2H9',
            'vid': 'V03',
        },
        2: {
            'descr': 'OSR-7600 Clock FRU 1',
            'name': 'CLK-7600 1',
            'pid': 'CLK-7600',
            'sn': 'FXS181101V4',
        },
        3: {
            'descr': 'OSR-7600 Clock FRU 2',
            'name': 'CLK-7600 2',
            'pid': 'CLK-7600',
            'sn': 'FXS181101V4',
        },
        4: {
            'descr': 'WS-SUP720-3BXL 2 ports Supervisor Engine 720 Rev. 5.6',
            'name': '1',
            'pid': 'WS-SUP720-3BXL',
            'sn': 'SAL11434P2C',
            'vid': 'V05',
        },
        5: {
            'descr': 'WS-SUP720 MSFC3 Daughterboard Rev. 3.1',
            'name': 'msfc sub-module of 1',
            'pid': 'WS-SUP720',
            'sn': 'SAL11434N9G',
        },
        6: {
            'descr': 'WS-F6K-PFC3BXL Policy Feature Card 3 Rev. 1.8',
            'name': 'switching engine sub-module of 1',
            'pid': 'WS-F6K-PFC3BXL',
            'sn': 'SAL11434LYG',
            'vid': 'V01',
        },
        7: {
            'descr': 'WS-X6748-GE-TX CEF720 48 port 10/100/1000mb Ethernet Rev. 2.6',
            'name': '2',
            'pid': 'WS-X6748-GE-TX',
            'sn': 'SAL1128UPQ9',
            'vid': 'V02',
        },
        8: {
            'descr': 'WS-F6700-DFC3CXL Distributed Forwarding Card 3 Rev. 1.1',
            'name': 'switching engine sub-module of 2',
            'pid': 'WS-F6700-DFC3CXL',
            'sn': 'SAL1214LAG5',
            'vid': 'V01',
        },
        9: {
            'descr': 'Enhanced 3-slot Fan Tray 1',
            'name': 'WS-C6503-E-FAN 1',
            'pid': 'WS-C6503-E-FAN',
            'sn': 'DCH183500KW',
            'vid': 'V02',
        },
        10: {
            'descr': 'AC power supply, 1400 watt 1',
            'name': 'PS 1 PWR-1400-AC',
            'pid': 'PWR-1400-AC',
            'sn': 'ABC0830J127',
            'vid': 'V01',
        },
    },
}

    showModuleCat6k = {
        "slot": {
            "1": {
                "rp": {
                    "card_type": "Catalyst 6000 supervisor 2 (Active)",
                    "fw_ver": "6.1(3)",
                    "hw_ver": "3.9",
                    "mac_address_from": "0001.6416.0342",
                    "mac_address_to": "0001.6416.0343",
                    "model": "WS-X6K-S2U-MSFC2",
                    "ports": 2,
                    "serial_number": "SAD0628035C",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-MSFC2": {
                            "hw_ver": "2.5",
                            "model": "WS-F6K-MSFC2",
                            "serial_number": "SAD062803TX",
                            "status": "Ok",
                        },
                        "WS-F6K-PFC2": {
                            "hw_ver": "3.2",
                            "model": "WS-F6K-PFC2",
                            "serial_number": "SAD062802AV",
                            "status": "Ok",
                        },
                    },
                    "sw_ver": "7.5(0.6)HUB9",
                }
            },
            "2": {
                "rp": {
                    "card_type": "Supervisor-Other",
                    "fw_ver": "Unknown",
                    "hw_ver": "0.0",
                    "mac_address_from": "0000.0000.0000",
                    "mac_address_to": "0000.0000.0000",
                    "model": "unknown",
                    "ports": 0,
                    "serial_number": "unknown",
                    "status": "Unknown",
                    "sw_ver": "Unknown",
                }
            },
            "3": {
                "lc": {
                    "card_type": "Pure SFM-mode 16 port 1000mb GBIC",
                    "fw_ver": "12.1(5r)E1",
                    "hw_ver": "1.3",
                    "mac_address_from": "0005.7485.9518",
                    "mac_address_to": "0005.7485.9527",
                    "model": "WS-X6816-GBIC",
                    "ports": 16,
                    "serial_number": "SAL061218K3",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-DFC": {
                            "hw_ver": "2.1",
                            "model": "WS-F6K-DFC",
                            "serial_number": "SAL06121A19",
                            "status": "Ok",
                        }
                    },
                    "sw_ver": "12.1(13)E3",
                }
            },
            "4": {
                "lc": {
                    "card_type": "Pure SFM-mode 16 port 1000mb GBIC",
                    "fw_ver": "12.1(5r)E1",
                    "hw_ver": "1.3",
                    "mac_address_from": "0005.7485.9548",
                    "mac_address_to": "0005.7485.9557",
                    "model": "WS-X6816-GBIC",
                    "ports": 16,
                    "serial_number": "SAL061218K8",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-DFC": {
                            "hw_ver": "2.1",
                            "model": "WS-F6K-DFC",
                            "serial_number": "SAL06121A46",
                            "status": "Ok",
                        }
                    },
                    "sw_ver": "12.1(13)E3",
                }
            },
            "5": {
                "other": {
                    "card_type": "Switching Fabric Module-136 (Active)",
                    "fw_ver": "6.1(3)",
                    "hw_ver": "1.2",
                    "mac_address_from": "0001.0002.0003",
                    "mac_address_to": "0001.0002.0003",
                    "model": "WS-X6500-SFM2",
                    "ports": 0,
                    "serial_number": "SAD061701YC",
                    "status": "Ok",
                    "sw_ver": "7.5(0.6)HUB9",
                }
            },
            "6": {
                "lc": {
                    "card_type": "1 port 10-Gigabit Ethernet Module",
                    "fw_ver": "6.3(1)",
                    "hw_ver": "1.0",
                    "mac_address_from": "0002.7ec2.95f2",
                    "mac_address_to": "0002.7ec2.95f2",
                    "model": "WS-X6502-10GE",
                    "ports": 1,
                    "serial_number": "SAD062003CM",
                    "status": "Ok",
                    "subslot": {
                        "WS-F6K-DFC": {
                            "hw_ver": "2.3",
                            "model": "WS-F6K-DFC",
                            "serial_number": "SAL06261R0A",
                            "status": "Ok",
                        },
                        "WS-G6488": {
                            "hw_ver": "1.1",
                            "model": "WS-G6488",
                            "serial_number": "SAD062201BN",
                            "status": "Ok",
                        },
                    },
                    "sw_ver": "7.5(0.6)HUB9",
                }
            },
        }
    }

    platform_all_cat6k = {
        'chassis': 'WS-C6503-E',
        'config_register': '0x2102',
        'dir': 'disk0:/',
        'image': 'disk0:s72033-adventerprisek9_wan-mz.122-18.SXF7',
        'main_mem': '983008',
        'os': 'ios',
        'redundancy_communication': False,
        'redundancy_mode': 'sso',
        'rtr_type': 'CAT6K',
        'slot': {
                'lc': {
                    '2': {
                        'name': '2',
                        'sn': 'SAL1128UPQ9',
                        'subslot': {
                            'switching engine sub-module of 2': {
                                'name': 'switching engine sub-module of 2',
                                'sn': 'SAL1214LAG5',
                            },
                        },
                    },
                },
                'oc': {
                    'CLK-7600 1': {
                        'name': 'CLK-7600 1',
                        'sn': 'FXS181101V4'
                    },
                    'CLK-7600 2': {
                        'name': 'CLK-7600 2',
                        'sn': 'FXS181101V4'
                    },
                    'PS 1 PWR-1400-AC': {
                        'name': 'PS 1 PWR-1400-AC',
                        'sn': 'ABC0830J127',
                    },
                    'WS-C6503-E-FAN 1': {
                        'name': 'WS-C6503-E-FAN 1',
                        'sn': 'DCH183500KW',
                    },
                },
                'rp': {
                    '1': {
                        'name': '1',
                        'sn': 'SAL11434P2C',
                        'config_register': '0x2102',
                        'redundancy_state': 'active',
                        'system_image': 'Cisco Internetwork Operating System Software',
                        'uptime': '21 weeks, 5 days, 1 hour, 2 minutes',
                        'subslot': {
                            'switching engine sub-module of 1': {
                                'name': 'switching engine sub-module of 1',
                                'sn': 'SAL11434LYG',
                            },
                            'msfc sub-module of 1': {
                                'name': 'msfc sub-module of 1',
                                'sn': 'SAL11434N9G',
                            },
                        },
                    },
                },
        },
        'switchover_reason': 'none',
        'version': '12.2(18)SXF7',
    }
