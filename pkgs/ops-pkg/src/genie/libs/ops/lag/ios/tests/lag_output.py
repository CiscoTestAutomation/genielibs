'''Lag Genie Ops Object Outputs for IOS'''


class LagOutput(object):

    ShowLacpSysId = {
        'system_id_mac': '001e.49af.8c00',
        'system_priority': 32768,
    }

    ShowLacpCounters = {
        'interfaces': {
            'Port-channel1': {
                'name': 'Port-channel1',
                'protocol': 'lacp',
                'members': {
                    'GigabitEthernet2': {
                        'interface': 'GigabitEthernet2',
                        'counters': {
                            'lacp_in_pkts': 22,
                            'lacp_out_pkts': 27,
                            'lacp_errors': 0,
                            'marker_in_pkts': 0,
                            'marker_out_pkts': 0,
                            'marker_response_in_pkts': 0,
                            'marker_response_out_pkts': 0,
                        },
                    },
                    'GigabitEthernet3': {
                        'interface': 'GigabitEthernet3',
                        'counters': {
                            'lacp_in_pkts': 21,
                            'lacp_out_pkts': 24,
                            'lacp_errors': 0,
                            'marker_in_pkts': 0,
                            'marker_out_pkts': 0,
                            'marker_response_in_pkts': 0,
                            'marker_response_out_pkts': 0,
                        },
                    },
                }
            },
            'Port-channel2': {
               'name': 'Port-channel2',
               'protocol': 'lacp',
               'members': {
                    'GigabitEthernet4': {
                        'interface': 'GigabitEthernet4',
                        'counters': {
                            'lacp_in_pkts': 31,
                            'lacp_out_pkts': 24,
                            'lacp_errors': 0,
                            'marker_in_pkts': 0,
                            'marker_out_pkts': 0,
                            'marker_response_in_pkts': 0,
                            'marker_response_out_pkts': 0,
                        },
                    },
                    'GigabitEthernet5': {
                        'interface': 'GigabitEthernet5',
                        'counters': {
                            'lacp_in_pkts': 10,
                            'lacp_out_pkts': 14,
                            'lacp_errors': 0,
                            'marker_in_pkts': 0,
                            'marker_out_pkts': 0,
                            'marker_response_in_pkts': 0,
                            'marker_response_out_pkts': 0,
                        },
                    },
                   'GigabitEthernet6': {
                       'interface': 'GigabitEthernet6',
                       'counters': {
                           'lacp_in_pkts': 11,
                           'lacp_out_pkts': 13,
                           'lacp_errors': 0,
                           'marker_in_pkts': 0,
                           'marker_out_pkts': 0,
                           'marker_response_in_pkts': 0,
                           'marker_response_out_pkts': 0,
                       },
                   },
               },
           },
        },
    }

    ShowEtherchannelSummary = {
        'number_of_lag_in_use': 2,
        'number_of_aggregators': 2,
        'interfaces': {
            'Port-channel1': {
                'name': 'Port-channel1',
                'bundle_id': 1,
                'protocol': 'lacp',
                'flags': 'RU',
                'oper_status': 'up',
                'members': {
                    'GigabitEthernet2': {
                        'interface': 'GigabitEthernet2',
                        'flags': 'bndl',
                        'bundled': True,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel1"
                        },
                        },
                    'GigabitEthernet3': {
                        'interface': 'GigabitEthernet3',
                        'flags': 'bndl',
                        'bundled': True,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel1"
                        },
                    },
                },
                'port_channel': {
                    'port_channel_member': True,
                    'port_channel_member_intfs': ['GigabitEthernet2', 'GigabitEthernet3'],
                }
            },
            'Port-channel2': {
                'name': 'Port-channel2',
                'bundle_id': 2,
                'protocol': 'lacp',
                'flags': 'RU',
                'oper_status': 'up',
                'members': {
                    'GigabitEthernet4': {
                        'interface': 'GigabitEthernet4',
                        'flags': 'bndl',
                        'bundled': True,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel2"
                        },
                    },
                    'GigabitEthernet5': {
                        'interface': 'GigabitEthernet5',
                        'flags': 'hot-sby',
                        'bundled': False,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel2"
                        },
                    },
                    'GigabitEthernet6': {
                        'interface': 'GigabitEthernet6',
                        'flags': 'bndl',
                        'bundled': True,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel2"
                        },
                    },
                },
                'port_channel': {
                    'port_channel_member': True,
                    'port_channel_member_intfs': ['GigabitEthernet4', 'GigabitEthernet5', 'GigabitEthernet6'],
                }
            },
        },
    }

    ShowLacpInternal = {
        'interfaces': {
            'Port-channel1': {
                'name': 'Port-channel1',
                'protocol': 'lacp',
                'members': {
                    'GigabitEthernet2': {
                        'interface': 'GigabitEthernet2',
                        'oper_key': 1,
                        'admin_key': 1,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'activity': 'auto',
                        'state': 'bndl',
                        'bundled': True,
                        'port_state': 61,
                        },
                    'GigabitEthernet3': {
                        'interface': 'GigabitEthernet3',
                        'oper_key': 1,
                        'admin_key': 1,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'activity': 'auto',
                        'state': 'bndl',
                        'bundled': True,
                        'port_state': 61,
                    },
                },
            },
            'Port-channel2': {
                'name': 'Port-channel2',
                'protocol': 'lacp',
                'members': {
                    'GigabitEthernet4': {
                        'interface': 'GigabitEthernet4',
                        'oper_key': 2,
                        'admin_key': 2,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'state': 'bndl',
                        'activity': 'auto',
                        'bundled': True,
                        'port_state': 61,
                    },
                    'GigabitEthernet5': {
                        'interface': 'GigabitEthernet5',
                        'oper_key': 2,
                        'admin_key': 2,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'activity': 'auto',
                        'state': 'bndl',
                        'bundled': True,
                        'port_state': 61,
                    },
                    'GigabitEthernet6': {
                        'interface': 'GigabitEthernet6',
                        'oper_key': 2,
                        'admin_key': 2,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'activity': 'auto',
                        'state': 'bndl',
                        'bundled': True,
                        'port_state': 61,
                    },
                },
            },
        }
    }

    ShowLacpNeighbor = {
        'interfaces': {
            'Port-channel1': {
                'name': 'Port-channel1',
                'protocol': 'lacp',
                'members': {
                    'GigabitEthernet2': {
                        'interface': 'GigabitEthernet2',
                        'oper_key': 1,
                        'admin_key': 0,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'activity' : 'active',
                        'partner_id': '001e.49e6.bc00',
                        'age': 25,
                        'port_state': 61
                        },
                    'GigabitEthernet3': {
                        'interface': 'GigabitEthernet3',
                        'oper_key': 1,
                        'admin_key': 0,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SA',
                        'activity': 'active',
                        'port_state': 61,
                        'partner_id': '001e.49e6.bc00',
                        'age': 19,
                    },
                },
            },
            'Port-channel2': {
                'name': 'Port-channel2',
                'protocol': 'lacp',
                'members': {
                    'GigabitEthernet4': {
                        'interface': 'GigabitEthernet4',
                        'oper_key': 2,
                        'admin_key': 0,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SP',
                        'port_state': 60,
                        'activity': 'passive',
                        'partner_id': '001e.49e6.bc00',
                        'age': 15,
                    },
                    'GigabitEthernet5': {
                        'interface': 'GigabitEthernet5',
                        'oper_key': 2,
                        'admin_key': 0,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SP',
                        'port_state': 60,
                        'activity': 'passive',
                        'partner_id': '001e.49e6.bc00',
                        'age': 1
                    },
                    'GigabitEthernet6': {
                        'interface': 'GigabitEthernet6',
                        'oper_key': 2,
                        'admin_key': 0,
                        'port_num': 1,
                        'lacp_port_priority': 32768,
                        'flags': 'SP',
                        'port_state': 60,
                        'activity': 'passive',
                        'partner_id': '001e.49e6.bc00',
                        'age': 0
                    },
                },
            },
        }
    }

    ShowPagpCounters = {
        'interfaces': {
            'Port-channel1': {
                'name': 'Port-channel1',
                'protocol': 'pagp',
                'members': {
                    'GigabitEthernet0/1': {
                        'interface': 'GigabitEthernet0/1',
                        'counters': {
                            'information_in_pkts': 52,
                            'information_out_pkts': 60,
                            'pagp_errors': 0,
                            'flush_in_pkts': 0,
                            'flush_out_pkts': 0,
                            },
                        },
                    'GigabitEthernet0/2': {
                        'interface': 'GigabitEthernet0/2',
                        'counters': {
                            'information_in_pkts': 52,
                            'information_out_pkts': 59,
                            'pagp_errors': 0,
                            'flush_in_pkts': 0,
                            'flush_out_pkts': 0,
                        },
                    },
                },
            },
            'Port-channel2': {
                'name': 'Port-channel2',
                'protocol': 'pagp',
                'members': {
                    'GigabitEthernet0/3': {
                        'interface': 'GigabitEthernet0/3',
                        'counters': {
                            'information_in_pkts': 11,
                            'information_out_pkts': 21,
                            'pagp_errors': 0,
                            'flush_in_pkts': 0,
                            'flush_out_pkts': 0,
                        },
                    },
                    'GigabitEthernet1/0': {
                        'interface': 'GigabitEthernet1/0',
                        'counters': {
                            'information_in_pkts': 11,
                            'information_out_pkts': 19,
                            'pagp_errors': 0,
                            'flush_in_pkts': 0,
                            'flush_out_pkts': 0,
                        },
                    },
                    'GigabitEthernet1/1': {
                        'interface': 'GigabitEthernet1/1',
                        'counters': {
                            'information_in_pkts': 10,
                            'information_out_pkts': 19,
                            'pagp_errors': 0,
                            'flush_in_pkts': 0,
                            'flush_out_pkts': 0,
                        },
                    },

                },
            },
        }
    }

    ShowPagpNeighbor = {
        "interfaces": {
            "Port-channel14": {
                "members": {
                    "GigabitEthernet1/0/7": {
                        "age": 22,
                        "flags": "SC",
                        "group_cap": "E0001",
                        "interface": "GigabitEthernet1/0/7",
                        "partner_id": "ecbd.1d09.5680",
                        "partner_name": "R4",
                        "partner_port": "GigabitEthernet1/0/7"
                    },
                    "GigabitEthernet1/0/8": {
                        "age": 16,
                        "flags": "SC",
                        "group_cap": "E0001",
                        "interface": "GigabitEthernet1/0/8",
                        "partner_id": "ecbd.1d09.5680",
                        "partner_name": "R4",
                        "partner_port": "GigabitEthernet1/0/8"
                    },
                    "GigabitEthernet1/0/9": {
                        "age": 18,
                        "flags": "SC",
                        "group_cap": "E0001",
                        "interface": "GigabitEthernet1/0/9",
                        "partner_id": "ecbd.1d09.5680",
                        "partner_name": "R4",
                        "partner_port": "GigabitEthernet1/0/9"
                    }
                },
                "name": "Port-channel14",
                "protocol": "pagp"
            }
        }
    }

    ShowPagpInternal = {
        'interfaces': {
            'Port-channel1': {
                'name': 'Port-channel1',
                'protocol': 'pagp',
                'members': {
                    'GigabitEthernet0/1': {
                        'interface': 'GigabitEthernet0/1',
                        'group_ifindex': 8,
                        'partner_count': 1,
                        'hello_interval': 30,
                        'timers': 'H',
                        'pagp_port_priority': 128,
                        'flags': 'SC',
                        'state': 'U6/S7',
                        'learn_method': 'any',
                    },
                    'GigabitEthernet0/2': {
                        'interface': 'GigabitEthernet0/2',
                        'group_ifindex': 8,
                        'partner_count': 1,
                        'hello_interval': 30,
                        'timers': 'H',
                        'pagp_port_priority': 128,
                        'flags': 'SC',
                        'state': 'U6/S7',
                        'learn_method': 'any',
                    },
                },
            },
            'Port-channel2': {
                'name': 'Port-channel2',
                'protocol': 'pagp',
                'members': {
                    'GigabitEthernet0/3': {
                        'interface': 'GigabitEthernet0/3',
                        'group_ifindex': 11,
                        'partner_count': 1,
                        'hello_interval': 30,
                        'timers': 'H',
                        'pagp_port_priority': 128,
                        'flags': 'SC',
                        'state': 'U6/S7',
                        'learn_method': 'any',
                    },
                    'GigabitEthernet1/0': {
                        'interface': 'GigabitEthernet1/0',
                        'group_ifindex': 11,
                        'partner_count': 1,
                        'hello_interval': 30,
                        'timers': 'H',
                        'pagp_port_priority': 128,
                        'flags': 'SC',
                        'state': 'U6/S7',
                        'learn_method': 'any',
                    },
                    'GigabitEthernet1/1': {
                        'interface': 'GigabitEthernet1/1',
                        'group_ifindex': 11,
                        'partner_count': 1,
                        'hello_interval': 30,
                        'timers': 'H',
                        'pagp_port_priority': 128,
                        'flags': 'SC',
                        'state': 'U6/S7',
                        'learn_method': 'any',
                    },
                },
            },
        }
    }

    Lag_info = {
        "system_priority": 32768,
        "interfaces": {
            "Port-channel1": {
                "name": "Port-channel1",
                "oper_status": "up",
                "bundle_id": 1,
                "protocol": "lacp",
                "members": {
                    "GigabitEthernet2": {
                            "lacp_port_priority": 32768,
                            "counters": {
                                "lacp_in_pkts": 22,
                                "lacp_errors": 0,
                                "lacp_out_pkts": 27
                            },
                            "interface": "GigabitEthernet2",
                            "bundled": True,
                            "port_num": 1,
                            "activity": "active",
                            "partner_id": "001e.49e6.bc00",
                            "bundle_id": 1,
                            "age": 25,
                            "oper_key": 1
                    },
                    "GigabitEthernet3": {
                            "lacp_port_priority": 32768,
                            "counters": {
                                "lacp_in_pkts": 21,
                                "lacp_errors": 0,
                                "lacp_out_pkts": 24
                            },
                            "interface": "GigabitEthernet3",
                            "bundled": True,
                            "port_num": 1,
                            "activity": "active",
                            "partner_id": "001e.49e6.bc00",
                            "bundle_id": 1,
                            "age": 19,
                            "oper_key": 1
                    },
                    "GigabitEthernet0/2": {
                            "bundle_id": 1,
                            "pagp_port_priority": 128
                    },
                    "GigabitEthernet0/1": {
                            "bundle_id": 1,
                            "pagp_port_priority": 128
                    }
                }
            },
            "Port-channel2": {
                "name": "Port-channel2",
                "oper_status": "up",
                "bundle_id": 2,
                "protocol": "lacp",
                "members": {
                    "GigabitEthernet5": {
                            "lacp_port_priority": 32768,
                            "counters": {
                                "lacp_in_pkts": 10,
                                "lacp_errors": 0,
                                "lacp_out_pkts": 14
                            },
                            "interface": "GigabitEthernet5",
                            "bundled": False,
                            "port_num": 1,
                            "activity": "passive",
                            "partner_id": "001e.49e6.bc00",
                            "bundle_id": 2,
                            "age": 1,
                            "oper_key": 2
                    },
                    "GigabitEthernet4": {
                            "lacp_port_priority": 32768,
                            "counters": {
                                "lacp_in_pkts": 31,
                                "lacp_errors": 0,
                                "lacp_out_pkts": 24
                            },
                            "interface": "GigabitEthernet4",
                            "bundled": True,
                            "port_num": 1,
                            "activity": "passive",
                            "partner_id": "001e.49e6.bc00",
                            "bundle_id": 2,
                            "age": 15,
                            "oper_key": 2
                    },
                    "GigabitEthernet1/1": {
                            "bundle_id": 2,
                            "pagp_port_priority": 128
                    },
                    "GigabitEthernet6": {
                            "lacp_port_priority": 32768,
                            "counters": {
                                "lacp_in_pkts": 11,
                                "lacp_errors": 0,
                                "lacp_out_pkts": 13
                            },
                            "interface": "GigabitEthernet6",
                            "bundled": True,
                            "port_num": 1,
                            "activity": "passive",
                            "partner_id": "001e.49e6.bc00",
                            "bundle_id": 2,
                            "age": 0,
                            "oper_key": 2
                    },
                    "GigabitEthernet0/3": {
                            "bundle_id": 2,
                            "pagp_port_priority": 128
                    },
                    "GigabitEthernet1/0": {
                            "bundle_id": 2,
                            "pagp_port_priority": 128
                    }
                }
            },
            "Port-channel14": {
                "members": {
                    "GigabitEthernet1/0/7": {
                            "partner_id": "ecbd.1d09.5680",
                            "age": 22
                    },
                    "GigabitEthernet1/0/9": {
                            "partner_id": "ecbd.1d09.5680",
                            "age": 18
                    },
                    "GigabitEthernet1/0/8": {
                            "partner_id": "ecbd.1d09.5680",
                            "age": 16
                    }
                }
            }
        }
    }