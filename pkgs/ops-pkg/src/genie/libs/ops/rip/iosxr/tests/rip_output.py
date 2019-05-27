"""
Rip Genie Ops Object Outputs for IOSXE.
"""


class RipOutput(object):

    show_vrf_all_detail = {
        "VRF1": {
            "description": "not set",
            "vrf_mode": "regular",
            "address_family": {
                 "ipv6 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"
                           },
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"
                           },
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"
                           },
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"
                           }
                      }
                 },
                 "ipv4 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"
                           },
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"
                           },
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"
                           },
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"
                           }
                      }
                 }
            },
            "route_distinguisher": "200:1",
            "interfaces": [
                 "GigabitEthernet0/0/0/1"
            ]
            }
    }

    show_rip = ''' \
        RP/0/RP0/CPU0:R1#show rip                                                                                                      
        Wed Jan 30 18:47:49.312 UTC                                                     
                                                                                        
        RIP config:                                                                     
        Active:                    Yes                                                  
        Added to socket:           Yes                                                  
        Out-of-memory state:        Normal                                              
        Version:                    2                                                   
        Default metric:             3                                                   
        Maximum paths:              4                                                   
        Auto summarize:            No                                                   
        Broadcast for V2:          No                                                   
        Packet source validation:  Yes                                                  
        NSF:                        Disabled                                            
        Timers: Update:             10 seconds (7 seconds until next update)            
                Invalid:            31 seconds                                          
                Holddown:           32 seconds                                          
                Flush:              33 seconds 
    '''

    show_rip_vrf1 = ''' \
        RP/0/RP0/CPU0:R1#show rip vrf VRF1                                               
        Wed Jan 30 18:48:40.235 UTC                                                     
                                                                                
                                                                                
        VRF: VRF1                                                                       
        =======================================                                         
        RIP config:                                                                     
        Active:                    Yes                                                  
        Added to socket:           Yes                                                  
        Out-of-memory state:        Normal                                              
        Version:                    2                                                   
        Default metric:             1                                                   
        Maximum paths:              4                                                   
        Auto summarize:            No                                                   
        Broadcast for V2:          No                                                   
        Packet source validation:  No                                                   
        NSF:                        Disabled                                            
        Timers: Update:             30 seconds (18 seconds until next update)           
                Invalid:            180 seconds                                         
                Holddown:           180 seconds                                         
                Flush:              240 seconds
    '''

    show_rip_statistics = ''' \
        RP/0/RP0/CPU0:R1#show rip statistics                                            
        Wed Jan 30 18:50:57.778 UTC                                                     
                                                                                        
        RIP statistics:                                                                 
        Total messages sent:        5294                                                
        Message send failures:      0                                                   
        Regular updates sent:       2944                                                
        Queries responsed to:       0                                                   
        RIB updates:                4365                                                
        Total packets received:     4896                                                
        Discarded packets:          0                                                   
        Discarded routes:           4760                                                
        Packet received at standby: 0                                                   
        Number of routes allocated: 9                                                   
        Number of paths allocated:  6                                                   
        Route malloc failures:      0                                                   
        Path malloc failures:       0   
    '''

    show_rip_vrf1_statistics = ''' \
        RP/0/RP0/CPU0:R1#show rip vrf VRF1 statistics                                   
        Wed Jan 30 18:51:24.635 UTC                                                     
                                                                                        
        RIP statistics:                                                                 
        Total messages sent:        995                                                 
        Message send failures:      0                                                   
        Regular updates sent:       988                                                 
        Queries responsed to:       0                                                   
        RIB updates:                6                                                   
        Total packets received:     495                                                 
        Discarded packets:          0                                                   
        Discarded routes:           0                                                   
        Packet received at standby: 0                                                   
        Number of routes allocated: 11                                                  
        Number of paths allocated:  7                                                   
        Route malloc failures:      0                                                   
        Path malloc failures:       0 
    '''

    show_rip_database = ''' \
        RP/0/RP0/CPU0:R1#show rip database
        Wed Jan 30 18:48:59.532 UTC                                                     
                                                                                
        Routes held in RIP's topology database:                                         
        10.1.2.0/24                                                                     
            [0]    directly connected, GigabitEthernet0/0/0/0.100                       
        10.1.3.0/24                                                                     
            [0]    directly connected, GigabitEthernet0/0/0/1.100                       
        10.0.0.0/8    auto-summary                                                      
        172.16.1.0/24                                                                   
            [3] distance: 0    redistributed                                            
        172.16.11.0/24                                                                  
            [3] distance: 1    redistributed                                            
        172.16.22.0/24                                                                  
            [11] via 10.1.2.2, next hop 10.1.2.2, Uptime: 15s, GigabitEthernet0/0/0/0.100                                                                               
        172.16.0.0/16    auto-summary                                                   
        192.168.1.1/32                                                                  
            [3] distance: 0    redistributed                                            
        192.168.1.0/24    auto-summary 
    '''

    show_rip_vrf1_database = ''' \
        RP/0/RP0/CPU0:R1#show rip vrf VRF1 database  
        Wed Jan 30 18:49:22.086 UTC                                                     
                                                                                
        Routes held in RIP's topology database:                                         
        10.1.2.0/24                                                                     
            [0]    directly connected, GigabitEthernet0/0/0/0.200                       
        10.1.3.0/24                                                                     
            [0]    directly connected, GigabitEthernet0/0/0/1.200                       
        10.2.3.0/24                                                                     
            [1] via 10.1.2.2, next hop 10.1.2.2, Uptime: 10s, GigabitEthernet0/0/0/0.200
        10.0.0.0/8    auto-summary                                                      
        172.16.11.0/24                                                                  
            [15] distance: 1    redistributed                                           
        172.16.22.0/24                                                                  
            [1] via 10.1.2.2, next hop 10.1.2.2, Uptime: 10s, GigabitEthernet0/0/0/0.200
        172.16.0.0/16    auto-summary                                                   
        192.168.1.1/32                                                                  
            [1] distance: 0    redistributed                                            
        192.168.1.0/24    auto-summary                                                  
        192.168.2.2/32                                                                  
            [1] via 10.1.2.2, next hop 10.1.2.2, Uptime: 10s, GigabitEthernet0/0/0/0.200
        192.168.2.0/24    auto-summary
    '''

    show_rip_interface = ''' \
        RP/0/RP0/CPU0:R1#show rip interface  
        Wed Jan 30 18:49:59.943 UTC                                                     
                                                                                
        GigabitEthernet0/0/0/0.100                                                      
        Rip enabled?:               Passive                                             
        Out-of-memory state:        Normal                                              
        Broadcast for V2:           No                                                  
        Accept Metric 0:           No                                                   
        Send versions:              2                                                   
        Receive versions:           2                                                   
        Interface state:            Up                                                  
        IP address:                 10.1.2.1/24                                         
        Metric Cost:                0                                                   
        Split horizon:              Enabled                                             
        Poison Reverse:             Disabled                                            
        Socket set options:                                                             
            Joined multicast group:    Yes                                              
            LPTS filter set:           Yes                                              
        Authentication mode:        None                                                
        Authentication keychain:    Not set                                             
                                                                                        
        Total packets received: 4877                                                  
        Authentication mode is not set                                                
        RIP peers attached to this interface:                                           
            10.1.2.2                                                                    
                uptime (sec): 2    version: 2                                           
                packets discarded: 0    routes discarded: 4733                          
                                                                                        
        GigabitEthernet0/0/0/1.100                                                      
        Rip enabled?:               Yes                                                 
        Out-of-memory state:        Normal                                              
        Broadcast for V2:           No                                                  
        Accept Metric 0:           No                                                   
        Send versions:              2                                                   
        Receive versions:           2                                                   
        Interface state:            Up                                                  
        IP address:                 10.1.3.1/24                                         
        Metric Cost:                0                                                   
        Split horizon:              Enabled                                             
        Poison Reverse:             Disabled                                            
        Socket set options:                                                             
            Joined multicast group:    Yes                                              
            LPTS filter set:           Yes                                              
        Authentication mode:        None                                                
        Authentication keychain:    Not set                                             
                                                                                        
        Total packets received: 0                                                     
        Authentication mode is not set
    '''

    show_rip_vrf1_interface = ''' \
        RP/0/RP0/CPU0:R1#show rip vrf VRF1 interface 
        Wed Jan 30 18:50:24.640 UTC                                                     
                                                                                
        GigabitEthernet0/0/0/0.200                                                      
        Rip enabled?:               Yes                                                 
        Out-of-memory state:        Normal                                              
        Broadcast for V2:           No                                                  
        Accept Metric 0:           No                                                   
        Send versions:              2                                                   
        Receive versions:           2                                                   
        Interface state:            Up                                                  
        IP address:                 10.1.2.1/24                                         
        Metric Cost:                0                                                   
        Split horizon:              Enabled                                             
        Poison Reverse:             Disabled                                            
        Socket set options:                                                             
            Joined multicast group:    Yes                                              
            LPTS filter set:           Yes                                              
        Authentication mode:        None                                                
        Authentication keychain:    Not set                                             
                                                                                        
        Total packets received: 493                                                   
        Authentication mode is not set                                                
        RIP peers attached to this interface:                                           
            10.1.2.2                                                                    
                uptime (sec): 15    version: 2                                          
                packets discarded: 0    routes discarded: 0                             
                                                                                        
        GigabitEthernet0/0/0/1.200                                                      
        Rip enabled?:               Yes                                                 
        Out-of-memory state:        Normal                                              
        Broadcast for V2:           No                                                  
        Accept Metric 0:           No                                                   
        Send versions:              2                                                   
        Receive versions:           2                                                   
        Interface state:            Up                                                  
        IP address:                 10.1.3.1/24                                         
        Metric Cost:                0                                                   
        Split horizon:              Enabled                                             
        Poison Reverse:             Disabled                                            
        Socket set options:                                                             
            Joined multicast group:    Yes                                              
            LPTS filter set:           Yes                                              
        Authentication mode:        None                                                
        Authentication keychain:    Not set                                             
                                                                                        
        Total packets received: 0                                                     
        Authentication mode is not set  
    '''

    rip_ops_output = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'instance': {
                            'rip': {
                                'default_metric': 1,
                                'maximum_paths': 4,
                                'num_of_routes': 11,
                                'routes': {
                                    '10.1.3.0/24': {
                                        'index': {
                                            1: {
                                                'route_type': 'connected',
                                                'metric': 0,
                                                'interface': 'GigabitEthernet0/0/0/1.200'
                                            }
                                        }
                                    },
                                    '10.1.2.0/24': {
                                        'index': {
                                            1: {
                                                'route_type': 'connected',
                                                'metric': 0,
                                                'interface': 'GigabitEthernet0/0/0/0.200'
                                            }
                                        }
                                    },
                                    '192.168.2.2/32': {
                                        'index': {
                                            1: {
                                                'metric': 1,
                                                'interface': 'GigabitEthernet0/0/0/0.200',
                                                'next_hop': '10.1.2.2'
                                            }
                                        }
                                    },
                                    '192.168.1.1/32': {
                                        'index': {
                                            1: {
                                                'metric': 1,
                                                'redistributed': True
                                            }
                                        }
                                    },
                                    '172.16.22.0/24': {
                                        'index': {
                                            1: {
                                                'metric': 1,
                                                'interface': 'GigabitEthernet0/0/0/0.200',
                                                'next_hop': '10.1.2.2'
                                            }
                                        }
                                    },
                                    '172.16.11.0/24': {
                                        'index': {
                                            1: {
                                                'metric': 15,
                                                'redistributed': True
                                            }
                                        }
                                    },
                                    '10.2.3.0/24': {
                                        'index': {
                                            1: {
                                                'metric': 1,
                                                'interface': 'GigabitEthernet0/0/0/0.200',
                                                'next_hop': '10.1.2.2'
                                            }
                                        }
                                    },
                                    '192.168.2.0/24': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    },
                                    '192.168.1.0/24': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    },
                                    '172.16.0.0/16': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    },
                                    '10.0.0.0/8': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    }
                                },
                                'interfaces': {
                                    'GigabitEthernet0/0/0/1.200': {
                                        'cost': 0,
                                        'passive': False,
                                        'split_horizon': True,
                                        'poison_reverse': False,
                                        'oper_status': 'up',
                                        'authentication': {
                                            'auth_key_chain': {
                                                'key_chain': 'Not set'
                                            },
                                            'auth_key': {
                                                'crypto_algorithm': 'None'
                                            }
                                        }
                                    },
                                    'GigabitEthernet0/0/0/0.200': {
                                        'cost': 0,
                                        'passive': False,
                                        'split_horizon': True,
                                        'poison_reverse': False,
                                        'oper_status': 'up',
                                        'authentication': {
                                            'auth_key_chain': {
                                                'key_chain': 'Not set'
                                            },
                                            'auth_key': {
                                                'crypto_algorithm': 'None'
                                            }
                                        },
                                        'neighbors': {
                                            '10.1.2.2': {
                                                'address': '10.1.2.2'
                                            }
                                        }
                                    }
                                },
                                'timers': {
                                    'flush_interval': 240,
                                    'holddown_interval': 180,
                                    'invalid_interval': 180,
                                    'update_interval': 30
                                }
                            }
                        }
                    }
                }
            },
            'default': {
                'address_family': {
                    'ipv4': {
                        'instance': {
                            'rip': {
                                'default_metric': 3,
                                'maximum_paths': 4,
                                'num_of_routes': 9,
                                'routes': {
                                    '10.1.3.0/24': {
                                        'index': {
                                            1: {
                                                'route_type': 'connected',
                                                'metric': 0,
                                                'interface': 'GigabitEthernet0/0/0/1.100'
                                            }
                                        }
                                    },
                                    '10.1.2.0/24': {
                                        'index': {
                                            1: {
                                                'route_type': 'connected',
                                                'metric': 0,
                                                'interface': 'GigabitEthernet0/0/0/0.100'
                                            }
                                        }
                                    },
                                    '192.168.1.1/32': {
                                        'index': {
                                            1: {
                                                'metric': 3,
                                                'redistributed': True
                                            }
                                        }
                                    },
                                    '172.16.22.0/24': {
                                        'index': {
                                            1: {
                                                'metric': 11,
                                                'interface': 'GigabitEthernet0/0/0/0.100',
                                                'next_hop': '10.1.2.2'
                                            }
                                        }
                                    },
                                    '172.16.11.0/24': {
                                        'index': {
                                            1: {
                                                'metric': 3,
                                                'redistributed': True
                                            }
                                        }
                                    },
                                    '172.16.1.0/24': {
                                        'index': {
                                            1: {
                                                'metric': 3,
                                                'redistributed': True
                                            }
                                        }
                                    },
                                    '192.168.1.0/24': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    },
                                    '172.16.0.0/16': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    },
                                    '10.0.0.0/8': {
                                        'index': {
                                            1: {
                                                'summary_type': 'auto-summary'
                                            }
                                        }
                                    }
                                },
                                'interfaces': {
                                    'GigabitEthernet0/0/0/1.100': {
                                        'cost': 0,
                                        'passive': False,
                                        'split_horizon': True,
                                        'poison_reverse': False,
                                        'oper_status': 'up',
                                        'authentication': {
                                            'auth_key_chain': {
                                                'key_chain': 'Not set'
                                            },
                                            'auth_key': {
                                                'crypto_algorithm': 'None'
                                            }
                                        }
                                    },
                                    'GigabitEthernet0/0/0/0.100': {
                                        'cost': 0,
                                        'passive': True,
                                        'split_horizon': True,
                                        'poison_reverse': False,
                                        'oper_status': 'up',
                                        'authentication': {
                                            'auth_key_chain': {
                                                'key_chain': 'Not set'
                                            },
                                            'auth_key': {
                                                'crypto_algorithm': 'None'
                                            }
                                        },
                                        'neighbors': {
                                            '10.1.2.2': {
                                                'address': '10.1.2.2'
                                            }
                                        }
                                    }
                                },
                                'timers': {
                                    'flush_interval': 33,
                                    'holddown_interval': 32,
                                    'invalid_interval': 31,
                                    'update_interval': 10
                                }
                            }
                        }
                    }
                }
            }
        }
    }