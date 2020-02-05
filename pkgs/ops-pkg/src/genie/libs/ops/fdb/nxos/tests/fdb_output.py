""" Fdb Genie Ops Object Outputs for NXOS """

class FdbOutput(object):
    show_mac_address_table = """
        N95_1# show mac address-table 
        Legend: 
            * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
            age - seconds since last seen,+ - primary entry using vPC Peer-Link,
            (T) - True, (F) - False, C - ControlPlane MAC, ~ - vsan
           VLAN     MAC Address      Type      age     Secure NTFY Ports
        ---------+-----------------+--------+---------+------+----+---------------
        *   10     aaaa.bbbb.cccc   static   -         F      F    Eth1/2
        *   20     aaaa.bbbb.cccc   static   -         F      F    Drop
        *   30     aaaa.bbbb.cccc   static   -         F      F    Drop
        G    -     0000.dead.beef   static   -         F      F    sup-eth1(R)
        G    -     5e00.c000.0007   static   -         F      F     (R)
        G    -     5e00.c000.0007   static   -         F      F  sup-eth1(R) (Lo0)
        G  100     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  101     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  102     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  103     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  105     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  106     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  107     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  108     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  109     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  110     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  111     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  112     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  113     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G  114     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G 1000     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G 1005     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G 1006     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G 1007     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G 1008     5e00.c000.0007   static   -         F      F    sup-eth1(R)
        G 1009     5e00.c000.0007   static   -         F      F    sup-eth1(R)
          2000     7e00.c000.0007    static       -       F    F  vPC Peer-Link(R)
          3000     5e00.c000.0007   static   -         F      F    sup-eth1(R)
          4000     5e00.c000.0007   static   ~~~         F      F    sup-eth1(R)
    """

    show_mac_address_table_custom = """
            N95_1# show mac address-table 
            Legend: 
                * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
                age - seconds since last seen,+ - primary entry using vPC Peer-Link,
                (T) - True, (F) - False, C - ControlPlane MAC, ~ - vsan
               VLAN     MAC Address      Type      age     Secure NTFY Ports
            ---------+-----------------+--------+---------+------+----+---------------
              8000     5e00.c000.0007   static   ~~~         F      F    Eth1/3
        """

    show_mac_address_table_aging_time = """
        N95_1# show mac address-table aging-time 
        Aging Time
        ----------
            120
    """

    show_system_internal_l2fwder_mac = """
        N95_1# show system internal l2fwder mac
        Legend: 
            * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
            age - seconds since last seen,+ - primary entry using vPC Peer-Link,
            (T) - True, (F) - False, C - ControlPlane MAC
           VLAN     MAC Address      Type      age     Secure NTFY Ports
        ---------+-----------------+--------+---------+------+----+---------------
        G   114    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   112    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   113    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   110    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   111    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   108    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   109    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   106    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   107    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   105    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   102    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   103    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   100    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G   101    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G     -    5e00:c000:0007    static   -          F     F   sup-eth1(R)
        *     1    fa16.3eef.6e79   dynamic   00:01:02   F     F     Eth1/4  
        *   100    fa16.3eef.6e79   dynamic   00:05:38   F     F     Eth1/4  
        G  1008    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G  1009    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G  1006    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G  1007    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G  1005    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        G  1000    5e00.c000.0007    static   -          F     F   sup-eth1(R)
        *    10    aaaa.bbbb.cccc    static   -          F     F     Eth1/2
            1           1         -00:00:de:ad:be:ef         -             1
    """

    fdb_info = {
        'mac_aging_time': 120,
        'mac_table': {
            'vlans': {
                '4000': {
                    'vlan': '4000',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '~~~',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '3000': {
                    'vlan': '3000',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '2000': {
                    'vlan': '2000',
                    'mac_addresses': {
                        '7e00.c000.0007': {
                            'mac_address': '7e00.c000.0007',
                            'interfaces': {
                                'vPC Peer-Link(R)': {
                                    'interface': 'vPC Peer-Link(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '1009': {
                    'vlan': '1009',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '1008': {
                    'vlan': '1008',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '1007': {
                    'vlan': '1007',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '1006': {
                    'vlan': '1006',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '1005': {
                    'vlan': '1005',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '1000': {
                    'vlan': '1000',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '114': {
                    'vlan': '114',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '113': {
                    'vlan': '113',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '112': {
                    'vlan': '112',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '111': {
                    'vlan': '111',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '110': {
                    'vlan': '110',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '109': {
                    'vlan': '109',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '108': {
                    'vlan': '108',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '107': {
                    'vlan': '107',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '106': {
                    'vlan': '106',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '105': {
                    'vlan': '105',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '103': {
                    'vlan': '103',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '102': {
                    'vlan': '102',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '101': {
                    'vlan': '101',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '100': {
                    'vlan': '100',
                    'mac_addresses': {
                        '5e00.c000.0007': {
                            'mac_address': '5e00.c000.0007',
                            'interfaces': {
                                'Sup-eth1(R)': {
                                    'interface': 'Sup-eth1(R)',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                },
                '30': {
                    'vlan': '30',
                    'mac_addresses': {
                        'aaaa.bbbb.cccc': {
                            'mac_address': 'aaaa.bbbb.cccc',
                            'drop': {
                                'drop': True,
                                'age': '-',
                                'entry_type': 'static'
                            }
                        }
                    }
                },
                '20': {
                    'vlan': '20',
                    'mac_addresses': {
                        'aaaa.bbbb.cccc': {
                            'mac_address': 'aaaa.bbbb.cccc',
                            'drop': {
                                'drop': True,
                                'age': '-',
                                'entry_type': 'static'
                            }
                        }
                    }
                },
                '10': {
                    'vlan': '10',
                    'mac_addresses': {
                        'aaaa.bbbb.cccc': {
                            'mac_address': 'aaaa.bbbb.cccc',
                            'interfaces': {
                                'Ethernet1/2': {
                                    'interface': 'Ethernet1/2',
                                    'age': '-',
                                    'entry_type': 'static'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
