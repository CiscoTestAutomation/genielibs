'''STP Genie Ops Object Outputs for IOSXR.'''


class StpOutput(object):

    ShowSpanningTreeMst_output = '''
    RP/0/RSP0/CPU0:athens#show spanning-tree mst test
    Tue Nov 14 05:54:37.272 EST
    Role:  ROOT=Root, DSGN=Designated, ALT=Alternate, BKP=Backup, MSTR=Master
    State: FWD=Forwarding, LRN=Learning, BLK=Blocked, DLY=Bringup Delayed

    Operating in dot1q mode


    MSTI 0 (CIST):

      VLANS Mapped: 1-4094

      CIST Root  Priority    32768
                 Address     0021.1bfd.1007
                 Ext Cost    2000

      Root ID    Priority    32768
                 Address     d867.d938.ace7
                 This bridge is the root
                 Int Cost    0
                 Max Age 20 sec, Forward Delay 15 sec


      Bridge ID  Priority    32768 (priority 32768 sys-id-ext 0)
                 Address     d867.d938.ace7
                 Max Age 20 sec, Forward Delay 15 sec
                 Max Hops 20, Transmit Hold count  6


    Interface    Port ID           Role State Designated           Port ID
                 Pri.Nbr Cost                 Bridge ID            Pri.Nbr 
    ------------ ------- --------- ---- ----- -------------------- -------
    Te0/0/0/16   128.1   2000      ROOT FWD   32768 0021.1bfd.1007 128.1  
    Te0/0/0/17   128.2   2000      ALT  BLK   32768 0021.1bfd.1007 128.2 
    '''

    ShowSpanningTreeMst = {
        'mstp': {
            'test': {
                'mst_instances': {
                    '0': {
                        'mst_id': '0',
                        'vlan': '1-4094',
                        'cist_root_priority': 32768,
                        'cist_root_address': '0021.1bfd.1007',
                        'cist_root_cost': 2000,
                        'designated_root_priority': 32768,
                        'designated_root_address': 'd867.d938.ace7',
                        'this_bridge_is': 'the root',
                        'root_cost': 0,
                        'root_max_age': 20,
                        'root_forward_delay': 15,
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': 'd867.d938.ace7',
                        'bridge_max_age': 20,
                        'bridge_forward_delay': 15,
                        'bridge_max_hops': 20,
                        'bridge_transmit_hold_count': 6,
                        'interfaces': {
                            'TenGigabitEthernet0/0/0/16': {
                                'name': 'TenGigabitEthernet0/0/0/16',
                                'cost': 2000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfd.1007',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                            'TenGigabitEthernet0/0/0/17': {
                                'name': 'TenGigabitEthernet0/0/0/17',
                                'cost': 2000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfd.1007',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                        },
                    },
                },
            },
        },
    }

    ShowSpanningTreeMstag_output = '''
    RP/0/RSP0/CPU0:iamx#show spanning-tree mstag risc
    Fri Apr 22 17:26:52.757 CEST
    Bundle-Ether10.0
      Pre-empt delay is disabled
      Name:            risc
      Revision:        1
      Max Age:         20
      Provider Bridge: no
      Bridge ID:       0000.0000.0002
      Port ID:         1
      External Cost:   0
      Hello Time:      2
      Active:          yes
      BPDUs sent:      39921
        MSTI 0 (CIST):
        VLAN IDs:         1-2,4-4094
        Bridge Priority:  8192
        Port Priority:    128
        Cost:             0
        Root Bridge:      0000.0000.0001
        Root Priority:    4096
        Topology Changes: 31
      MSTI 1
        VLAN IDs:         3
        Bridge Priority:  4096
        Port Priority:    128
        Cost:             0
        Root Bridge:      0000.0000.0002
        Root Priority:    4096
        Topology Changes: 51
    '''

    ShowSpanningTreeMstag = {
        'mstag': {
            'risc': {
                'domain': 'risc',
                'interfaces': {
                    'Bundle-Ether10.0': {
                        'interface': 'Bundle-Ether10.0',
                        'preempt_delay': False,
                        'name': 'risc',
                        'revision': 1,
                        'max_age': 20,
                        'provider_bridge': False,
                        'bridge_id': '0000.0000.0002',
                        'port_id': 1,
                        'external_cost': 0,
                        'hello_time': 2,
                        'active': True,
                        'counters': {
                            'bdpu_sent': 39921,
                        },
                    },
                    'instances': {
                        '0': {
                            'instance': 0,
                            'vlans': '1-2,4-4094',
                            'priority': 8192,
                            'port_priority': 128,
                            'cost': 0,
                            'root_bridge': '0000.0000.0001',
                            'root_priority': 4096,
                            'counters': {
                                'topology_changes': 31,
                            },
                        },
                        '1': {
                            'instance': 1,
                            'vlans': '3',
                            'priority': 4096,
                            'port_priority': 128,
                            'cost': 0,
                            'root_bridge': '0000.0000.0002',
                            'root_priority': 4096,
                            'counters': {
                                'topology_changes': 51,
                            },
                        },
                    },
                },
            },
        },
    }

    ShowSpanningTreePvrst_output = '''
        RP/0/RSP0/CPU0:vkg3#show spanning-tree pvrst a       
        Role:  ROOT=Root, DSGN=Designated, ALT=Alternate, BKP=Backup
        State: FWD=Forwarding, LRN=Learning, BLK=Blocked


        VLAN 2:

          Root ID    Priority    32768
                     Address     0021.1bfc.dc76
                     Max Age 20 sec, Forward Delay 15 sec


          Bridge ID  Priority    32768 (priority 32768 sys-id-ext 0)
                     Address     8cb6.4fe9.7b9e
                     Max Age 20 sec, Forward Delay 15 sec
                     Transmit Hold count   6


        Interface    Port ID           Role State Designated           Port ID
                     Pri.Nbr Cost                 Bridge ID            Pri.Nbr 
        ------------ ------- --------- ---- ----- -------------------- -------
        Gi0/7/0/0    128.1   20000     DSGN FWD   32768 8cb6.4fe9.7b9e 128.1
        Gi0/7/0/1    128.2   20000     DSGN FWD   32768 8cb6.4fe9.7b9e 128.2  
        Gi0/7/0/10   128.3   20000     ROOT FWD   32768 0021.1bfc.dc76 128.3  
        Gi0/7/0/11   128.4   20000     ALT  BLK   32768 0021.1bfc.dc76 128.4  

        VLAN 3:

          Root ID    Priority    32768
                     Address     0021.1bfc.dc76
                     Max Age 20 sec, Forward Delay 15 sec


          Bridge ID  Priority    32768 (priority 32768 sys-id-ext 0)
                     Address     8cb6.4fe9.7b9e
                     Max Age 20 sec, Forward Delay 15 sec
                     Transmit Hold count  6


        Interface    Port ID           Role State Designated           Port ID
                     Pri.Nbr Cost                 Bridge ID            Pri.Nbr 
        ------------ ------- --------- ---- ----- -------------------- -------
        Gi0/7/0/0    128.1   20000     DSGN FWD   32768 8cb6.4fe9.7b9e 128.1  
        Gi0/7/0/1    128.2   20000     DSGN FWD   32768 8cb6.4fe9.7b9e 128.2  
        Gi0/7/0/10   128.3   20000     ROOT FWD   32768 0021.1bfc.dc76 128.3  
        Gi0/7/0/11   128.4   20000     ALT  BLK   32768 0021.1bfc.dc76 128.4  

        VLAN 4:

          Root ID    Priority    32768
                     Address     0021.1bfc.dc76
                     Max Age 20 sec, Forward Delay 15 sec


          Bridge ID  Priority    32768 (priority 32768 sys-id-ext 0)
                     Address     8cb6.4fe9.7b9e
                     Max Age 20 sec, Forward Delay 15 sec
                     Transmit Hold count  6


        Interface    Port ID           Role State Designated           Port ID
                     Pri.Nbr Cost                 Bridge ID            Pri.Nbr 
        ------------ ------- --------- ---- ----- -------------------- -------
        Gi0/7/0/0    128.1   20000     DSGN FWD   32768 8cb6.4fe9.7b9e 128.1  
        Gi0/7/0/1    128.2   20000     DSGN FWD   32768 8cb6.4fe9.7b9e 128.2  
        Gi0/7/0/10   128.3   20000     ROOT FWD   32768 0021.1bfc.dc76 128.3  
        Gi0/7/0/11   128.4   20000     ALT  BLK   32768 0021.1bfc.dc76 128.4
    '''

    ShowSpanningTreePvrst = {
        'pvst': {
            'a': {
                'pvst_id': 'a',
                'vlans': {
                    2: {
                        'vlan_id': 2,
                        'designated_root_priority': 32768,
                        'designated_root_address': '0021.1bfc.dc76',
                        'designated_root_max_age': 20,
                        'designated_root_forward_delay': 15,
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': '8cb6.4fe9.7b9e',
                        'bridge_max_age': 20,
                        'bridge_forward_delay': 15,
                        'bridge_transmit_hold_count': 6,
                        'interface': {
                            'GigabitEthernet0/7/0/0': {
                                'name': 'GigabitEthernet0/7/0/0',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                            'GigabitEthernet0/7/0/1': {
                                'name': 'GigabitEthernet0/7/0/1',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'GigabitEthernet0/7/0/10': {
                                'name': 'GigabitEthernet0/7/0/10',
                                'cost': 20000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 3,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 3,
                            },
                            'GigabitEthernet0/7/0/11': {
                                'name': 'GigabitEthernet0/7/0/11',
                                'cost': 20000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 4,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 4,
                            },
                        },
                    },
                    3: {
                        'vlan_id': 3,
                        'designated_root_priority': 32768,
                        'designated_root_address': '0021.1bfc.dc76',
                        'designated_root_max_age': 20,
                        'designated_root_forward_delay': 15,
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': '8cb6.4fe9.7b9e',
                        'bridge_max_age': 20,
                        'bridge_forward_delay': 15,
                        'bridge_transmit_hold_count': 6,
                        'interface': {
                            'GigabitEthernet0/7/0/0': {
                                'name': 'GigabitEthernet0/7/0/0',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                            'GigabitEthernet0/7/0/1': {
                                'name': 'GigabitEthernet0/7/0/1',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'GigabitEthernet0/7/0/10': {
                                'name': 'GigabitEthernet0/7/0/10',
                                'cost': 20000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 3,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 3,
                            },
                            'GigabitEthernet0/7/0/11': {
                                'name': 'GigabitEthernet0/7/0/11',
                                'cost': 20000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 4,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 4,
                            },
                        },
                    },
                    4: {
                        'vlan_id': 4,
                        'designated_root_priority': 32768,
                        'designated_root_address': '0021.1bfc.dc76',
                        'designated_root_max_age': 20,
                        'designated_root_forward_delay': 15,
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': '8cb6.4fe9.7b9e',
                        'bridge_max_age': 20,
                        'bridge_forward_delay': 15,
                        'bridge_transmit_hold_count': 6,
                        'interface': {
                            'GigabitEthernet0/7/0/0': {
                                'name': 'GigabitEthernet0/7/0/0',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                            'GigabitEthernet0/7/0/1': {
                                'name': 'GigabitEthernet0/7/0/1',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'GigabitEthernet0/7/0/10': {
                                'name': 'GigabitEthernet0/7/0/10',
                                'cost': 20000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 3,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 3,
                            },
                            'GigabitEthernet0/7/0/11': {
                                'name': 'GigabitEthernet0/7/0/11',
                                'cost': 20000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 4,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 4,
                            },
                        },
                    },
                },
            },
        },
    }

    ShowSpanningTreePvrsTag_output = '''
    RP/0/0/CPU0:ios#show spanning-tree pvrstag foo
    Wed Mar 29 12:38:05.528 UTC
    GigabitEthernet0/0/0/0
      VLAN 5
        Pre-empt delay is enabled. Sending startup BPDU until 13:38:03
        Sub-interface:    GigabitEthernet0/0/0/0.5 (Up)
        Max Age: 20
        Root Priority:    0
        Root Bridge: 0000.0000.0000
        Cost:             1
        Bridge Priority:  32768
        Bridge ID:        0255.1d30.0c40
        Port Priority:    128
        Port ID           1
        Hello Time:       2
        Active:           Yes
        BPDUs sent:       6
        Topology Changes: 0

    GigabitEthernet0/0/0/1
      VLAN 5
        Pre-empt delay is enabled. Sending standard BPDU
        Sub-interface:    GigabitEthernet0/0/0/1.5 (Up)
        Max Age:          20
        Root Priority:    0
        Root Bridge:      0000.0000.0000
        Cost:             0
        Bridge Priority:  32768
        Bridge ID:        021a.9eeb.6a59
        Port Priority:    128
        Port ID           1
        Hello Time:       2
        Active:           Yes
        BPDUs sent:       7
        Topology Changes: 0
    '''

    ShowSpanningTreePvrsTag = {
        'pvrstag': {
            'foo': {
                'domain': 'foo',
                'interfaces': {
                    'GigabitEthernet0/0/0/0': {
                        'interface': 'GigabitEthernet0/0/0/0',
                        'vlans': {
                            '5': {
                                'preempt_delay': True,
                                'preempt_delay_state':
                                'Sending startup BPDU until 13:38:03',
                                'sub_interface': 'GigabitEthernet0/0/0/0.5',
                                'sub_interface_state': 'Up',
                                'max_age': 20,
                                'root_priority': 0,
                                'root_bridge': '0000.0000.0000',
                                'root_cost': 1,
                                'bridge_priority': 32768,
                                'bridge_id': '0255.1d30.0c40',
                                'port_priority': 128,
                                'port_id': 1,
                                'hello_time': 2,
                                'active': True,
                                'counters': {
                                    'bdpu_sent': 6,
                                    'topology_changes': 0,
                                },
                            },
                        },
                    },
                    'GigabitEthernet0/0/0/1': {
                        'interface': 'GigabitEthernet0/0/0/1',
                        'vlans': {
                            '5': {
                                'preempt_delay': True,
                                'preempt_delay_state': 'Sending standard BPDU',
                                'sub_interface': 'GigabitEthernet0/0/0/1.5',
                                'sub_interface_state': 'Up',
                                'max_age': 20,
                                'root_priority': 0,
                                'root_bridge': '0000.0000.0000',
                                'root_cost': 0,
                                'bridge_priority': 32768,
                                'bridge_id': '021a.9eeb.6a59',
                                'port_priority': 128,
                                'port_id': 1,
                                'hello_time': 2,
                                'active': True,
                                'counters': {
                                    'bdpu_sent': 7,
                                    'topology_changes': 0,
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    ShowSpanningTreePvsTag_output = '''
     RP/0/RSP0/CPU0:SMU-uut#show spanning-tree pvstag foo 
    Bundle-Ether1000
      VLAN 2100
        Pre-empt delay is disabled
        Sub-interface:    Bundle-Ether1000.2100 (Up)
        Max Age:          20
        Root Priority:    0
        Root Bridge:      0000.0000.0000
        Cost:             0
        Bridge Priority:  32768
        Bridge ID:        6c9c.ed0d.8088
        Port Priority:    128
        Port ID           1
        Hello Time:       2
        Active:           Yes
        BPDUs sent:       10
        Topology Changes: 0
    '''
    ShowSpanningTreePvsTag = {
        'pvstag': {
            'foo': {
                'domain': 'foo',
                'interfaces': {
                    'Bundle-Ether1000': {
                        'interface': 'Bundle-Ether1000',
                        'vlans': {
                            '2100': {
                                'preempt_delay': False,
                                'sub_interface': 'Bundle-Ether1000.2100',
                                'sub_interface_state': 'Up',
                                'max_age': 20,
                                'root_priority': 0,
                                'root_bridge': '0000.0000.0000',
                                'root_cost': 0,
                                'bridge_priority': 32768,
                                'bridge_id': '6c9c.ed0d.8088',
                                'port_priority': 128,
                                'port_id': 1,
                                'hello_time': 2,
                                'active': True,
                                'counters': {
                                    'bdpu_sent': 10,
                                    'topology_changes': 0,
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    stpOutput = {
        'mstp': {
            'test': {
                'mst_instances': {
                    '0': {
                        'mst_id': '0',
                        'vlan': '1-4094',
                        'bridge_priority': 32768,
                        'bridge_address': 'd867.d938.ace7',
                        'designated_root_priority': 32768,
                        'designated_root_address': 'd867.d938.ace7',
                        'root_cost': 0,
                        'interfaces': {
                            'TenGigabitEthernet0/0/0/17': {
                                'name': 'TenGigabitEthernet0/0/0/17',
                                'cost': 2000,
                                'port_priority': 128,
                                'port_num': 2,
                                'role': 'ALT',
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfd.1007',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'TenGigabitEthernet0/0/0/16': {
                                'name': 'TenGigabitEthernet0/0/0/16',
                                'cost': 2000,
                                'port_priority': 128,
                                'port_num': 1,
                                'role': 'ROOT',
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfd.1007',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                        },
                    },
                },
            },
        },
        'mstag': {
            'risc': {
                'domain': 'risc',
                'interfaces': {
                    'Bundle-Ether10.0': {
                        'interface': 'Bundle-Ether10.0',
                        'preempt_delay': False,
                        'name': 'risc',
                        'revision': 1,
                        'max_age': 20,
                        'provider_bridge': False,
                        'bridge_id': '0000.0000.0002',
                        'port_id': 1,
                        'external_cost': 0,
                        'hello_time': 2,
                        'active': True,
                    },
                    'instances': {
                        '1': {
                            'instance': 1,
                            'vlans': '3',
                            'priority': 4096,
                            'port_priority': 128,
                            'cost': 0,
                            'root_priority': 4096,
                            'counters': {
                                'topology_changes': 51,
                            },
                        },
                        '0': {
                            'instance': 0,
                            'vlans': '1-2,4-4094',
                            'priority': 8192,
                            'port_priority': 128,
                            'cost': 0,
                            'root_priority': 4096,
                            'counters': {
                                'topology_changes': 31,
                            },
                        },
                    },
                },
            },
        },
        'pvst': {
            'a': {
                'pvst_id': 'a',
                'vlans': {
                    4: {
                        'vlan_id': 4,
                        'designated_root_priority': 32768,
                        'designated_root_address': '0021.1bfc.dc76',
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': '8cb6.4fe9.7b9e',
                        'interface': {
                            'GigabitEthernet0/7/0/11': {
                                'name': 'GigabitEthernet0/7/0/11',
                                'cost': 20000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 4,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 4,
                            },
                            'GigabitEthernet0/7/0/10': {
                                'name': 'GigabitEthernet0/7/0/10',
                                'cost': 20000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 3,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 3,
                            },
                            'GigabitEthernet0/7/0/1': {
                                'name': 'GigabitEthernet0/7/0/1',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'GigabitEthernet0/7/0/0': {
                                'name': 'GigabitEthernet0/7/0/0',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                        },
                    },
                    3: {
                        'vlan_id': 3,
                        'designated_root_priority': 32768,
                        'designated_root_address': '0021.1bfc.dc76',
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': '8cb6.4fe9.7b9e',
                        'interface': {
                            'GigabitEthernet0/7/0/11': {
                                'name': 'GigabitEthernet0/7/0/11',
                                'cost': 20000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 4,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 4,
                            },
                            'GigabitEthernet0/7/0/10': {
                                'name': 'GigabitEthernet0/7/0/10',
                                'cost': 20000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 3,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 3,
                            },
                            'GigabitEthernet0/7/0/1': {
                                'name': 'GigabitEthernet0/7/0/1',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'GigabitEthernet0/7/0/0': {
                                'name': 'GigabitEthernet0/7/0/0',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                        },
                    },
                    2: {
                        'vlan_id': 2,
                        'designated_root_priority': 32768,
                        'designated_root_address': '0021.1bfc.dc76',
                        'bridge_priority': 32768,
                        'sys_id_ext': 0,
                        'bridge_address': '8cb6.4fe9.7b9e',
                        'interface': {
                            'GigabitEthernet0/7/0/11': {
                                'name': 'GigabitEthernet0/7/0/11',
                                'cost': 20000,
                                'role': 'ALT',
                                'port_priority': 128,
                                'port_num': 4,
                                'port_state': 'BLK',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 4,
                            },
                            'GigabitEthernet0/7/0/10': {
                                'name': 'GigabitEthernet0/7/0/10',
                                'cost': 20000,
                                'role': 'ROOT',
                                'port_priority': 128,
                                'port_num': 3,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '0021.1bfc.dc76',
                                'designated_port_priority': 128,
                                'designated_port_num': 3,
                            },
                            'GigabitEthernet0/7/0/1': {
                                'name': 'GigabitEthernet0/7/0/1',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 2,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 2,
                            },
                            'GigabitEthernet0/7/0/0': {
                                'name': 'GigabitEthernet0/7/0/0',
                                'cost': 20000,
                                'role': 'DSGN',
                                'port_priority': 128,
                                'port_num': 1,
                                'port_state': 'FWD',
                                'designated_bridge_priority': 32768,
                                'designated_bridge_address': '8cb6.4fe9.7b9e',
                                'designated_port_priority': 128,
                                'designated_port_num': 1,
                            },
                        },
                    },
                },
            },
        },
        'pvrstag': {
            'foo': {
                'domain': 'foo',
                'interfaces': {
                    'GigabitEthernet0/0/0/1': {
                        'interface': 'GigabitEthernet0/0/0/1',
                        'vlans': {
                            '5': {
                                'preempt_delay': True,
                                'preempt_delay_state': 'Sending standard BPDU',
                                'sub_interface': 'GigabitEthernet0/0/0/1.5',
                                'sub_interface_state': 'Up',
                                'max_age': 20,
                                'root_priority': 0,
                                'root_cost': 0,
                                'bridge_id': '021a.9eeb.6a59',
                                'port_priority': 128,
                                'port_id': 1,
                                'hello_time': 2,
                                'active': True,
                                'counters': {
                                    'topology_changes': 0,
                                },
                            },
                        },
                    },
                    'GigabitEthernet0/0/0/0': {
                        'interface': 'GigabitEthernet0/0/0/0',
                        'vlans': {
                            '5': {
                                'preempt_delay': True,
                                'preempt_delay_state':
                                'Sending startup BPDU until 13:38:03',
                                'sub_interface': 'GigabitEthernet0/0/0/0.5',
                                'sub_interface_state': 'Up',
                                'max_age': 20,
                                'root_priority': 0,
                                'root_cost': 1,
                                'bridge_id': '0255.1d30.0c40',
                                'port_priority': 128,
                                'port_id': 1,
                                'hello_time': 2,
                                'active': True,
                                'counters': {
                                    'topology_changes': 0,
                                },
                            },
                        },
                    },
                },
            },
        },
        'pvstag': {
            'foo': {
                'domain': 'foo',
                'interfaces': {
                    'Bundle-Ether1000': {
                        'interface': 'Bundle-Ether1000',
                        'vlans': {
                            '2100': {
                                'preempt_delay': False,
                                'sub_interface': 'Bundle-Ether1000.2100',
                                'sub_interface_state': 'Up',
                                'max_age': 20,
                                'root_priority': 0,
                                'root_cost': 0,
                                'bridge_id': '6c9c.ed0d.8088',
                                'port_priority': 128,
                                'port_id': 1,
                                'hello_time': 2,
                                'active': True,
                                'counters': {
                                    'topology_changes': 0,
                                },
                            },
                        },
                    },
                },
            },
        },
    }
