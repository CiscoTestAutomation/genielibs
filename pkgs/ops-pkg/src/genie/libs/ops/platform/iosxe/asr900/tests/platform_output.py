
class PlatformOutput(object):

    showVersion = {
        'version': {
            'version_short': '16.9',
            'platform': 'ASR920',
            'version': '16.9.5f',
            'image_id': 'PPC_LINUX_IOSD-UNIVERSALK9_NPE-M',
            'os': 'IOS-XE',
            'image_type': 'production image',
            'compiled_date': 'Fri 28-Feb-20 08:00',
            'compiled_by': 'mcpre',
            'rom': 'IOS-XE ROMMON',
            'hostname': 'SLV3ARIP1',
            'uptime': '4 weeks, 20 hours, 35 minutes',
            'uptime_this_cp': '4 weeks, 20 hours, 40 minutes',
            'returned_to_rom_by': 'reload',
            'returned_to_rom_at': '04:49:49 WEST Mon Aug 3 2020',
            'system_restarted_at': '13:25:16 WEST Mon Aug 3 2020',
            'system_image': 'bootflash:asr920-universalk9_npe.16.09.05f.SPA.bin',
            'last_reload_reason': 'Reload Command',
            'license_level': 'advancedmetroipaccess',
            'license_type': 'Smart License',
            'next_reload_license_level': 'advancedmetroipaccess',
            'chassis': 'ASR-920-24SZ-M',
            'main_mem': '896500',
            'processor_type': 'Freescale P2020',
            'rtr_type': 'ASR-920-24SZ-M',
            'chassis_sn': 'CAT2351V2DV',
            'number_of_intfs': {
                'Gigabit Ethernet': '24',
                'Ten Gigabit Ethernet': '4'
            },
            'mem_size': {
                'non-volatile configuration': '32768',
                'physical': '3670016'
            },
            'disks': {
                'bootflash:.': {
                    'disk_size': '1231647',
                    'type_of_disk': 'eMMC flash'
                }
            },
            'curr_config_register': '0x2102'
        }
    }


    showDir = {
        'dir': {
            'bootflash:/': {
                'files': {
                    'asr920-universalk9_npe.V169_3_SR684942877_7.SPA.bin': {
                        'index': '12',
                        'permissions': '-rw-',
                        'size': '445859733',
                        'last_modified_date': 'Aug 3 2020 04:46:07 +01:00'
                    },
                    'asr920-universalk9_npe.16.09.05f.SPA.bin': {
                        'index': '46294',
                        'permissions': '-rw-',
                        'size': '446696903',
                        'last_modified_date': 'Aug 3 2020 04:39:15 +01:00'
                    },
                },
                'bytes_total': '1241329664',
                'bytes_free': '197324800'
            },
            'dir': 'bootflash:/'
        }
    }


    showDirEmpty = {}

    showPlatform = {
        'slot': {
            'R0': {
                'other': {
                    'ASR-920-24SZ-M': {
                        'slot': 'R0',
                        'name': 'ASR-920-24SZ-M',
                        'state': 'ok, active',
                        'insert_time': '4w0d',
                        'cpld_ver': '19070515',
                        'fw_ver': '15.6(32r)S'
                    }
                }
            },
            'F0': {
                'other': {
                    'ok,': {
                        'slot': 'F0',
                        'name': 'ok,',
                        'state': 'active',
                        'insert_time': '4w0d',
                        'cpld_ver': '19070515',
                        'fw_ver': '15.6(32r)S'
                    }
                }
            },
            'P0': {
                'other': {
                    'ASR920-PSU0': {
                        'slot': 'P0',
                        'name': 'ASR920-PSU0',
                        'state': 'ok',
                        'insert_time': '4w0d'
                    }
                }
            },
            'P1': {
                'other': {
                    'ASR920-PSU1': {
                        'slot': 'P1',
                        'name': 'ASR920-PSU1',
                        'state': 'ok',
                        'insert_time': '4w0d'
                    }
                }
            },
            'P2': {
                'other': {
                    'ASR920-FAN': {
                        'slot': 'P2',
                        'name': 'ASR920-FAN',
                        'state': 'ok',
                        'insert_time': '4w0d'
                    }
                }
            }
        }
    }


    showInventory = {
        'main': {
            'chassis': {
                'ASR-920-24SZ-M': {
                    'name': 'Chassis',
                    'descr': 'Cisco ASR920 Series - 24GE Fiber and 4-10GE - Modular PSU',
                    'pid': 'ASR-920-24SZ-M',
                    'vid': 'V01',
                    'sn': 'CAT2351V2DV'
                }
            }
        },
        'slot': {
            '0': {
                'rp': {
                    'ASR-920-24SZ-M': {
                        'name': 'Chassis',
                        'descr': 'Cisco ASR920 Series - 24GE Fiber and 4-10GE - Modular PSU',
                        'pid': 'ASR-920-24SZ-M',
                        'vid': 'V01',
                        'sn': 'CAT2351V2DV',
                        'subslot': {
                            '0 transceiver 0': {
                                'GLC-LH-SMD': {
                                    'name': 'subslot 0/0 transceiver 0',
                                    'descr': 'GE ZX',
                                    'pid': 'GLC-LH-SMD',
                                    'vid': '001',
                                    'sn': 'EO12004220289'
                                }
                            },
                            '0 transceiver 4': {
                                'GPB-4324L-L2CD-C': {
                                    'name': 'subslot 0/0 transceiver 4',
                                    'descr': '1000BASE BX10-D',
                                    'pid': 'GPB-4324L-L2CD-C',
                                    'vid': '11.0',
                                    'sn': 'S1407012750'
                                }
                            },
                            '0 transceiver 5': {
                                'GPB-4324L-L2CD-C': {
                                    'name': 'subslot 0/0 transceiver 5',
                                    'descr': '1000BASE BX10-D',
                                    'pid': 'GPB-4324L-L2CD-C',
                                    'vid': '11.0',
                                    'sn': 'S1407012739'
                                }
                            },
                            '0 transceiver 6': {
                                'GPB-4324L-L2CD-C': {
                                    'name': 'subslot 0/0 transceiver 6',
                                    'descr': '1000BASE BX10-D',
                                    'pid': 'GPB-4324L-L2CD-C',
                                    'vid': '11.0',
                                    'sn': 'S1406135212'
                                }
                            },
                            '0 transceiver 7': {
                                'GPB-4324L-L2CD-C': {
                                    'name': 'subslot 0/0 transceiver 7',
                                    'descr': '1000BASE BX10-D',
                                    'pid': 'GPB-4324L-L2CD-C',
                                    'vid': '11.0',
                                    'sn': 'S1406136319'
                                }
                            },
                            '0 transceiver 17': {
                                'GLC-LH-SMD': {
                                    'name': 'subslot 0/0 transceiver 17',
                                    'descr': 'GE ZX',
                                    'pid': 'GLC-LH-SMD',
                                    'vid': '001',
                                    'sn': 'EO12004220288'
                                }
                            },
                            '0 transceiver 18': {
                                'GLC-LH-SMD': {
                                    'name': 'subslot 0/0 transceiver 18',
                                    'descr': 'GE ZX',
                                    'pid': 'GLC-LH-SMD',
                                    'vid': '001',
                                    'sn': 'EO11904130602'
                                }
                            },
                            '0 transceiver 19': {
                                'GLC-LH-SMD': {
                                    'name': 'subslot 0/0 transceiver 19',
                                    'descr': 'GE ZX',
                                    'pid': 'GLC-LH-SMD',
                                    'vid': '001',
                                    'sn': 'EO11904130517'
                                }
                            }
                        }
                    }
                }
            },
            'P0': {
                'other': {
                    'ASR-920-PWR-D': {
                        'name': 'Power Supply Module 0',
                        'descr': 'ASR 920 250W DC Power Supply',
                        'pid': 'ASR-920-PWR-D',
                        'vid': 'V01',
                        'sn': 'ART2233FMRV'
                    }
                }
            },
            'P1': {
                'other': {
                    'ASR-920-PWR-D': {
                        'name': 'Power Supply Module 1',
                        'descr': 'ASR 920 250W DC Power Supply',
                        'pid': 'ASR-920-PWR-D',
                        'vid': 'V01',
                        'sn': 'ART2240F3N8'
                    }
                }
            },
            'Fan_Tray': {
                'other': {
                    'ASR-920-FAN-F': {
                        'name': 'Fan Tray',
                        'descr': 'ASR 920 Fan tray',
                        'pid': 'ASR-920-FAN-F',
                        'vid': 'V01',
                        'sn': 'CAT2351V09N'
                    }
                }
            }
        }
    }


    showRedundancy = {
        'red_sys_info': {
            'available_system_uptime': '4 weeks, 20 hours, 35 minutes',
            'switchovers_system_experienced': '0',
            'standby_failures': '0',
            'last_switchover_reason': 'none',
            'hw_mode': 'Simplex',
            'conf_red_mode': 'Non-redundant',
            'oper_red_mode': 'Non-redundant',
            'maint_mode': 'Disabled',
            'communications': 'Down',
            'communications_reason': 'Failure'
        },
        'slot': {
            'slot 6': {
                'curr_sw_state': 'ACTIVE',
                'uptime_in_curr_state': '4 weeks, 20 hours, 35 minutes',
                'image_ver': 'Cisco IOS Software [Fuji], ASR920 Software (PPC_LINUX_IOSD-UNIVERSALK9_NPE-M), Version 16.9.5f, RELEASE SOFTWARE (fc2)',
                'boot': 'asr920-universalk9_npe.16.09.05f.SPA.bin,1;asr920-universalk9_npe.V169_3_SR684942877_7.SPA.bin,1;',
                'config_register': '0x2102'
            }
        }
    }


    ShowIssuStateDetail = {
        'slot': {
            'R0': {
                'issu_in_progress': False
            }
        }
    }


    ShowIssuRollbackTimer = {
        'rollback_timer_state': 'inactive',
        'rollback_timer_reason': 'no ISSU operation is in progress'
    }


    platform_all = {
        'context_manager': {},
        'attributes': None,
        'commands': None,
        'connections': None,
        'chassis': 'ASR-920-24SZ-M',
        'chassis_sn': 'CAT2351V2DV',
        'rtr_type': 'ASR-920-24SZ-M',
        'os': 'iosxe',
        'version': '16.9.5f',
        'image': 'bootflash:asr920-universalk9_npe.16.09.05f.SPA.bin',
        'config_register': '0x2102',
        'main_mem': '896500',
        'dir': 'bootflash:/',
        'redundancy_mode': 'Non-redundant',
        'switchover_reason': 'none',
        'redundancy_communication': False,
        'issu_rollback_timer_state': 'inactive',
        'issu_rollback_timer_reason': 'no ISSU operation is in progress',
        'slot': {
            'rp': {
                '0': {
                    'sn': 'CAT2351V2DV',
                    'subslot': {
                        '0 transceiver 19': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO11904130517'
                        },
                        '0 transceiver 18': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO11904130602'
                        },
                        '0 transceiver 17': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO12004220288'
                        },
                        '0 transceiver 7': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1406136319'
                        },
                        '0 transceiver 6': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1406135212'
                        },
                        '0 transceiver 5': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1407012739'
                        },
                        '0 transceiver 4': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1407012750'
                        },
                        '0 transceiver 0': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO12004220289'
                        }
                    }
                },
                'R0': {
                    'issu': {
                        'in_progress': False
                    }
                }
            },
            'oc': {
                'Fan_Tray': {
                    'name': 'ASR-920-FAN-F',
                    'sn': 'CAT2351V09N'
                },
                'P1': {
                    'name': 'ASR-920-PWR-D',
                    'state': 'ok',
                    'sn': 'ART2240F3N8'
                },
                'P0': {
                    'name': 'ASR-920-PWR-D',
                    'state': 'ok',
                    'sn': 'ART2233FMRV'
                },
                'P2': {
                    'state': 'ok'
                },
                'F0': {
                    'state': 'active'
                },
                'R0': {
                    'state': 'ok, active'
                }
            }
        }
    }


    platform_all_empty_dir = {
        'context_manager': {},
        'attributes': None,
        'commands': None,
        'connections': None,
        'chassis': 'ASR-920-24SZ-M',
        'chassis_sn': 'CAT2351V2DV',
        'rtr_type': 'ASR-920-24SZ-M',
        'os': 'iosxe',
        'version': '16.9.5f',
        'image': 'bootflash:asr920-universalk9_npe.16.09.05f.SPA.bin',
        'config_register': '0x2102',
        'main_mem': '896500',
        'redundancy_mode': 'Non-redundant',
        'switchover_reason': 'none',
        'redundancy_communication': False,
        'issu_rollback_timer_state': 'inactive',
        'issu_rollback_timer_reason': 'no ISSU operation is in progress',
        'slot': {
            'rp': {
                '0': {
                    'sn': 'CAT2351V2DV',
                    'subslot': {
                        '0 transceiver 19': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO11904130517'
                        },
                        '0 transceiver 18': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO11904130602'
                        },
                        '0 transceiver 17': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO12004220288'
                        },
                        '0 transceiver 7': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1406136319'
                        },
                        '0 transceiver 6': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1406135212'
                        },
                        '0 transceiver 5': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1407012739'
                        },
                        '0 transceiver 4': {
                            'name': 'GPB-4324L-L2CD-C',
                            'sn': 'S1407012750'
                        },
                        '0 transceiver 0': {
                            'name': 'GLC-LH-SMD',
                            'sn': 'EO12004220289'
                        }
                    }
                },
                'R0': {
                    'issu': {
                        'in_progress': False
                    }
                }
            },
            'oc': {
                'Fan_Tray': {
                    'name': 'ASR-920-FAN-F',
                    'sn': 'CAT2351V09N'
                },
                'P1': {
                    'name': 'ASR-920-PWR-D',
                    'state': 'ok',
                    'sn': 'ART2240F3N8'
                },
                'P0': {
                    'name': 'ASR-920-PWR-D',
                    'state': 'ok',
                    'sn': 'ART2233FMRV'
                },
                'P2': {
                    'state': 'ok'
                },
                'F0': {
                    'state': 'active'
                },
                'R0': {
                    'state': 'ok, active'
                }
            }
        }
    }
