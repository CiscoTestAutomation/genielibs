# python
import copy

class TriggersConfigs():
    
    basic_config = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'lldp run\n'\
                              'interface GigabitEthernet1/0/13\n'\
                              'no shutdown\n'\
                              'default interface GigabitEthernet2/0/15\n'\
                              'default interface GigabitEthernet3/0/15\n'\
                              'no interface vlan 10\n'\
                              'no interface vlan 11',
                    'sleep': 300
                }
            },
            'helper': {
                '1': {
                    'config': 'lldp run'
                }
            }
        }
    }
    
    basic_unconfig = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'no lldp run\n'\
                              'default interface GigabitEthernet1/0/13\n'\
                              'default interface vlan 1\n'\
                              'default interface GigabitEthernet1/0/15\n'\
                              'default interface GigabitEthernet1/0/16\n'\
                              'default interface GigabitEthernet1/0/17\n'\
                              'default interface GigabitEthernet2/0/15\n'\
                              'default interface GigabitEthernet3/0/15\n'\
                              'no vlan 2\n'\
                              'no vlan 10\n'\
                              'no vlan 11\n'\
                              'no interface vlan 2\n'\
                              'no interface vlan 10\n'\
                              'no interface vlan 11',
                }
            },
            'helper': {
                '1': {
                    'config': 'no lldp run\n'\
                              'default vlan 1\n'\
                              'default interface vlan 1\n'\
                              'no vlan 2\n'\
                              'no vlan 10\n'\
                              'no vlan 11\n'\
                              'no interface vlan 2\n'\
                              'no interface vlan 10\n'\
                              'no interface vlan 11\n'\
                              'no ip vrf test1\n'\
                              'no ip vrf test2\n'\
                              'no ip vrf test3\n'\
                              'default interface GigabitEthernet1/0/1\n'\
                              'default interface GigabitEthernet1/0/2\n'\
                              'default interface GigabitEthernet1/0/4\n'\
                              'default interface GigabitEthernet1/0/5\n',
                }
            }
        }
    }

    switchover_ping = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'default interface vlan 1\n'\
                            'ip routing\n'\
                            'vlan 10\n'\
                            'state active\n'\
                            'interface vlan 10\n'\
                            'ip address 1.1.1.2 255.255.255.0\n'\
                            'no shut\n'\
                            'ipv6 unicast-routing\n'\
                            'interface GigabitEthernet2/0/15\n'\
                            'switchport access vlan 10\n'\
                            'switchport mode access\n'\
                            'no shut\n'\
                            'vlan 11\n'\
                            'state active\n'\
                            'interface vlan 11\n'\
                            'ip address 2.2.2.2 255.255.255.0\n'\
                            'no shut\n'\
                            'interface GigabitEthernet3/0/15\n'\
                            'switchport access vlan 11\n'\
                            'switchport mode access\n'\
                            'no shut\n'\
                            'do copy running-config startup-config\n'\
                            'do write memory',
                    'unconfig': 'default interface GigabitEthernet2/0/15\n'\
                                'default interface GigabitEthernet3/0/15\n'\
                                'no vlan 10\n'\
                                'no vlan 11\n'\
                                'no interface vlan 10\n'\
                                'no interface vlan 11',
                    'sleep': 45
                }
            },
            'helper': {
                '1': {
                    'config': '!\n'\
                              'ip routing\n'\
                              '!\n'\
                              'ip vrf vrf1\n'\
                              'rd 1:1\n'\
                              '!\n'\
                              'ip vrf vrf2\n'\
                              'rd 1:2\n'\
                              '!\n'\
                              'interface GigabitEthernet1/0/4\n'\
                              'no switchport\n'\
                              'no ip address\n'\
                              'ip vrf forwarding vrf1\n'\
                              'ip address 1.1.1.1 255.255.255.0\n'\
                              'no shutdown\n'\
                              '!\n'\
                              'interface GigabitEthernet1/0/5\n'\
                              'no switchport\n'\
                              'no ip address\n'\
                              'ip vrf forwarding vrf2\n'\
                              'ip address 2.2.2.1 255.255.255.0\n'\
                              'no shutdown\n'\
                              'ip route vrf vrf2 1.1.1.0 255.255.255.0 GigabitEthernet1/0/5 2.2.2.2\n'\
                              'ip route vrf vrf1 2.2.2.0 255.255.255.0 GigabitEthernet1/0/4 1.1.1.2',
                    'unconfig': 'default interface GigabitEthernet1/0/4\n'\
                                'default interface GigabitEthernet1/0/5\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2\n'\
                                'no ip route vrf vrf2 1.1.1.0 255.255.255.0 GigabitEthernet1/0/5 2.2.2.2\n'\
                                'no ip route vrf vrf1 2.2.2.0 255.255.255.0 GigabitEthernet1/0/4 1.1.1.2',
                }
            }
        }
    }

    application_sanity_base = '!enable gloabl cef for ipv4 and vrf forwarding\n'\
                              'ip routing\n'\
                              '!\n'\
                              'ip vrf vrf1\n'\
                              'rd 1:1\n'\
                              '!\n'\
                              'ip vrf vrf2\n'\
                              'rd 1:2\n'\
                              '!\n'\
                              'interface GigabitEthernet1/0/1\n'\
                              'no switchport\n'\
                              'no ip address\n'\
                              'ip vrf forwarding vrf1\n'\
                              'ip address 10.0.0.1 255.255.255.0\n'\
                              'mac-address 0200.dead.0001\n'\
                              'no shut\n'\
                              '!\n'\
                              'interface GigabitEthernet1/0/2\n'\
                              'no switchport\n'\
                              'no ip address\n'\
                              'ip vrf forwarding vrf2\n'\
                              'ip address 10.0.0.2 255.255.255.0\n'\
                              'mac-address 0200.dead.0002\n'\
                              'no shut\n'\
                              '!'

    l2_int_up = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16',
                    'sleep': 30
                }
            },
            'helper': {
                '1': {
                    'config': application_sanity_base,
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2',
                }
            }
        }
    }

    SVI_L3_ping_native_VLAN = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'default interface vlan 1\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport\n'\
                            'switchport access vlan 1\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport\n'\
                            'switchport access vlan 1\n'\
                            'no shut\n'\
                            'interface vlan 1\n'\
                            'ip address 18.0.1.1 255.255.255.0\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface vlan 1',
                    'sleep': 30
                }
            },
            'helper': {
                '1': {
                    'config': application_sanity_base,
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2',
                },
                '2': {
                    'config': 'default interface GigabitEthernet1/0/1\n'\
                            'default interface GigabitEthernet1/0/2\n'\
                            'default interface vlan 1\n'\
                            'interface GigabitEthernet1/0/1\n'\
                            'switchport\n'\
                            'switchport access vlan 1\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/2\n'\
                            'switchport\n'\
                            'switchport access vlan 1\n'\
                            'no shut\n'\
                            'interface vlan 1\n'\
                            'ip address 18.0.1.2 255.255.255.0\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface vlan 1',
                }
            }
        }
    }

    SVI_L3_ping_VLAN99 = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'default interface vlan 1\n'\
                            'interface vlan 99\n'\
                            'ip address 18.0.1.1 255.255.255.0\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport\n'\
                            'switchport access vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport\n'\
                            'switchport access vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'no interface vlan 99',
                    'sleep': 40
                }
            },
            'helper': {
                '1': {
                    'config': application_sanity_base,
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2',
                },
                '2': {
                    'config': 'default interface GigabitEthernet1/0/1\n'\
                            'default interface GigabitEthernet1/0/2\n'\
                            'default interface vlan 1\n'\
                            'interface vlan 99\n'\
                            'ip address 18.0.1.2 255.255.255.0\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/1\n'\
                            'switchport\n'\
                            'switchport access vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/2\n'\
                            'switchport\n'\
                            'switchport access vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no interface vlan 99',
                }
            }
        }
    }

    trunk_config = {
        'devices': {
            'uut': {
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'default interface vlan 1\n'\
                            'vlan 99\n'\
                            'state active\n'\
                            'interface vlan 99\n'\
                            'ip address 18.0.1.1 255.255.255.0\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'no vlan 99\n'\
                                'no interface vlan 99',
                    'sleep': 60
                }
            },
            'helper': {
                '1': {
                    'config': application_sanity_base,
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2',
                },
                '2': {
                    'config': 'default interface GigabitEthernet1/0/1\n'\
                            'default interface GigabitEthernet1/0/2\n'\
                            'default interface vlan 1\n'\
                            'vlan 99\n'\
                            'state active\n'\
                            'interface vlan 99\n'\
                            'ip address 18.0.1.2 255.255.255.0\n'\
                            'no shut\n'\
                            'interface loopback1\n'\
                            'ip address 1.1.1.1 255.255.255.0\n'\
                            'interface GigabitEthernet1/0/1\n'\
                            'switchport trunk encapsulation dot1q\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/2\n'\
                            'switchport trunk encapsulation dot1q\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no interface loopback1\n'\
                                'no vlan 99\n'\
                                'no interface vlan 99',
                }
            }
        }
    }

    SVI_L3_ping_VLAN99_Trunk = {
        'devices': {
            'uut': {
                'next_hop': '18.0.1.2',
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'default interface vlan 1\n'\
                            'vlan 99\n'\
                            'state active\n'\
                            'interface vlan 99\n'\
                            'ip address 18.0.1.1 255.255.255.0\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'no vlan 99\n'\
                                'no interface vlan 99',
                    'sleep': 50
                }
            },
            'helper': {
                '1': {
                    'config': application_sanity_base,
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2',
                },
                '2': {
                    'config': 'default interface GigabitEthernet1/0/1\n'\
                            'default interface GigabitEthernet1/0/2\n'\
                            'default interface vlan 1\n'\
                            'vlan 99\n'\
                            'state active\n'\
                            'interface vlan 99\n'\
                            'ip address {next_hop} 255.255.255.0\n'\
                            'no shut\n'\
                            'interface loopback1\n'\
                            'ip address 1.1.1.1 255.255.255.0\n'\
                            'interface GigabitEthernet1/0/1\n'\
                            'switchport trunk encapsulation dot1q\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/2\n'\
                            'switchport trunk encapsulation dot1q\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no interface loopback1\n'\
                                'no vlan 99\n'\
                                'no interface vlan 99',
                }
            }
        }
    }

    IPv6_Traceroute_VLAN99_Trunk = {
        'devices': {
            'uut': {
                'next_hop': '2001:ABAD:BEEF::2',
                '1': {
                    'config': 'default interface GigabitEthernet1/0/15\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'default interface vlan 1\n'\
                            'vlan 99\n'\
                            'state active\n'\
                            'interface vlan 99\n'\
                            'ipv6 address 2001:ABAD:BEEF::1/64\n'\
                            'no shut\n'\
                            'ipv6 unicast-routing\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'no vlan 99\n'\
                                'no interface vlan 99',
                    'sleep': 50
                }
            },
            'helper': {
                '1': {
                    'config': application_sanity_base,
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip vrf vrf1\n'\
                                'no ip vrf vrf2',
                },
                '2': {
                    'config': 'default interface GigabitEthernet1/0/2\n'\
                            'default interface GigabitEthernet1/0/1\n'\
                            'default interface vlan 1\n'\
                            'vlan 99\n'\
                            'state active\n'\
                            'interface vlan 99\n'\
                            'ipv6 address 2001:ABAD:BEEF::2/64\n'\
                            'no shut\n'\
                            'interface loopback1\n'\
                            'ipv6 address 3020:3020::1/64\n'\
                            'interface GigabitEthernet1/0/1\n'\
                            'switchport trunk encapsulation dot1q\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut\n'\
                            'interface GigabitEthernet1/0/2\n'\
                            'switchport trunk encapsulation dot1q\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 99\n'\
                            'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no interface loopback1\n'\
                                'no vlan 99\n'\
                                'no interface vlan 99',
                }
            }
        }
    }

    stp_base_uut = 'interface GigabitEthernet1/0/15\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/16\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/17\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/1\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/2\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/3\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/4\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/7\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/8\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet1/0/9\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet2/0/15\n'\
                   'shutdown\n'\
                   'interface GigabitEthernet3/0/15\n'\
                   'shutdown\n'\
                   'vlan 1-2\n'\
                   'no vlan 3-1000\n'\
                   'spanning-tree vlan 1-2\n'\
                   'spanning-tree mode pvst\n'\
                   'default int GigabitEthernet1/0/15\n'\
                   'int GigabitEthernet1/0/15\n'\
                   'switchport mode trunk\n'\
                   'switchport trunk allowed vlan 1-2\n'\
                   'shut\n'\
                   'no shut\n'\
                   'int GigabitEthernet1/0/16\n'\
                   'shut\n'\
                   'default int GigabitEthernet1/0/17\n'\
                   'int GigabitEthernet1/0/17\n'\
                   'switchport mode access\n'\
                   'switchport access vlan 1\n'\
                   'shut\n'\
                   'no shut\n'\
                   'default int GigabitEthernet2/0/15\n'\
                   'int GigabitEthernet2/0/15\n'\
                   'switchport mode access\n'\
                   'switchport access vlan 2\n'\
                   'shut\n'\
                   'no shut'

    stp_base_helper = 'ip routing\n'\
                  'vlan 1-2\n'\
                  'exit\n'\
                  'spanning-tree vlan 1-2\n'\
                  'spanning-tree mode pvst\n'\
                  'ip vrf test1\n'\
                  'rd 100:1\n'\
                  'route-target export 100:1\n'\
                  'route-target import 100:1\n'\
                  '!\n'\
                  'ip vrf test2\n'\
                  'rd 100:2\n'\
                  'route-target export 100:2\n'\
                  'route-target import 100:2\n'\
                  '!\n'\
                  'ip vrf test3\n'\
                  'rd 100:3\n'\
                  'route-target export 100:3\n'\
                  'route-target import 100:3\n'\
                  'exit\n'\
                  '!\n'\
                  'default int Vlan1\n'\
                  'interface Vlan1\n'\
                  'ip vrf forwarding test1\n'\
                  'ip address 1.2.1.1 255.255.255.0\n'\
                  'no shut\n'\
                  '!\n'\
                  'interface Vlan2\n'\
                  'ip vrf forwarding test1\n'\
                  'ip address 1.2.2.1 255.255.255.0\n'\
                  'no shut\n'\
                  '!\n'\
                  'default int GigabitEthernet1/0/1\n'\
                  'interface GigabitEthernet1/0/1\n'\
                  'switchport trunk encapsulation dot1q\n'\
                  'switchport mode trunk\n'\
                  'switchport trunk allowed vlan 1-2\n'\
                  'no shut\n'\
                  '!\n'\
                  'interface GigabitEthernet1/0/2\n'\
                  'shut\n'\
                  '!\n'\
                  'default int GigabitEthernet1/0/3\n'\
                  'interface GigabitEthernet1/0/3\n'\
                  'no switchport\n'\
                  'ip vrf forwarding test2\n'\
                  'ip address 1.2.1.2 255.255.255.0\n'\
                  'no shut\n'\
                  '!\n'\
                  'default int GigabitEthernet1/0/4\n'\
                  'interface GigabitEthernet1/0/4\n'\
                  'no switchport\n'\
                  'ip vrf forwarding test3\n'\
                  'ip address 1.2.2.2 255.255.255.0\n'\
                  'no shut\n'\
                  '!\n'\
                  'loggin buffer 500000 debugging'

    STP_root_check = {
        'devices': {
            'uut': {
                '1': {
                    'config': stp_base_uut,
                    'unconfig': 'default vlan 1\n'\
                                'no vlan 2\n'\
                                'no interface vlan2',
                },
                '2': {
                    'config': 'spanning-tree vlan 1\n'\
                              'spanning-tree mode pvst\n'\
                              'default spanning-tree vlan 1 priority\n'\
                              'spanning-tree vlan 1 priority 0',
                    'unconfig': 'default spanning-tree vlan 1\n'\
                                'default spanning-tree mode\n'\
                                'default spanning-tree vlan 1 priority\n'\
                                'default interface GigabitEthernet2/0/15\n'\
                                'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface GigabitEthernet1/0/17\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'default interface GigabitEthernet1/0/4\n'\
                                'default interface GigabitEthernet1/0/7\n'\
                                'default interface GigabitEthernet1/0/8\n'\
                                'default interface GigabitEthernet1/0/9\n'\
                                'default interface GigabitEthernet3/0/15',
                    'sleep': 60
                }
            },
            'helper': {
                '1': {
                    'config': stp_base_helper,
                    'unconfig': 'no ip vrf test1\n'\
                                'no ip vrf test2\n'\
                                'no ip vrf test3\n'\
                                'default vlan 1\n'\
                                'no vlan 2\n'\
                                'no interface vlan2',
                },
                '2': {
                    'config': 'spanning-tree vlan 1\n'\
                              'spanning-tree mode pvst\n'\
                              'default spanning-tree vlan 1 priority',
                    'unconfig': 'default spanning-tree vlan 1\n'\
                                'default spanning-tree mode\n'\
                                'default spanning-tree vlan 1 priority\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'default interface GigabitEthernet1/0/4\n'\
                                'no interface vlan2',
                }
            }
        }
    }

    STP_Rapid_PVST_root_check = {
        'devices': {
            'uut': {
                '1': {
                    'config': stp_base_uut,
                    'unconfig': 'default vlan 1\n'\
                                'no vlan 2\n'\
                                'no interface vlan2',
                },
                '2': {
                    'config': 'vlan 1-2\n'\
                              'exit\n'\
                              'spanning-tree vlan 1-2\n'\
                              'spanning-tree mode rapid-pvst\n'\
                              'default spanning-tree vlan 1-2 priority\n'\
                              'spanning-tree vlan 1-2 priority 0',
                    'unconfig': 'default spanning-tree vlan 1\n'\
                                'default spanning-tree mode\n'\
                                'default spanning-tree vlan 1-2 priority\n'\
                                'default interface GigabitEthernet2/0/15\n'\
                                'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface GigabitEthernet1/0/17\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'default interface GigabitEthernet1/0/4\n'\
                                'default interface GigabitEthernet1/0/7\n'\
                                'default interface GigabitEthernet1/0/8\n'\
                                'default interface GigabitEthernet1/0/9\n'\
                                'no vlan 2\n'\
                                'default vlan 1\n'\
                                'default interface GigabitEthernet3/0/15',
                    'sleep': 60
                }
            },
            'helper': {
                '1': {
                    'config': stp_base_helper,
                    'unconfig': 'no ip vrf test1\n'\
                                'no ip vrf test2\n'\
                                'no ip vrf test3\n'\
                                'default vlan 1\n'\
                                'no vlan 2\n'\
                                'no interface vlan2',
                },
                '2': {
                    'config': 'vlan 1-2\n'\
                              'exit\n'\
                              'spanning-tree vlan 1-2\n'\
                              'spanning-tree mode rapid-pvst\n'\
                              'default spanning-tree vlan 1-2 priority',
                    'unconfig': 'default spanning-tree vlan 1\n'\
                                'default spanning-tree mode\n'\
                                'default spanning-tree vlan 1-2 priority\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'default interface GigabitEthernet1/0/4\n'\
                                'no vlan 2\n'\
                                'default vlan 1\n'\
                                'no interface vlan2',
                }
            }
        }
    }

    ethernet_acl_pacl = {
        'devices': {
            'uut': {
                '1': {
                    'config': stp_base_uut,
                    'unconfig': 'default vlan 1\n'\
                                'no vlan 2\n'\
                                'no interface vlan2',
                },
                '2': {
                    'config': 'vlan 1-2\n'\
                              'exit\n'\
                              'spanning-tree vlan 1-2\n'\
                              'spanning-tree mode rapid-pvst\n'\
                              'default spanning-tree vlan 1-2 priority',
                    'unconfig': 'default spanning-tree vlan 1\n'\
                                'default spanning-tree mode\n'\
                                'default spanning-tree vlan 1-2 priority\n'\
                                'default interface GigabitEthernet2/0/15\n'\
                                'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface GigabitEthernet1/0/17\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'default interface GigabitEthernet1/0/4\n'\
                                'default interface GigabitEthernet1/0/7\n'\
                                'default interface GigabitEthernet1/0/8\n'\
                                'default interface GigabitEthernet1/0/9\n'\
                                'no vlan 2\n'\
                                'default vlan 1\n'\
                                'default interface GigabitEthernet3/0/15',
                    'sleep': 50
                }
            },
            'helper': {
                '1': {
                    'config': stp_base_helper,
                    'unconfig': 'no ip vrf test1\n'\
                                'no ip vrf test2\n'\
                                'no ip vrf test3\n'\
                                'default vlan 1\n'\
                                'no vlan 2\n'\
                                'no interface vlan2',
                },
                '2': {
                    'config': 'vlan 1-2\n'\
                              'exit\n'\
                              'spanning-tree vlan 1-2\n'\
                              'spanning-tree mode rapid-pvst\n'\
                              'default spanning-tree vlan 1-2 priority',
                    'unconfig': 'default spanning-tree vlan 1\n'\
                                'default spanning-tree mode\n'\
                                'default spanning-tree vlan 1-2 priority\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'default interface GigabitEthernet1/0/4\n'\
                                'no vlan 2\n'\
                                'default vlan 1\n'\
                                'no interface vlan2',
                }
            }
        }
    }

    ip_acl_pacl_permit = copy.deepcopy(ethernet_acl_pacl)
    ip_acl_pacl_deny = copy.deepcopy(ethernet_acl_pacl)

    ip_acl_racl = {
        'devices': {
            'helper': {
                '1': {
                    'config': \
                        'interface vlan 10\n'\
                        'ip address 20.1.1.1 255.255.255.0\n'\
                        'no shut\n'\
                        '!\n'\
                        'default interface GigabitEthernet1/0/2\n'\
                        'interface GigabitEthernet1/0/2\n'\
                        'switchport mode access\n'\
                        'switchport access vlan 10\n'\
                        'no shut\n'\
                        'exit\n'\
                        '!\n'\
                        'ip routing\n'\
                        'ip route 1.5.1.0 255.255.255.0 20.1.1.2',
                    'unconfig': 'no interface vlan 10\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'no ip route 1.5.1.0 255.255.255.0 20.1.1.2',
                }
            },
            'uut': {
                '1': {
                    'config': \
                        'interface vlan 10\n'\
                        'ip address 20.1.1.2 255.255.255.0\n'\
                        'no shut\n'\
                        '!\n'\
                        'default interface GigabitEthernet1/0/16\n'\
                        'interface GigabitEthernet1/0/16\n'\
                        'switchport mode access\n'\
                        'switchport access vlan 10\n'\
                        'no shut\n'\
                        'exit\n'\
                        'interface loopback 10\n'\
                        'ip address 1.5.1.1 255.255.255.0\n'\
                        'no shut\n'\
                        '!',
                    'unconfig': 'no interface vlan 10\n'\
                                'no vlan 10\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'no interface loopback 10',
                    'sleep': 40
                }
            }
        }
    }

    Etherchannel_LACP_ping_check = {
        'devices': {
            'helper': {
                '1': {
                    'config': 'vlan 11\n'\
                              'spanning-tree mode rapid-pvst\n'\
                              'interface Vlan11\n'\
                              'ip address 1.2.1.1 255.255.255.0\n'\
                              'no shut\n'\
                              '!\n'\
                              'default int GigabitEthernet1/0/1\n'\
                              'interface GigabitEthernet1/0/1\n'\
                              'switchport trunk encapsulation dot1q\n'\
                              'switchport mode trunk\n'\
                              'switchport trunk allowed vlan 11\n'\
                              'channel-group 10 mode passive\n'\
                              'no shut\n'\
                              '!\n'\
                              'default int GigabitEthernet1/0/2\n'\
                              'interface GigabitEthernet1/0/2\n'\
                              'switchport trunk encapsulation dot1q\n'\
                              'switchport mode trunk\n'\
                              'switchport trunk allowed vlan 11\n'\
                              'channel-group 10 mode passive\n'\
                              'no shut\n'\
                              '!\n'\
                              'default int GigabitEthernet1/0/3\n'\
                              'interface GigabitEthernet1/0/3\n'\
                              'switchport trunk encapsulation dot1q\n'\
                              'switchport mode trunk\n'\
                              'switchport trunk allowed vlan 11\n'\
                              'channel-group 10 mode passive\n'\
                              'no shut\n'\
                              '!\n'\
                              'loggin buffer 500000 debugging',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'no vlan 11\n'\
                                'no interface vlan 11\n'\
                                'no interface Port-channel10\n'\
                                'no spanning-tree mode rapid-pvst',
                }
            },
            'uut': {
                '1': {
                    'config': 'no vlan 11\n'\
                            'vlan 11\n'\
                            'spanning-tree mode rapid-pvst\n'\
                            'spanning-tree vlan 11\n'\
                            'no interface Vlan11\n'\
                            'no interface Po10\n'\
                            'interface Vlan11\n'\
                            'ip address 1.2.1.2 255.255.255.0\n'\
                            'no shut\n'\
                            'default interface GigabitEthernet1/0/15\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 11\n'\
                            'no shut\n'\
                            'default interface GigabitEthernet1/0/16\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 11\n'\
                            'no shut\n'\
                            'default interface GigabitEthernet1/0/17\n'\
                            'interface GigabitEthernet1/0/17\n'\
                            'switchport mode trunk\n'\
                            'switchport trunk allowed vlan 11\n'\
                            'no shut\n'\
                            '!\n'\
                            'loggin buffer 500000 debugging',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface GigabitEthernet1/0/17\n'\
                                'no interface vlan11\n'\
                                'no vlan 11\n'\
                                'no interface Port-channel10\n'\
                                'no spanning-tree mode rapid-pvst',
                    'sleep': 40
                }
            }
        }
    }

    Etherchannel_PAGP_ping_check = {        
        'devices': {
            'helper': {
                '1': {
                    'config': 'vlan 11\n'\
                              'spanning-tree mode rapid-pvst\n'\
                              '!\n'\
                              'interface Vlan11\n'\
                              'ip address 1.2.1.1 255.255.255.0\n'\
                              'no shut\n'\
                              '!\n'\
                              'default int GigabitEthernet1/0/1\n'\
                              'interface GigabitEthernet1/0/1\n'\
                              'switchport mode access\n'\
                              'switchport access vlan 11\n'\
                              'channel-group 10 mode desirable non-silent\n'\
                              'no shut\n'\
                              '!\n'\
                              'default int GigabitEthernet1/0/2\n'\
                              'interface GigabitEthernet1/0/2\n'\
                              'switchport mode access\n'\
                              'switchport access vlan 11\n'\
                              'channel-group 10 mode desirable non-silent\n'\
                              'no shut\n'\
                              '!\n'\
                              'default int GigabitEthernet1/0/3\n'\
                              'interface GigabitEthernet1/0/3\n'\
                              'switchport mode access\n'\
                              'switchport access vlan 11\n'\
                              'channel-group 10 mode desirable non-silent\n'\
                              'no shut\n'\
                              '!\n'\
                              'loggin buffer 500000 debugging',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'no vlan 11\n'\
                                'no interface vlan 11\n'\
                                'no interface Port-channel10\n'\
                                'no spanning-tree mode rapid-pvst',
                }
            },
            'uut': {
                '1': {
                    'config': 'no vlan 11\n'\
                            'vlan 11\n'\
                            'spanning-tree mode rapid-pvst\n'\
                            'interface Vlan11\n'\
                            'ip address 1.2.1.2 255.255.255.0\n'\
                            'no shut\n'\
                            '!\n'\
                            'default int GigabitEthernet1/0/15\n'\
                            'interface GigabitEthernet1/0/15\n'\
                            'switchport mode access\n'\
                            'switchport access vlan 11\n'\
                            'no shut\n'\
                            '!\n'\
                            'default int GigabitEthernet1/0/16\n'\
                            'interface GigabitEthernet1/0/16\n'\
                            'switchport mode access\n'\
                            'switchport access vlan 11\n'\
                            'no shut\n'\
                            '!\n'\
                            'default int GigabitEthernet1/0/17\n'\
                            'interface GigabitEthernet1/0/17\n'\
                            'switchport mode access\n'\
                            'switchport access vlan 11\n'\
                            'no shut\n'\
                            '!\n'\
                            'loggin buffer 500000 debugging',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface GigabitEthernet1/0/17\n'\
                                'no interface vlan11\n'\
                                'no vlan 11\n'\
                                'no interface Port-channel10\n'\
                                'no spanning-tree mode rapid-pvst',
                    'sleep': 30
                }
            }
        }
    }

    L3_Etherchannel_ping_check = {        
        'devices': {
            'helper': {
                '1': {
                    'config': 'default interface GigabitEthernet1/0/1\n'\
                              'interface GigabitEthernet1/0/1\n'\
                              'no switchport\n'\
                              'channel-group 10 mode desirable non-silent\n'\
                              'no shut\n'\
                              '!\n'\
                              'default interface GigabitEthernet1/0/2\n'\
                              'interface GigabitEthernet1/0/2\n'\
                              'no switchport\n'\
                              'channel-group 10 mode desirable non-silent\n'\
                              'no shut\n'\
                              '!\n'\
                              'default interface GigabitEthernet1/0/3\n'\
                              'interface GigabitEthernet1/0/3\n'\
                              'no switchport\n'\
                              'channel-group 10 mode desirable non-silent\n'\
                              'no shut\n'\
                              '!\n'\
                              'interface Po10\n'\
                              'no switchport\n'\
                              'ip address 1.2.1.1 255.255.255.0\n'\
                              'no shut\n'\
                              '!\n'\
                              'loggin buffer 500000 debugging',
                    'unconfig': 'default interface GigabitEthernet1/0/1\n'\
                                'default interface GigabitEthernet1/0/2\n'\
                                'default interface GigabitEthernet1/0/3\n'\
                                'no interface Port-channel10',
                }
            },
            'uut': {
                '1': {
                    'config': 'spanning-tree mode rapid-pvst\n'\
                              '!\n'\
                              'default interface Port-channel10\n'\
                              'interface Port-channel10\n'\
                              'no switchport\n'\
                              'no shut\n'\
                              'ip address 1.2.1.2 255.255.255.0\n'\
                              '!\n'\
                              'default interface GigabitEthernet1/0/15\n'\
                              'interface GigabitEthernet1/0/15\n'\
                              'no switchport\n'\
                              'no shut\n'\
                              '!\n'\
                              'default interface GigabitEthernet1/0/16\n'\
                              'interface GigabitEthernet1/0/16\n'\
                              'no switchport\n'\
                              'no shut\n'\
                              '!\n'\
                              'default interface GigabitEthernet1/0/17\n'\
                              'interface GigabitEthernet1/0/17\n'\
                              'no switchport\n'\
                              'no shut\n'\
                              '!\n'\
                              'loggin buffer 500000 debugging',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'default interface GigabitEthernet1/0/16\n'\
                                'default interface GigabitEthernet1/0/17\n'\
                                'no interface Port-channel10\n'\
                                'no spanning-tree mode rapid-pvst',
                    'sleep': 30
                }
            }
        }
    }

    dot1x_base_uut = 'interface vlan 1\n'\
                     '!name default\n'\
                     '!\n'\
                     'interface vlan 20\n'\
                     '!name nondefault\n'\
                     '!\n'\
                     'dot1x system-auth-control\n'\
                     '!\n'\
                     'interface GigabitEthernet1/0/15\n'\
                     'shut\n'\
                     'interface vlan1\n'\
                     'no ip address\n'\
                     'interface vlan20\n'\
                     'no ip address\n'\
                     'no shut\n'\
                     'policy-map type control subscriber dummy\n'\
                     '!\n'\
                     'no policy-map type control subscriber dummy\n'\
                     '!\n'\
                     'aaa new-model\n'\
                     'aaa session-id common\n'\
                     'aaa authentication dot1x default local\n'\
                     'aaa authorization network default local\n'\
                     'aaa local authentication default authorization default\n'\
                     'aaa authorization credential-download default local\n'\
                     '!\n'\
                     'eap profile EAP-METH\n'\
                     'method md5\n'\
                     '!\n'\
                     'interface GigabitEthernet1/0/15\n'\
                     'dot1x authenticator eap profile EAP-METH\n'\
                     'username switch password 0 cisco123\n'\
                     'username switch4 password 0 cisco123'

    dot1x_base_helper = 'line con 0\n'\
                  'exec-timeout 0 0\n'\
                  '!\n'\
                  'ip routing\n'\
                  'ip domain-name cisco\n'\
                  'cdp run\n'\
                  'dot1x system-auth-control\n'\
                  'dot1x supplicant force-multicast\n'\
                  '!\n'\
                  'ip vrf ABCD\n'\
                  '!\n'\
                  'eap profile EAP-METH\n'\
                  'method md5\n'\
                  '!\n'\
                  'dot1x credentials switch1\n'\
                  'username switch\n'\
                  'password 0 cisco123\n'\
                  '!\n'\
                  'dot1x credentials switch2\n'\
                  'username switch2\n'\
                  'password 0 cisco123\n'\
                  '!\n'\
                  'dot1x credentials switch3\n'\
                  'username switch3\n'\
                  'password 0 cisco123\n'\
                  '!\n'\
                  'dot1x credentials switch4\n'\
                  'username switch4\n'\
                  'password 0 cisco123\n'\
                  '!\n'\
                  'dot1x credentials user1\n'\
                  'username user1\n'\
                  'password 0 cisco\n'\
                  '!\n'\
                  'dot1x credentials user2\n'\
                  'username aaaaa\n'\
                  'password 0 cisco\n'\
                  '!\n'\
                  '!\n'\
                  'dot1x credentials wrong\n'\
                  'username wrong\n'\
                  'password 0 wrong'

    dot1xeapsessiondefaultvlan = {
        'devices': {
            'uut': {
                '1': {
                    'config': dot1x_base_uut,
                    'unconfig': 'no interface vlan20\n'\
                                'default interface vlan1\n'\
                                'no dot1x system-auth-control\n'\
                                'default interface GigabitEthernet1/0/15\n'\
                                'no aaa authentication dot1x default local\n'\
                                'no aaa authorization network default local\n'\
                                'no aaa authorization credential-download default local\n'\
                                'no username switch\n'\
                                'no username switch4\n'\
                                'no eap profile EAP-METH\n'\
                                'no parameter-map type webauth global\n'\
                                'no policy-map type control subscriber DOT1X\n'\
                                'no service-template DEFAULT_CRITICAL_VOICE_TEMPLATE\n'\
                                'no service-template DEFAULT_LINKSEC_POLICY_MUST_SECURE\n'\
                                'no service-template DEFAULT_LINKSEC_POLICY_SHOULD_SECURE\n'\
                                'no service-template webauth-global-inactive\n'\
                                'no aaa local authentication default authorization default\n'\
                                'no aaa new-model',
                },
                '2': {
                    'config': 'interface GigabitEthernet1/0/15\n'\
                              'dot1x authenticator eap profile EAP-METH\n'\
                              'policy-map type control subscriber DOT1X\n'\
                              'event session-started match-all\n'\
                              '1 class always do-until-failure\n'\
                              '1 authenticate using dot1x\n'\
                              'interface GigabitEthernet1/0/15\n'\
                              'no shut\n'\
                              'switchport\n'\
                              'switchport mode access\n'\
                              'switchport access vlan 1\n'\
                              'no access-session closed\n'\
                              'no switchport port-security\n'\
                              'access-session port-control auto\n'\
                              'access-session host-mode multi-auth\n'\
                              'dot1x pae authenticator\n'\
                              'dot1x authenticator eap profile EAP-METH\n'\
                              'service-policy type control subscriber DOT1X\n'\
                              'interface vlan1\n'\
                              '!no switchport\n'\
                              'ip address 1.1.1.2 255.255.255.0\n'\
                              'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/15\n'\
                                'no policy-map type control subscriber DOT1X\n'\
                                'default interface vlan 1',
                    'sleep': 45
                }
            },
            'helper': {
                '1': {
                    'config': dot1x_base_helper,
                    'unconfig': 'no dot1x system-auth-control\n'\
                                'no dot1x supplicant force-multicast\n'\
                                '!\n'\
                                'no eap profile EAP-METH\n'\
                                '!\n'\
                                'no dot1x credentials switch\n'\
                                '!\n'\
                                'default interface GigabitEthernet1/0/1\n'\
                                'no dot1x credentials switch1\n'\
                                'no dot1x credentials switch2\n'\
                                'no dot1x credentials switch3\n'\
                                'no dot1x credentials switch4\n'\
                                'no dot1x credentials user1\n'\
                                'no dot1x credentials user2\n'\
                                'no ip vrf ABCD\n'\
                                'no ip domain-name cisco\n'\
                                'no dot1x credentials wrong',
                },
                '2': {
                    'config': 'interface GigabitEthernet1/0/1\n'\
                              'no switchport\n'\
                              'ip address 1.1.1.1 255.255.255.0\n'\
                              'dot1x pae supplicant\n'\
                              'dot1x credentials switch1\n'\
                              'dot1x supplicant eap profile EAP-METH\n'\
                              'no shut',
                    'unconfig': 'default interface GigabitEthernet1/0/1',
                }
            }
        }
    }

    dot1xeapsessionWrongUser = {
        'devices': {
            'uut': {
                'peer': 'helper',
                'name': 'GigabitEthernet1/0/15',
                'peer_intf': 'GigabitEthernet1/0/1',
                '1': {
                    'config': dot1x_base_uut,
                    'unconfig': 'no interface vlan20\n'\
                                'default interface vlan1\n'\
                                'no dot1x system-auth-control\n'\
                                'default interface {name}\n'\
                                'no aaa authentication dot1x default local\n'\
                                'no aaa authorization network default local\n'\
                                'no aaa authorization credential-download default local\n'\
                                'no username switch\n'\
                                'no username switch4\n'\
                                'no eap profile EAP-METH\n'\
                                'no parameter-map type webauth global\n'\
                                'no policy-map type control subscriber DOT1X\n'\
                                'no service-template DEFAULT_CRITICAL_VOICE_TEMPLATE\n'\
                                'no service-template DEFAULT_LINKSEC_POLICY_MUST_SECURE\n'\
                                'no service-template DEFAULT_LINKSEC_POLICY_SHOULD_SECURE\n'\
                                'no service-template webauth-global-inactive\n'\
                                'no aaa local authentication default authorization default\n'\
                                'no aaa new-model',
                },
                '2': {
                    'config': 'interface {name}\n'\
                              'dot1x authenticator eap profile EAP-METH\n'\
                              'policy-map type control subscriber DOT1X\n'\
                              'event session-started match-all\n'\
                              '1 class always do-until-failure\n'\
                              '1 authenticate using dot1x\n'\
                              'interface {name}\n'\
                              'no shut\n'\
                              'switchport\n'\
                              'switchport mode access\n'\
                              'switchport access vlan 20\n'\
                              'access-session closed\n'\
                              'no switchport port-security\n'\
                              'access-session port-control auto\n'\
                              'access-session host-mode single-host\n'\
                              'dot1x pae authenticator\n'\
                              'dot1x authenticator eap profile EAP-METH\n'\
                              'service-policy type control subscriber DOT1X',
                    'unconfig': 'default interface {name}\n'\
                                'no policy-map type control subscriber DOT1X\n'\
                                'no vlan 20\n'\
                                'no interface vlan 20',
                    'sleep': 45
                }
            },
            'helper': {
                '1': {
                    'config': dot1x_base_helper,
                    'unconfig': 'no dot1x system-auth-control\n'\
                                'no dot1x supplicant force-multicast\n'\
                                '!\n'\
                                'no eap profile EAP-METH\n'\
                                '!\n'\
                                'no dot1x credentials switch\n'\
                                '!\n'\
                                'default interface {peer_intf}\n'\
                                'no dot1x credentials switch1\n'\
                                'no dot1x credentials switch2\n'\
                                'no dot1x credentials switch3\n'\
                                'no dot1x credentials switch4\n'\
                                'no dot1x credentials user1\n'\
                                'no dot1x credentials user2\n'\
                                'no ip vrf ABCD\n'\
                                'no ip domain-name cisco\n'\
                                'no dot1x credentials wrong',
                },
                '2': {
                    'config': 'interface {peer_intf}\n'\
                              'no switchport\n'\
                              'ip address 1.1.1.1 255.255.255.0\n'\
                              'dot1x pae supplicant\n'\
                              'dot1x credentials switch1\n'\
                              'dot1x supplicant eap profile EAP-METH\n'\
                              'no shut',
                    'unconfig': 'default interface {peer_intf}',
                }
            }
        }
    }
    
