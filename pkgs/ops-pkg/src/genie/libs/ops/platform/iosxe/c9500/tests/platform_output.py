
class PlatformOutput(object):

    # ==========================================================================
    #                               C9500
    # ==========================================================================

    showVersionC9500 = {
        "version": {
            "version_short": "2019-10-31_17.49_makale",
            "os": "IOS-XE",
            "code_name": "Amsterdam",
            "platform": "Catalyst L3 Switch",
            "image_id": "CAT9K_IOSXE",
            "version": "17.2.20191101:003833",
            "compiled_date": "Thu 31-Oct-19 17:43",
            "compiled_by": "makale",
            "rom": "IOS-XE ROMMON",
            "bootldr_version": "System Bootstrap, Version 17.1.1[FC2], RELEASE SOFTWARE (P)",
            "hostname": "SF2",
            "uptime": "1 day, 18 hours, 48 minutes",
            "returned_to_rom_by": "Reload Command",
            "system_image": "bootflash:/ecr.bin",
            "last_reload_reason": "Reload Command",
            "license_level": "AIR DNA Advantage",
            "next_reload_license_level": "AIR DNA Advantage",
            "smart_licensing_status": "UNREGISTERED/EVAL EXPIRED",
            "chassis": "C9500-32QC",
            "processor_type": "X86",
            "main_mem": "1863083",
            "processor_board_id": "CAT2242L6CG",
            'uptime_this_cp': '1 day, 18 hours, 49 minutes',
            "number_of_intfs": {
                "virtual_ethernet_interfaces": "44",
                "forty_gigabit_ethernet_interfaces": "32",
                "hundred_gigabit_ethernet_interfaces": "16"
            },
            "mem_size": {
                "non_volatile_memory": "32768",
                "physical_memory": "16002848"
            },
            "disks": {
                "bootflash:": {
                    "disk_size": "11161600"
                },
                "crashinfo:": {
                    "disk_size": "1638400"
                }
            },
            "mac_address": "70:b3:17:60:05:00",
            "mb_assembly_num": "47A7",
            "mb_sn": "CAT2242L6CG",
            "model_rev_num": "V02",
            "mb_rev_num": "4",
            "model_num": "C9500-32QC",
            "system_sn": "CAT2242L6CG",
            "curr_config_register": "0x102"
        }
    }

    showDirC9500 = {
                    'dir': {
                        'dir': 'flash:/',
                        'flash:/': {
                            'files': {
                                'bootloader_evt_handle.log': {
                                    'index': '30530',
                                    'permissions': '-rw-',
                                    'size': '16872',
                                    'last_modified_date': 'Apr 10 2017 17:20:51 +00:00',
                                },
                                'core': {
                                    'index': '30531',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Apr 10 2017 00:17:34 +00:00',
                                },
                                '.prst_sync': {
                                    'index': '30532',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Apr 10 2017 14:35:35 +00:00',
                                },
                                '.rollback_timer': {
                                    'index': '30534',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Jan 15 2017 20:53:32 +00:00',
                                },
                                'dc_profile_dir': {
                                    'index': '30535',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Apr 10 2017 17:21:10 +00:00',
                                },
                                'gs_script': {
                                    'index': '30537',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Jan 15 2017 20:53:40 +00:00',
                                },
                                'memleak.tcl': {
                                    'index': '30540',
                                    'permissions': '-rw-',
                                    'size': '65301',
                                    'last_modified_date': 'Apr 10 2017 17:21:27 +00:00',
                                },
                                'boothelper.log': {
                                    'index': '30542',
                                    'permissions': '-rw-',
                                    'size': '66',
                                    'last_modified_date': 'Apr 10 2017 17:21:28 +00:00',
                                },
                                '.installer': {
                                    'index': '30541',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Jan 15 2017 20:54:21 +00:00',
                                },
                                'nvram_config': {
                                    'index': '30539',
                                    'permissions': '-rw-',
                                    'size': '2097152',
                                    'last_modified_date': 'Apr 10 2017 17:25:37 +00:00',
                                },
                                'tools': {
                                    'index': '68689',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Mar 18 2017 20:39:57 +00:00',
                                },
                                'mscfips_post_test.dbg': {
                                    'index': '30544',
                                    'permissions': '-rw-',
                                    'size': '17500',
                                    'last_modified_date': 'Apr 10 2017 17:23:01 +00:00',
                                },
                                'vlan.dat': {
                                    'index': '30548',
                                    'permissions': '-rw-',
                                    'size': '3436',
                                    'last_modified_date': 'Apr 10 2017 11:52:23 +00:00',
                                },
                                'mscfips_post_test.output': {
                                    'index': '30545',
                                    'permissions': '-rw-',
                                    'size': '6856',
                                    'last_modified_date': 'Apr 10 2017 17:23:01 +00:00',
                                },
                                'pnp-tech-time': {
                                    'index': '30546',
                                    'permissions': '-rw-',
                                    'size': '35',
                                    'last_modified_date': 'Apr 10 2017 17:25:57 +00:00',
                                },
                                'ISSUCleanGolden': {
                                    'index': '30550',
                                    'permissions': '-rw-',
                                    'size': '630812001',
                                    'last_modified_date': 'Jan 16 2017 11:05:56 +00:00',
                                },
                                'pnp-tech-discovery-summary': {
                                    'index': '30547',
                                    'permissions': '-rw-',
                                    'size': '21107',
                                    'last_modified_date': 'Apr 10 2017 17:26:38 +00:00',
                                },
                                'onep': {
                                    'index': '30552',
                                    'permissions': 'drwx',
                                    'size': '4096',
                                    'last_modified_date': 'Jan 17 2017 10:21:50 +00:00',
                                },
                            },
                            'bytes_total': '1598627840',
                            'bytes_free': '880939008',
                        },
                    }
                }

    showDirEmptyC9500 = {}

    showPlatformC9500 = {
        "chassis": "C9500-32QC",
        "slot": {
            "1": {
                "name": "C9500-32QC",
                "state": "ok",
                "insert_time": "1d18h",
                "slot": "1",
                "cpld_ver": "19061022",
                "fw_ver": "17.1.1[FC2]",
                "subslot": {
                    "0": {
                        "name": "C9500-32QC",
                        "state": "ok",
                        "insert_time": "1d18h",
                        "subslot": "0"
                    }
                }
            },
            "R0": {
                "name": "C9500-32QC",
                "state": "ok, active",
                "insert_time": "1d18h",
                "slot": "R0"
            },
            "P0": {
                "name": "C9K-PWR-650WAC-R",
                "state": "ok",
                "insert_time": "1d18h",
                "slot": "P0"
            },
            "P2": {
                "name": "C9K-T1-FANTRAY",
                "state": "ok",
                "insert_time": "1d18h",
                "slot": "P2"
            },
            "P3": {
                "name": "C9K-T1-FANTRAY",
                "state": "ok",
                "insert_time": "1d18h",
                "slot": "P3",
            }
        }
    }

    showInventoryC9500 = {
        "index": {
            1: {
                "name": "Chassis",
                "descr": "Cisco Catalyst 9500 Series Chassis",
                "pid": "C9500-32QC",
                "vid": "V01",
                "sn": "CAT2242L6CG"
            },
            2: {
                "name": "Power Supply Module 0",
                "descr": "Cisco Catalyst 9500 Series 650W AC Power Supply",
                "pid": "C9K-PWR-650WAC-R",
                "vid": "V01",
                "sn": "ART2216F3XV"
            },
            3: {
                "name": "Fan Tray 0",
                "descr": "Cisco Catalyst 9500 Series Fan Tray",
                "pid": "C9K-T1-FANTRAY"
            },
            4: {
                "name": "Fan Tray 1",
                "descr": "Cisco Catalyst 9500 Series Fan Tray",
                "pid": "C9K-T1-FANTRAY"
            },
            5: {
                "name": "Slot 1 Supervisor",
                "descr": "Cisco Catalyst 9500 Series Router",
                "pid": "C9500-32QC",
                "vid": "V01",
                "sn": "CAT2242L6CG"
            },
            6: {
                "name": "FortyGigabitEthernet1/0/4",
                "descr": "QSFP 40GE CU3M",
                "pid": "QSFP-H40G-CU3M",
                "vid": "V03",
                "sn": "TED2122K3A4-B"
            },
            7: {
                "name": "FortyGigabitEthernet1/0/8",
                "descr": "QSFP 40GE AOC3M",
                "pid": "QSFP-H40G-AOC3M",
                "vid": "V02",
                "sn": "FIW231301C6-B"
            },
            8: {
                "name": "FortyGigabitEthernet1/0/14",
                "descr": "QSFP 40GE AOC3M",
                "pid": "QSFP-H40G-AOC3M",
                "vid": "V02",
                "sn": "FIW231301BQ-B"
            },
            9: {
                "name": "FortyGigabitEthernet1/0/16",
                "descr": "QSFP 40GE AOC3M",
                "pid": "QSFP-H40G-AOC3M",
                "vid": "V02",
                "sn": "FIW2311023W-A"
            },
            10: {
                "name": "FortyGigabitEthernet1/0/20",
                "descr": "QSFP 40GE AOC3M",
                "pid": "QSFP-H40G-AOC3M",
                "vid": "V02",
                "sn": "FIW231301CF-B"
            },
            11: {
                "name": "HundredGigE1/0/33",
                "descr": "QSFP 100GE SR",
                "pid": "QSFP-100G-SR4-S",
                "vid": "V03",
                "sn": "INL23092488"
            },
            12: {
                "name": "HundredGigE1/0/35",
                "descr": "QSFP 100GE SR",
                "pid": "QSFP-100G-SR4-S",
                "vid": "V03",
                "sn": "AVF2243S0ZT"
            },
            13: {
                "name": "HundredGigE1/0/37",
                "descr": "QSFP 100GE SR",
                "pid": "QSFP-100G-SR4-S",
                "vid": "V03",
                "sn": "INL23092508"
            },
            14: {
                "name": "HundredGigE1/0/38",
                "descr": "QSFP 100GE AOC3M",
                "pid": "QSFP-100G-AOC3M",
                "vid": "V02",
                "sn": "FIW231000BV-A"
            },
            15: {
                "name": "HundredGigE1/0/41",
                "descr": "QSFP 100GE AOC1M",
                "pid": "QSFP-100G-AOC1M",
                "vid": "V03",
                "sn": "INL23100481-B"
            },
            16: {
                "name": "HundredGigE1/0/43",
                "descr": "QSFP 100GE CU2M",
                "pid": "QSFP-100G-CU2M",
                "sn": "APF23030058-B"
            },
            17: {
                "name": "HundredGigE1/0/44",
                "descr": "QSFP 100GE AOC3M",
                "pid": "QSFP-100G-AOC3M",
                "vid": "V02",
                "sn": "FIW23080391-B"
            },
            18: {
                "name": "HundredGigE1/0/45",
                "descr": "QSFP 100GE CU5M",
                "pid": "QSFP-100G-CU5M",
                "sn": "LCC2229G2JT-A"
            },
            19: {
                "name": "HundredGigE1/0/46",
                "descr": "QSFP 100GE AOC3M",
                "pid": "QSFP-100G-AOC3M",
                "vid": "V02",
                "sn": "FIW230802M4-B"
            },
            20: {
                "name": "HundredGigE1/0/47",
                "descr": "QSFP 100GE CU2M",
                "pid": "QSFP-100G-CU2M",
                "sn": "LCC2250H9M1-B"
            },
            21: {
                "name": "HundredGigE1/0/48",
                "descr": "QSFP 100GE SR",
                "pid": "QSFP-100G-SR4-S",
                "vid": "V03",
                "sn": "AVF2243S10A"
            }
        }
    }

    showRedundancyC9500 = {
        "red_sys_info": {
            "available_system_uptime": "1 day, 18 hours, 48 minutes",
            "switchovers_system_experienced": "0",
            "standby_failures": "0",
            "last_switchover_reason": "none",
            "hw_mode": "Simplex",
            "conf_red_mode": "Non-redundant",
            "oper_red_mode": "Non-redundant",
            "maint_mode": "Disabled",
            "communications": "Down",
            "communications_reason": "Failure"
        },
        "slot": {
            "slot 1": {
                "curr_sw_state": "ACTIVE",
                "uptime_in_curr_state": "1 day, 18 hours, 48 minutes",
                "image_ver": "Cisco IOS Software [Amsterdam], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental Version 17.2.20191101:003833 [HEAD-/nobackup/makale/puntject2/polaris 106]",
                "compiled_by": "makale",
                "compiled_date": "Thu 31-Oct-19 17:43",
                "boot": "bootflash:/ecr.bin;",
                "config_register": "0x102",
            }
        }
    }

    ShowIssuStateDetailC9500 = {
        "slot": {
            "R0": {
                "issu_in_progress": False,
                "current_status": "Disabled",
                'previous_operation': 'N/A',
                "system_check": {
                    "platform_issu_support": "No",
                    "standby_online": "No",
                    "autoboot_enabled": "Yes",
                    "sso_mode": "No",
                    "install_boot": "No",
                    "valid_boot_media": "Yes"
                }
            }
        }
    }

    ShowIssuRollbackTimerC9500 = {
        'rollback_timer_reason': 'no ISSU operation is in progress',
        'rollback_timer_state': 'inactive',
    }

    platform_all_C9500 = {
        "chassis": "C9500-32QC",
        "chassis_sn": "CAT2242L6CG",
        "rtr_type": "C9500",
        "os": "iosxe",
        "version": "17.2.20191101:003833",
        "image": "bootflash:/ecr.bin",
        "config_register": "0x102",
        "main_mem": "1863083",
        "dir": "flash:/",
        "redundancy_mode": "Non-redundant",
        "switchover_reason": "none",
        "redundancy_communication": False,
        "issu_rollback_timer_state": "inactive",
        "issu_rollback_timer_reason": "no ISSU operation is in progress",
        "slot": {
            "oc": {
                "P3": {
                    "name": "C9K-T1-FANTRAY",
                    "state": "ok",
                },
                "P2": {
                    "name": "C9K-T1-FANTRAY",
                    "state": "ok",
                },
                "P0": {
                    "name": "C9K-PWR-650WAC-R",
                    "state": "ok",
                    "sn": "ART2216F3XV",
                },
            },
            "rp": {
                "R0": {
                    "name": "C9500-32QC",
                    "state": "ok, active",
                    "issu": {
                        "in_progress": False
                    }
                },
                "1": {
                    "name": "C9500-32QC",
                    "state": "ok",
                    "sn": "CAT2242L6CG",
                    "subslot": {
                        "0": {
                            "name": "C9500-32QC",
                            "state": "ok"
                        },
                        "0/48": {
                            "name": "HundredGigE1/0/48",
                            "sn": "AVF2243S10A"
                        },
                        "0/47": {
                            "name": "HundredGigE1/0/47",
                            "sn": "LCC2250H9M1-B"
                        },
                        "0/46": {
                            "name": "HundredGigE1/0/46",
                            "sn": "FIW230802M4-B"
                        },
                        "0/45": {
                            "name": "HundredGigE1/0/45",
                            "sn": "LCC2229G2JT-A"
                        },
                        "0/44": {
                            "name": "HundredGigE1/0/44",
                            "sn": "FIW23080391-B"
                        },
                        "0/43": {
                            "name": "HundredGigE1/0/43",
                            "sn": "APF23030058-B"
                        },
                        "0/41": {
                            "name": "HundredGigE1/0/41",
                            "sn": "INL23100481-B"
                        },
                        "0/38": {
                            "name": "HundredGigE1/0/38",
                            "sn": "FIW231000BV-A"
                        },
                        "0/37": {
                            "name": "HundredGigE1/0/37",
                            "sn": "INL23092508"
                        },
                        "0/35": {
                            "name": "HundredGigE1/0/35",
                            "sn": "AVF2243S0ZT"
                        },
                        "0/33": {
                            "name": "HundredGigE1/0/33",
                            "sn": "INL23092488"
                        },
                        "0/20": {
                            "name": "FortyGigabitEthernet1/0/20",
                            "sn": "FIW231301CF-B"
                        },
                        "0/16": {
                            "name": "FortyGigabitEthernet1/0/16",
                            "sn": "FIW2311023W-A"
                        },
                        "0/14": {
                            "name": "FortyGigabitEthernet1/0/14",
                            "sn": "FIW231301BQ-B"
                        },
                        "0/8": {
                            "name": "FortyGigabitEthernet1/0/8",
                            "sn": "FIW231301C6-B"
                        },
                        "0/4": {
                            "name": "FortyGigabitEthernet1/0/4",
                            "sn": "TED2122K3A4-B"
                        },
                    },
                    "redundancy_state": "active",
                    "uptime": "1 day, 18 hours, 48 minutes",
                    "system_image": "Cisco IOS Software [Amsterdam], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental Version 17.2.20191101:003833 [HEAD-/nobackup/makale/puntject2/polaris 106]",
                    "boot_image": "bootflash:/ecr.bin;",
                    "config_register": "0x102"
                },
            },
        }
    }

    platform_all_empty_dir_C9500 = {
        "chassis": "C9500-32QC",
        "chassis_sn": "CAT2242L6CG",
        "rtr_type": "C9500",
        "os": "iosxe",
        "version": "17.2.20191101:003833",
        "image": "bootflash:/ecr.bin",
        "config_register": "0x102",
        "main_mem": "1863083",
        "redundancy_mode": "Non-redundant",
        "switchover_reason": "none",
        "redundancy_communication": False,
        "issu_rollback_timer_state": "inactive",
        "issu_rollback_timer_reason": "no ISSU operation is in progress",
        "slot": {
            "oc": {
                "P3": {
                    "name": "C9K-T1-FANTRAY",
                    "state": "ok",
                },
                "P2": {
                    "name": "C9K-T1-FANTRAY",
                    "state": "ok",
                },
                "P0": {
                    "name": "C9K-PWR-650WAC-R",
                    "state": "ok",
                    "sn": "ART2216F3XV",
                },
            },
            "rp": {
                "R0": {
                    "name": "C9500-32QC",
                    "state": "ok, active",
                    "issu": {
                        "in_progress": False
                    }
                },
                "1": {
                    "name": "C9500-32QC",
                    "state": "ok",
                    "sn": "CAT2242L6CG",
                    "subslot": {
                        "0": {
                            "name": "C9500-32QC",
                            "state": "ok"
                        },
                        "0/48": {
                            "name": "HundredGigE1/0/48",
                            "sn": "AVF2243S10A"
                        },
                        "0/47": {
                            "name": "HundredGigE1/0/47",
                            "sn": "LCC2250H9M1-B"
                        },
                        "0/46": {
                            "name": "HundredGigE1/0/46",
                            "sn": "FIW230802M4-B"
                        },
                        "0/45": {
                            "name": "HundredGigE1/0/45",
                            "sn": "LCC2229G2JT-A"
                        },
                        "0/44": {
                            "name": "HundredGigE1/0/44",
                            "sn": "FIW23080391-B"
                        },
                        "0/43": {
                            "name": "HundredGigE1/0/43",
                            "sn": "APF23030058-B"
                        },
                        "0/41": {
                            "name": "HundredGigE1/0/41",
                            "sn": "INL23100481-B"
                        },
                        "0/38": {
                            "name": "HundredGigE1/0/38",
                            "sn": "FIW231000BV-A"
                        },
                        "0/37": {
                            "name": "HundredGigE1/0/37",
                            "sn": "INL23092508"
                        },
                        "0/35": {
                            "name": "HundredGigE1/0/35",
                            "sn": "AVF2243S0ZT"
                        },
                        "0/33": {
                            "name": "HundredGigE1/0/33",
                            "sn": "INL23092488"
                        },
                        "0/20": {
                            "name": "FortyGigabitEthernet1/0/20",
                            "sn": "FIW231301CF-B"
                        },
                        "0/16": {
                            "name": "FortyGigabitEthernet1/0/16",
                            "sn": "FIW2311023W-A"
                        },
                        "0/14": {
                            "name": "FortyGigabitEthernet1/0/14",
                            "sn": "FIW231301BQ-B"
                        },
                        "0/8": {
                            "name": "FortyGigabitEthernet1/0/8",
                            "sn": "FIW231301C6-B"
                        },
                        "0/4": {
                            "name": "FortyGigabitEthernet1/0/4",
                            "sn": "TED2122K3A4-B"
                        },
                    },
                    "redundancy_state": "active",
                    "uptime": "1 day, 18 hours, 48 minutes",
                    "system_image": "Cisco IOS Software [Amsterdam], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental Version 17.2.20191101:003833 [HEAD-/nobackup/makale/puntject2/polaris 106]",
                    "boot_image": "bootflash:/ecr.bin;",
                    "config_register": "0x102"
                },
            },
        }
    }
