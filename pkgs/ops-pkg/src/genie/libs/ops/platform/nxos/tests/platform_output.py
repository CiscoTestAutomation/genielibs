class PlatformOutput(object):
    showVersion = {'platform':
                      {'reason': 'Reset Requested by CLI command reload',
                       'system_version': '6.2(6)',
                       'os': 'NX-OS',
                       'hardware': 
                        {'bootflash': '2007040',
                         'chassis': '("Supervisor Module-2")',
                         'cpu': 'Intel(R) Xeon(R)',
                         'device_name': 'PE1',
                         'memory': '32938744',
                         'model': 'Nexus7000 C7009',
                         'processor_board_id': 'JAF1708AAKL',
                         'slots': '9'}, 
                      'kernel_uptime': 
                        {'days': '0',
                         'hours': '0',
                         'minutes': '53',
                         'seconds': '5'},
                      'software': 
                        {'bios': 'version 2.12.0',
                         'bios_compile_time': '05/29/2013',
                         'kickstart': 'version 8.1(1) [build 8.1(0.129)] [gdb]',
                         'kickstart_compile_time': '4/30/2017 23:00:00 [04/15/2017 ''04:34:05]',
                         'kickstart_image_file': 'slot0:///n7000-s2-kickstart.10.81.0.129.gbin',
                         'system_version': 'version 8.1(1) [build 8.1(0.129)] [gdb]',
                         'system_compile_time': '4/30/2017 23:00:00 [04/15/2017 ''06:43:41]',
                         'system_image_file': 'slot0:///n7000-s2-dk10.34.1.0.129.gbin'}
                      }
                    }


    showInventory = {'name':
                        {'Chassis':
                            {'description': 'Nexus7000 C7009 (9 Slot) Chassis ',
                             'pid': 'N7K-C7009',
                             'slot': 'None',
                             'vid': 'V01',
                             'serial_number': 'JAF1704ARQG'},
                         'Slot 1':
                            {'description': 'Supervisor Module-2',
                             'pid': 'N7K-SUP2',
                             'slot': '1',
                             'vid': 'V01',
                             'serial_number': 'JAF1708AGTH'},
                         'Slot 2':
                            {'description': 'Supervisor Module-2',
                             'pid': 'N7K-SUP2',
                             'slot': '2',
                             'vid': 'V01',
                             'serial_number': 'JAF1708AGQH'},
                         'Slot 3':
                            {'description': '1/10 Gbps Ethernet Module',
                             'pid': 'N7K-F248XP-25E',
                             'slot': '3',
                             'vid': 'V01',
                             'serial_number': 'JAF1717AAND'},
                         'Slot 4':
                            {'description': '10/40 Gbps Ethernet Module',
                             'pid': 'N7K-F312FQ-25',
                             'slot': '4',
                             'vid': 'V01',
                             'serial_number': 'JAE18120FLU'},
                         'Slot 33':
                            {'description': 'Nexus7000 C7009 (9 Slot) Chassis Power Supply',
                             'pid': 'N7K-AC-6.0KW',
                             'slot': '33',
                             'vid': 'V03',
                             'serial_number': 'DTM171300QB'},
                         'Slot 35':
                            {'description': 'Nexus7000 C7009 (9 Slot) Chassis Fan Module',
                             'pid': 'N7K-C7009-FAN',
                             'slot': '35',
                             'vid': 'V01',
                             'serial_number': 'JAF1702AEBE'}
                        }
                    }

    showInstallActive = {'boot_images':
                              {'kickstart_image': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                               'system_image': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin'},
                            'active_packages':
                              {'active_package_module_0':
                                {'active_package_name': 'n7700-s2-dk10.1.2.0.D1.1.CSCuo7721.bin'},
                               'active_package_module_3': 
                                {'active_package_name': 'n7700-s2-dk10.1.2.0.D1.1.CSCuo7721.bin'}
                              }
                            }

    showSystemRedundancyStatus = {'redundancy_mode':
                            {'administrative': 'HA',
                             'operational': 'HA'},
                            'supervisor_1':
                              {'redundancy_state': 'Active',
                               'supervisor_state': 'Active',
                               'internal_state':'Active with HA standby'},
                            'supervisor_2':
                              {'redundancy_state': 'Standby',
                               'supervisor_state': 'HA standby',
                               'internal_state':'HA standby'},
                          }

    showRedundancyStatus = {'redundancy_mode':
                              {'administrative': 'HA',
                               'operational': 'HA'},
                            'supervisor_1':
                              {'redundancy_state': 'Active',
                               'supervisor_state': 'Active',
                               'internal_state':'Active with HA standby'},
                            'supervisor_2':
                              {'redundancy_state': 'Standby',
                               'supervisor_state': 'HA standby',
                               'internal_state':'HA standby'},
                            'system_start_time': 'Fri Apr 21 01:53:24 2017',
                            'system_uptime': '0 days, 7 hours, 57 minutes, 30 seconds',
                            'kernel_uptime': '0 days, 8 hours, 0 minutes, 56 seconds',
                            'active_supervisor_time': '0 days, 7 hours, 57 minutes, 30 seconds'}

    showBoot = {'current_boot_variable':
                    {'sup_number':
                        {'sup-1':
                            {'kickstart_variable': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                             'system_variable': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin',
                             'boot_poap':'Disabled'},
                         'sup-2':
                            {'kickstart_variable': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                             'system_variable': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin',
                             'boot_poap':'Disabled'}
                        }
                    },
                'next_reload_boot_variable':
                    {'sup_number':
                        {'sup-1':
                            {'kickstart_variable': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                             'system_variable': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin',
                             'boot_poap':'Disabled'},
                         'sup-2':
                            {'kickstart_variable': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                             'system_variable': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin',
                             'boot_poap':'Disabled'}
                        }
                    }
                }

    showBootEmpty = {}

    showModule = {'slot':
                    {'rp':
                      {'1':
                        {'Supervisor Module-2':
                          {'ports': '0',
                           'model': 'N7K-SUP2',
                           'status': 'active',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '1.0',
                           'mac_address': '84-78-ac-0f-c4-cd to 84-78-ac-0f-c4-df',
                           'serial_number': 'JAF1708AGTH',
                           'online_diag_status': 'Pass'}
                        },
                      '2':
                        {'Supervisor Module-2':
                          {'ports': '0',
                           'model': 'N7K-SUP2',
                           'status': 'ha-standby',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '1.0',
                           'mac_address': '84-78-ac-0f-b9-00 to 84-78-ac-0f-b9-12',
                           'serial_number': 'JAF1708AGQH',
                           'online_diag_status': 'Pass'}
                        }
                      },
                    'lc':
                      {'3':
                        {'1/10 Gbps Ethernet Module':
                          {'ports': '48',
                           'model': 'N7K-F248XP-25E',
                           'status': 'ok',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '1.0',
                           'mac_address': '84-78-ac-18-dd-30 to 84-78-ac-18-dd-63',
                           'serial_number': 'JAF1717AAND',
                           'online_diag_status': 'Pass'}
                        },
                      '4':
                        {'10/40 Gbps Ethernet Module':
                          {'ports': '12',
                           'model': 'N7K-F312FQ-25',
                           'status': 'ok',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '1.0',
                           'mac_address': '54-4a-00-ad-19-40 to 54-4a-00-ad-19-7b',
                           'serial_number': 'JAE18120FLU',
                           'online_diag_status': 'Pass'}
                        },
                      '6':
                        {'10 Gbps Ethernet XL Module':
                          {'ports': '32',
                           'model': 'N7K-M132XP-12L',
                           'status': 'ok',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '2.0',
                           'mac_address': 'bc-16-65-54-af-64 to bc-16-65-54-af-87',
                           'serial_number': 'JAF1719AHMB',
                           'online_diag_status': 'Pass'}
                        },
                      '7':
                        {'10 Gbps Ethernet Module':
                          {'ports': '24',
                           'model': 'N7K-M224XP-23L',
                           'status': 'ok',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '1.0',
                           'mac_address': 'd8-67-d9-0e-91-c8 to d8-67-d9-0e-91-e3',
                           'serial_number': 'JAF1641APPF',
                           'online_diag_status': 'Pass'}
                        },
                      '8':
                        {'10/100/1000 Mbps Ethernet XL Module':
                          {'ports': '48',
                           'model': 'N7K-M148GT-11L',
                           'status': 'ok',
                           'software': '8.3(0)CV(0.658)',
                           'hardware': '2.1',
                           'mac_address': 'bc-16-65-3a-b8-d0 to bc-16-65-3a-b9-03',
                           'serial_number': 'JAF1717BEAT',
                           'online_diag_status': 'Pass'}
                        }
                      }
                    },
                'xbar':
                  {'1':
                      {'ports': '0',
                       'module_type': 'Fabric Module 2',
                       'model': 'N7K-C7009-FAB-2',
                       'status': 'ok',
                       'software': 'NA',
                       'hardware': '3.1',
                       'mac_address': 'NA',
                       'serial_number': 'JAF1705AEEF'},
                  '2':
                      {'ports': '0',
                       'module_type': 'Fabric Module 2',
                       'model': 'N7K-C7009-FAB-2',
                       'status': 'ok',
                       'software': 'NA',
                       'hardware': '3.1',
                       'mac_address': 'NA',
                       'serial_number': 'JAF1705BFBM'},
                  '3':
                      {'ports': '0',
                       'module_type': 'Fabric Module 2',
                       'model': 'N7K-C7009-FAB-2',
                       'status': 'ok',
                       'software': 'NA',
                       'hardware': '3.1',
                       'mac_address': 'NA',
                       'serial_number': 'JAF1705AELK'},
                  '4':
                      {'ports': '0',
                       'module_type': 'Fabric Module 2',
                       'model': 'N7K-C7009-FAB-2',
                       'status': 'ok',
                       'software': 'NA',
                       'hardware': '3.1',
                       'mac_address': 'NA',
                       'serial_number': 'JAF1705BFCF'},
                  '5':
                      {'ports': '0',
                       'module_type': 'Fabric Module 2',
                       'model': 'N7K-C7009-FAB-2',
                       'status': 'ok',
                       'software': 'NA',
                       'hardware': '3.1',
                       'mac_address': 'NA',
                       'serial_number': 'JAF1704APQH'}
                  }
              }

    directory = {'files':
                    {'.patch/': 
                        {'size': '4096', 'date': 'Apr 20 2017', 'time': '10:23:05'},
                     '20170202_074746_poap_7537_init.log': 
                        {'size': '1398', 'date': 'Feb 02 2017', 'time': '00:48:18'},
                     'ethpm_act_logs.log': 
                        {'size': '251599', 'date': 'Mar 15 2017', 'time': '10:35:50'},
                     'ethpm_im_tech.log': 
                        {'size': '1171318', 'date': 'Mar 15 2017', 'time': '10:35:55'},
                     'ethpm_mts_details.log': 
                        {'size': '3837', 'date': 'Mar 15 2017', 'time': '10:35:50'},
                     'ethpm_syslogs.log': 
                        {'size': '81257', 'date': 'Mar 15 2017', 'time': '10:35:50'},
                     'ethpm_tech.log': 
                        {'size': '3930383', 'date': 'Mar 15 2017', 'time': '10:35:55'},
                     'fault-management-logs/': 
                        {'size': '24576', 'date': 'Apr 21 2017', 'time': '04:18:28'},
                     'lost+found/': 
                        {'size': '4096', 'date': 'Nov 23 2016', 'time': '08:25:40'},
                     'n7000-s2-debug-sh.10.81.0.125.gbin': 
                        {'size': '4073830', 'date': 'Apr 20 2017', 'time': '10:19:08'},
                     'virtual-instance-stby-sync/': 
                        {'size': '4096', 'date': 'Apr 20 2017', 'time': '10:28:55'}
                    },
                'dir': 'bootflash:',
                'disk_used_space': '108449792',
                'disk_free_space': '1674481664',
                'disk_total_space': '1782931456'
              }

    showVdcDetail = {'vdc':
                        {'1':
                          {'name': 'PE1',
                           'state': 'active',
                           'mac_address': '84:78:ac:5a:86:c1',
                           'ha_policy': 'RELOAD',
                           'dual_sup_ha_policy': 'SWITCHOVER',
                           'boot_order': '1',
                           'cpu_share': '5',
                           'cpu_share_percentage': '33%',
                           'create_time': 'Fri Apr 28 03:36:26 2017',
                           'reload_count': '0',
                           'uptime': '0 day(s), 10 hour(s), 35 minute(s), 47 second(s)',
                           'restart_count': '1',
                           'restart_time': 'Fri Apr 28 03:36:26 2017',
                           'type': 'Ethernet',
                           'supported_linecards': 'f3'},
                        '2':
                          {'name': 'PE2',
                           'state': 'active',
                           'mac_address': '84:78:ac:5a:86:c2',
                           'ha_policy': 'RESTART',
                           'dual_sup_ha_policy': 'SWITCHOVER',
                           'boot_order': '1',
                           'cpu_share': '5',
                           'cpu_share_percentage': '33%',
                           'create_time': 'Fri Apr 28 03:48:01 2017',
                           'reload_count': '0',
                           'uptime': '0 day(s), 10 hour(s), 25 minute(s), 2 second(s)',
                           'restart_count': '1',
                           'restart_time': 'Fri Apr 28 03:48:01 2017',
                           'type': 'Ethernet',
                           'supported_linecards': 'f3'},
                        '3':
                          {'name': 'CORE',
                           'state': 'active',
                           'mac_address': '84:78:ac:5a:86:c3',
                           'ha_policy': 'RESTART',
                           'dual_sup_ha_policy': 'SWITCHOVER',
                           'boot_order': '1',
                           'cpu_share': '5',
                           'cpu_share_percentage': '33%',
                           'create_time': 'Fri Apr 28 03:49:33 2017',
                           'reload_count': '0',
                           'uptime': '0 day(s), 10 hour(s), 23 minute(s), 39 second(s)',
                           'restart_count': '1',
                           'restart_time': 'Fri Apr 28 03:49:33 2017',
                           'type': 'Ethernet',
                           'supported_linecards': 'f3'}
                        }
                    }

    showVdcCurrent = {'current_vdc':
                        {'id': '1',
                         'name': 'PE1'}
                     }

    showVdcMembershipStatus = {'virtual_device':
                                {'0':
                                    {'membership':
                                        {'Unallocated':
                                            {'Eth3/1':
                                              {'vd_ms_name': 'Eth3/1',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'},
                                             'Eth3/2':
                                              {'vd_ms_name': 'Eth3/2',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'}
                                            }
                                        }
                                    },
                                '1':
                                    {'membership':
                                        {'PE1':
                                            {'Eth4/5':
                                              {'vd_ms_name': 'Eth4/5',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'},
                                             'Eth4/6':
                                              {'vd_ms_name': 'Eth4/6',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'}
                                            }
                                        }
                                    },
                                '2':
                                    {'membership':
                                        {'PE2':
                                            {'Eth4/3':
                                              {'vd_ms_name': 'Eth4/3',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'},
                                             'Eth4/4':
                                              {'vd_ms_name': 'Eth4/4',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'}
                                            }
                                        }
                                    },
                                '3':
                                    {'membership':
                                        {'CORE':
                                            {'Eth4/1':
                                              {'vd_ms_name': 'Eth4/1',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'},
                                             'Eth4/2(b)':
                                              {'vd_ms_name': 'Eth4/2(b)',
                                               'vd_ms_status': 'OK',
                                               'vd_ms_type': 'Ethernet'}
                                            }
                                        }
                                    }
                                }
                            }

    slot = {
       "oc": {
          "1": {
             "ports": "0",
             "module_type": "Fabric Module 2",
             "model": "N7K-C7009-FAB-2",
             "status": "ok",
             "software": "NA",
             "hardware": "3.1",
             "mac_address": "NA",
             "serial_number": "JAF1705AEEF",
             "state": "ok",
             "name": "Fabric Module 2"
          },
          "2": {
             "ports": "0",
             "module_type": "Fabric Module 2",
             "model": "N7K-C7009-FAB-2",
             "status": "ok",
             "software": "NA",
             "hardware": "3.1",
             "mac_address": "NA",
             "serial_number": "JAF1705BFBM",
             "state": "ok",
             "name": "Fabric Module 2"
          },
          "3": {
             "ports": "0",
             "module_type": "Fabric Module 2",
             "model": "N7K-C7009-FAB-2",
             "status": "ok",
             "software": "NA",
             "hardware": "3.1",
             "mac_address": "NA",
             "serial_number": "JAF1705AELK",
             "state": "ok",
             "name": "Fabric Module 2"
          },
          "4": {
             "ports": "0",
             "module_type": "Fabric Module 2",
             "model": "N7K-C7009-FAB-2",
             "status": "ok",
             "software": "NA",
             "hardware": "3.1",
             "mac_address": "NA",
             "serial_number": "JAF1705BFCF",
             "state": "ok",
             "name": "Fabric Module 2"
          },
          "5": {
             "ports": "0",
             "module_type": "Fabric Module 2",
             "model": "N7K-C7009-FAB-2",
             "status": "ok",
             "software": "NA",
             "hardware": "3.1",
             "mac_address": "NA",
             "serial_number": "JAF1704APQH",
             "state": "ok",
             "name": "Fabric Module 2"
          },
          "35": {
             "name": "Nexus7000 C7009 (9 Slot) Chassis Fan Module",
             "sn": "JAF1702AEBE"
          },
          "33": {
             "name": "Nexus7000 C7009 (9 Slot) Chassis Power Supply",
             "sn": "DTM171300QB"
          }
       },
       "rp": {
          "2": {
             "name": "N7K-SUP2",
             "state": "ha-standby",
             "sn": "JAF1708AGQH",
             "redundancy_state": "ha-standby",
             "rp_boot_image": "slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin",
             "rp_kickstart_boot_image": "slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin",
             "rp_uptime": 28650
          },
          "1": {
             "name": "N7K-SUP2",
             "state": "active",
             "sn": "JAF1708AGTH",
             "redundancy_state": "active",
             "rp_boot_image": "slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin",
             "rp_kickstart_boot_image": "slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin",
             "rp_uptime": 28650
          }
       },
       "lc": {
          "4": {
             "name": "10/40 Gbps Ethernet Module",
             "sn": "JAE18120FLU",
             "state": "ok"
          },
          "3": {
             "name": "1/10 Gbps Ethernet Module",
             "sn": "JAF1717AAND",
             "state": "ok"
          }
       }
    }
    virtual_device = {'2': 
                        {'vd_name': 'PE2', 'membership': {'Eth4/4': {'status': 'OK', 'type': 'Ethernet'}, 'Eth4/3': {'status': 'OK', 'type': 'Ethernet'}}, 'vd_status': 'active'}, 
                      '3': 
                        {'vd_name': 'CORE', 'membership': {'Eth4/1': {'status': 'OK', 'type': 'Ethernet'}, 'Eth4/2(b)': {'status': 'OK', 'type': 'Ethernet'}}, 'vd_status': 'active'}, 
                      '1': 
                        {'vd_name': 'PE1', 'membership': {'Eth4/5': {'status': 'OK', 'type': 'Ethernet'}, 'Eth4/6': {'status': 'OK', 'type': 'Ethernet'}}, 'vd_status': 'active'}, 
                      '0': 
                        {'membership': {'Eth3/2': {'status': 'OK', 'type': 'Ethernet'}, 'Eth3/1': {'status': 'OK', 'type': 'Ethernet'}}}
                    }

    platform_all = {'attributes': None,
                     # 'callables': {},
                     'chassis': 'Nexus7000 C7009 (9 Slot) Chassis',
                     'chassis_sn': 'JAF1704ARQG',
                     'connections': None,
                     'context_manager': {},
                     # 'device': <Device aDevice at 0xf7111f2c>,
                     # 'diff_ignore': deque(['maker', 'callables', 'device']),
                     'dir': 'bootflash:',
                     'disk_free_space': '1674481664',
                     'disk_total_space': '1782931456',
                     'disk_used_space': '108449792',
                     'image': 'slot0:///n7000-s2-dk10.34.1.0.129.gbin',
                     'installed_packages': 'n7700-s2-dk10.1.2.0.D1.1.CSCuo7721.bin',
                     'kickstart_image': 'slot0:///n7000-s2-kickstart.10.81.0.129.gbin',
                     'kickstart_version': 'version 8.1(1) [build 8.1(0.129)] [gdb]',
                     'main_mem': '32938744',
                     # 'maker': <genie.ops.base.maker.Maker object at 0xf712414c>,
                     'os': 'NX-OS',
                     'rtr_type': 'Nexus7000 C7009',
                     'rp_uptime': 28650,
                     'slot': {'lc': {'3': {'name': '1/10 Gbps Ethernet Module',
                                           'sn': 'JAF1717AAND',
                                           'state': 'ok'},
                                     '4': {'name': '10/40 Gbps Ethernet Module',
                                           'sn': 'JAE18120FLU',
                                           'state': 'ok'}},
                              'oc': {'33': {'name': 'Nexus7000 C7009 (9 Slot) Chassis Power '
                                                    'Supply',
                                            'sn': 'DTM171300QB'},
                                     '35': {'name': 'Nexus7000 C7009 (9 Slot) Chassis Fan '
                                                    'Module',
                                            'sn': 'JAF1702AEBE'}},
                              'rp': {'1': {'name': 'N7K-SUP2',
                                           'redundancy_state': 'active',
                                           'rp_boot_image': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin',
                                           'rp_kickstart_boot_image': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                                           'rp_uptime': 28650,
                                           'sn': 'JAF1708AGTH',
                                           'state': 'active'},
                                     '2': {'name': 'N7K-SUP2',
                                           'redundancy_state': 'ha-standby',
                                           'rp_boot_image': 'slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin',
                                           'rp_kickstart_boot_image': 'slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin',
                                           'rp_uptime': 28650,
                                           'sn': 'JAF1708AGQH',
                                           'state': 'ha-standby'}}},
                     'version': 'version 8.1(1) [build 8.1(0.129)] [gdb]',
                     'virtual_device': {'0': {'membership': {'Eth3/1': {'status': 'OK',
                                                                        'type': 'Ethernet'},
                                                             'Eth3/2': {'status': 'OK',
                                                                        'type': 'Ethernet'}}},
                                        '1': {'membership': {'Eth4/5': {'status': 'OK',
                                                                        'type': 'Ethernet'},
                                                             'Eth4/6': {'status': 'OK',
                                                                        'type': 'Ethernet'}},
                                              'vd_name': 'PE1',
                                              'vd_status': 'active'},
                                        '2': {'membership': {'Eth4/3': {'status': 'OK',
                                                                        'type': 'Ethernet'},
                                                             'Eth4/4': {'status': 'OK',
                                                                        'type': 'Ethernet'}},
                                              'vd_name': 'PE2',
                                              'vd_status': 'active'},
                                        '3': {'membership': {'Eth4/1': {'status': 'OK',
                                                                        'type': 'Ethernet'},
                                                             'Eth4/2(b)': {'status': 'OK',
                                                                           'type': 'Ethernet'}},
                                              'vd_name': 'CORE',
                                              'vd_status': 'active'}}}
