"""Mock parser outputs for a Catalyst 9610R chassis.

Used by ``test_platform_rev1`` and ``test_platform_rev2`` to drive
``Platform.learn()`` end-to-end against a chassis that exercises the
``hw_revision`` reconciliation path .

"""


class PlatformOutput(object):

    showVersionC9610R = {
        'version': {
            'version_short': '26.01',
            'platform': 'Catalyst L3 Switch',
            'version': '26.01.01prd12',
            'image_id': 'CISCO9K_IOSXE-UNIVERSALK9-M',
            'rom': 'IOS-XE ROMMON',
            'hostname': 'EPCOT-ES-DUT1',
            'uptime': '5 days, 4 hours',
            'system_image': 'bootflash:cisco9k-universalk9.26.01.01.SPA.bin',
            'last_reload_reason': 'Reload Command',
            'license_level': 'network-advantage',
            'chassis': 'C9610R',
            'processor_type': 'X86',
            'chassis_sn': 'FOX2746PQGL',
            'rtr_type': 'C9610R',
            'os': 'IOS-XE',
            'curr_config_register': '0x2102',
            'main_mem': '5762870',
        }
    }

    showDirC9610R = {
        'dir': {
            'dir': 'bootflash:/',
            'bootflash:/': {
                'bytes_free': '8000000000',
                'bytes_total': '16000000000',
                'files': {},
            },
        },
    }

    showRedundancyC9610R = {
        'red_sys_info': {
            'available_system_uptime': '5 days, 4 hours',
            'switchovers_system_experienced': '0',
            'standby_failures': '0',
            'last_switchover_reason': 'none',
            'hw_mode': 'Duplex',
            'conf_red_mode': 'sso',
            'oper_red_mode': 'sso',
            'maint_mode': 'Disabled',
            'communications': 'Up',
        },
        'slot': {
            'slot 5': {
                'curr_sw_state': 'ACTIVE',
                'uptime_in_curr_state': '5 days, 4 hours',
                'image_ver': 'Cisco IOS Software [IOSXE], Version 26.01.01prd12',
                'boot': 'bootflash:cisco9k-universalk9.26.01.01.SPA.bin,1;',
                'config_register': '0x2102',
            },
            'slot 6': {
                'curr_sw_state': 'STANDBY HOT',
                'uptime_in_curr_state': '5 days, 3 hours',
                'image_ver': 'Cisco IOS Software [IOSXE], Version 26.01.01prd12',
                'boot': 'bootflash:cisco9k-universalk9.26.01.01.SPA.bin,1;',
                'config_register': '0x2102',
            },
        },
    }

    showInventoryC9610R = {
        'main': {
            'chassis': {
                'C9610R': {
                    'name': 'Chassis',
                    'descr': 'Cisco C9610 Series 10 Slot Chassis',
                    'pid': 'C9610R',
                    'vid': 'V00',
                    'sn': 'FOX2746PQGL',
                },
            },
        },
        'slot': {
            '1': {
                'lc': {
                    'C9600X-LC-32CD': {
                        'name': 'module 1',
                        'descr': 'Cisco Catalyst 9600 Series 32x40/100GE + 2x40/100/400GE',
                        'pid': 'C9600X-LC-32CD',
                        'vid': 'V00',
                        'sn': 'FDO281001L2',
                    },
                },
            },
            '3': {
                'lc': {
                    'C9610-LC-40YL4CD': {
                        'name': 'module 3',
                        'descr': 'Cisco Catalyst 9610 Series 40x1/10/25/50GE + 2x200GE + 2x400GE',
                        'pid': 'C9610-LC-40YL4CD',
                        'vid': 'V00',
                        'sn': 'FDO28080M8H',
                    },
                },
            },
            '5': {
                'rp': {
                    'C9610-SUP-3': {
                        'name': 'module 5',
                        'descr': 'Cisco Catalyst 9610 Series Supervisor 3 Module',
                        'pid': 'C9610-SUP-3',
                        'vid': 'V00',
                        'sn': 'FDO27520J4X',
                    },
                },
            },
            '6': {
                'rp': {
                    'C9610-SUP-3': {
                        'name': 'module 6',
                        'descr': 'Cisco Catalyst 9610 Series Supervisor 3 Module',
                        'pid': 'C9610-SUP-3',
                        'vid': 'V00',
                        'sn': 'FDO27520J4Y',
                    },
                },
            },
            '9': {
                'lc': {
                    'C9600-LC-48TX': {
                        'name': 'module 9',
                        'descr': 'Cisco Catalyst 9600 Series 48-Port 10GE and MGIG COPPER',
                        'pid': 'C9600-LC-48TX',
                        'vid': 'V00',
                        'sn': 'CAT2315L01R',
                    },
                },
            },
        },
    }

    showPlatformC9610R = {
        'main': {
            'switch_mac_address': 'a410.b6bb.b9ff',
            'mac_persistency_wait_time': 'Indefinite',
            'chassis': 'C9610R',
        },
        'slot': {
            '1': {
                'lc': {
                    'C9600X-LC-32CD': {
                        'slot': '1',
                        'name': 'C9600X-LC-32CD',
                        'state': 'ok',
                        'insert_time': '5d04h',
                    },
                },
            },
            '3': {
                'lc': {
                    'C9610-LC-40YL4CD': {
                        'slot': '3',
                        'name': 'C9610-LC-40YL4CD',
                        'state': 'ok',
                        'insert_time': '5d04h',
                    },
                },
            },
            '5': {
                'rp': {
                    'C9610-SUP-3': {
                        'slot': '5',
                        'name': 'C9610-SUP-3',
                        'state': 'ok, active',
                        'role': 'Active',
                    },
                },
            },
            '6': {
                'rp': {
                    'C9610-SUP-3': {
                        'slot': '6',
                        'name': 'C9610-SUP-3',
                        'state': 'ok, standby',
                        'role': 'Standby',
                    },
                },
            },
            '9': {
                'lc': {
                    'C9600-LC-48TX': {
                        'slot': '9',
                        'name': 'C9600-LC-48TX',
                        'state': 'ok',
                        'insert_time': '5d04h',
                    },
                },
            },
        },
    }


    showModuleC9610R = {
        'module': {
            1: {
                'ports': 32,
                'card_type': '30x40/100GE + 2x40/100/400GE',
                'model': 'C9600X-LC-32CD',
                'serial': 'FDO281001L2',
                'mac_address': 'B08D.57C1.2400',
                'hw': '1.0',
                'fw': '18.1.0.9',
                'sw': '26.01.01prd12',
                'status': 'ok',
            },
            3: {
                'ports': 44,
                'card_type': '40x1/10/25/50GE + 2x200GE + 2x400GE',
                'model': 'C9610-LC-40YL4CD',
                'serial': 'FDO28080M8H',
                'mac_address': '24D5.E4D1.C280',
                'hw': '0.2',
                'fw': '18.1.0.9',
                'sw': '26.01.01prd12',
                'status': 'ok',
            },
            5: {
                'ports': 0,
                'card_type': 'Supervisor 3 Module',
                'model': 'C9610-SUP-3',
                'serial': 'FDO27520J4X',
                'mac_address': 'CC36.CFF4.4C00',
                'hw': '0.3',
                'fw': '18.1.0.9',
                'sw': '26.01.01prd12',
                'status': 'ok',
                'redundancy_role': 'Active',
                'operating_redundancy_mode': 'sso',
                'configured_redundancy_mode': 'sso',
            },
            6: {
                'ports': 0,
                'card_type': 'Supervisor 3 Module',
                'model': 'C9610-SUP-3',
                'serial': 'FDO27520J4Y',
                'mac_address': 'CC36.CFF4.4980',
                'hw': '0.3',
                'fw': '18.1.0.9',
                'sw': '26.01.01prd12',
                'status': 'ok',
                'redundancy_role': 'Standby',
                'operating_redundancy_mode': 'sso',
                'configured_redundancy_mode': 'sso',
            },
            9: {
                'ports': 48,
                'card_type': '48-Port 10GE and MGIG COPPER',
                'model': 'C9600-LC-48TX',
                'serial': 'CAT2315L01R',
                'mac_address': 'DC8C.37CA.1780',
                'hw': '0.5',
                'fw': '18.1.0.9',
                'sw': '26.01.01prd12',
                'status': 'ok',
            },
        },
        'number_of_mac_address': 64,
        'chassis_mac_address_lower_range': 'a410.b6bb.b9ff',
        'chassis_mac_address_upper_range': 'a410.b6bb.ba3e',
    }

    expected_hw_revision_C9610R = {
        'lc': {
            '1': '1.0',
            '3': '0.2',
            '9': '0.5',
        },
        'rp': {
            '5': '0.3',
            '6': '0.3',
        },
    }
