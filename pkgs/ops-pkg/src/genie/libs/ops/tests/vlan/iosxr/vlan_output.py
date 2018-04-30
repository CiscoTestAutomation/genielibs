class VlanOutput(object):

    showEthernetTags =  {'interface': 
                            {'Gi0/0/0/1': 
                                {'sub_interface': 
                                    {'Gi0/0/0/1.501': 
                                        {'vlan_id': {'501': {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}}}, 
                             'Gi0/0/0/0': 
                                {'sub_interface': 
                                    {'Gi0/0/0/0.503': 
                                        {'vlan_id': 
                                            {'503': 
                                                {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}, 
                                     'Gi0/0/0/0.504': 
                                        {'vlan_id': 
                                            {'504': 
                                                {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}, 
                                     'Gi0/0/0/0.501': 
                                        {'vlan_id': 
                                            {'4': 
                                                {'outer_encapsulation_type': 'dot1ad', 'inner_encapsulation_vlan_id': '5', 'status': 'Up', 'inner_encapsulation_type': 'dot1Q', 'mtu': '1522', 'layer': 'L3'}}}, 
                                     'Gi0/0/0/0.511': 
                                        {'vlan_id': 
                                            {'511': 
                                                {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}, 
                                     'Gi0/0/0/0.505': 
                                        {'vlan_id': 
                                            {'505': 
                                                {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}, 
                                     'Gi0/0/0/0.510': 
                                        {'vlan_id': 
                                            {'510': 
                                                {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}, 
                                     'Gi0/0/0/0.502': 
                                        {'vlan_id': 
                                            {'502': 
                                                {'layer': 'L3', 'mtu': '1518', 'status': 'Up', 'outer_encapsulation_type': 'dot1Q'}}}}
                                }
                            }
                        }

    showEthernetTagsempty = {}

    vlan_all = {'501': 
                    {'sub_interface': 'Gi0/0/0/1.501', 'ethernet_encapsulation_type': 'dot1Q'}, 
                '503': 
                    {'sub_interface': 'Gi0/0/0/0.503', 'ethernet_encapsulation_type': 'dot1Q'}, 
                '504': 
                    {'sub_interface': 'Gi0/0/0/0.504', 'ethernet_encapsulation_type': 'dot1Q'}, 
                '4': 
                    {'sub_interface': 'Gi0/0/0/0.501', 'ethernet_encapsulation_type': 'dot1ad', 'inner_encapsulation_vlan_id': '5', 'inner_encapsulation_type': 'dot1Q'},
                '511': 
                    {'sub_interface': 'Gi0/0/0/0.511', 'ethernet_encapsulation_type': 'dot1Q'}, 
                '505': 
                    {'sub_interface': 'Gi0/0/0/0.505', 'ethernet_encapsulation_type': 'dot1Q'}, 
                '510': 
                    {'sub_interface': 'Gi0/0/0/0.510', 'ethernet_encapsulation_type': 'dot1Q'}, 
                '502': 
                    {'sub_interface': 'Gi0/0/0/0.502', 'ethernet_encapsulation_type': 'dot1Q'} 
            }

    vlan_all_empty = {}