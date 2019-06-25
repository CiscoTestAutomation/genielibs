''' 
Ntp Genie Ops Object Outputs for NXOS.
'''


class NtpOutput(object):

    ShowNtpPeerStatus = {
       'clock_state': {'system_status': {'associations_address': '10.4.1.1',
                                          'clock_state': 'synchronized',
                                          'clock_stratum': 8,
                                          'root_delay': 0.01311}},
        'vrf': {
            'default': {
                'peer': {'10.4.1.1': {'delay': 0.01311,
                                     'local': '0.0.0.0',
                                     'mode': 'synchronized',
                                     'poll': 16,
                                     'reach': 377,
                                     'remote': '10.4.1.1',
                                     'stratum': 8,
                                     'vrf': 'default'},
                        '10.16.2.2': {'delay': 0.01062,
                                  'local': '0.0.0.0',
                                  'mode': 'client',
                                  'poll': 16,
                                  'reach': 377,
                                  'remote': '10.16.2.2',
                                  'stratum': 9,
                                  'vrf': 'default'},
                        '10.100.5.5': {'delay': 0.0,
                                  'local': '0.0.0.0',
                                  'mode': 'client',
                                  'poll': 64,
                                  'reach': 0,
                                  'remote': '10.100.5.5',
                                  'stratum': 16,
                                  'vrf': 'default'}
                }
            },
            'VRF1': {
                'peer': {'10.64.4.4': {'delay': 0.0,
                                     'local': '0.0.0.0',
                                     'mode': 'client',
                                     'poll': 256,
                                     'reach': 0,
                                     'remote': '10.64.4.4',
                                     'stratum': 16,
                                     'vrf': 'VRF1'}
                }
            },
        },
        'total_peers': 4
    }

    ShowNtpPeers = {
        'peer': {'10.4.1.1': {'isconfigured': {'True': {'address': '10.4.1.1',
                                                       'isconfigured': True,
                                                       'type': 'server'}}},
                 '10.16.2.2': {'isconfigured': {'True': {'address': '10.16.2.2',
                                                       'isconfigured': True,
                                                       'type': 'server'}}},
                 '10.64.4.4': {'isconfigured': {'True': {'address': '10.64.4.4',
                                                       'isconfigured': True,
                                                       'type': 'server'}}},
                 '10.100.5.5': {'isconfigured': {'True': {'address': '10.100.5.5',
                                                       'isconfigured': True,
                                                       'type': 'server'}}}}
    }

    Ntp_info = {
        "clock_state": {
            "system_status": {
               "associations_address": "10.4.1.1",
               "clock_stratum": 8,
               "clock_state": "synchronized",
               "root_delay": 0.01311
            }
        },
        "vrf": {
            "default": {
                "associations": {
                    "address": {
                         "10.16.2.2": {
                              "local_mode": {
                                   "client": {
                                        "isconfigured": {
                                             "True": {
                                                  "reach": 377,
                                                  "stratum": 9,
                                                  "poll": 16,
                                                  "address": "10.16.2.2",
                                                  "delay": 0.01062,
                                                  "vrf": "default",
                                                  "isconfigured": True,
                                                  "local_mode": "client"
                                             }
                                        }
                                   }
                              }
                         },
                         "10.100.5.5": {
                              "local_mode": {
                                   "client": {
                                        "isconfigured": {
                                             "True": {
                                                  "reach": 0,
                                                  "stratum": 16,
                                                  "poll": 64,
                                                  "address": "10.100.5.5",
                                                  "delay": 0.0,
                                                  "vrf": "default",
                                                  "isconfigured": True,
                                                  "local_mode": "client"
                                             }
                                        }
                                   }
                              }
                         }
                    }
                },
                "unicast_configuration": {
                    "address": {
                         "10.16.2.2": {
                              "type": {
                                   "server": {
                                        "address": "10.16.2.2",
                                        "source": "0.0.0.0",
                                        "type": "server",
                                        "vrf": "default"
                                   }
                              }
                         },
                         "10.100.5.5": {
                              "type": {
                                   "server": {
                                        "address": "10.100.5.5",
                                        "source": "0.0.0.0",
                                        "type": "server",
                                        "vrf": "default"
                                   }
                              }
                         },
                         "10.4.1.1": {
                              "type": {
                                   "server": {
                                        "address": "10.4.1.1",
                                        "source": "0.0.0.0",
                                        "type": "server",
                                        "vrf": "default"
                                   }
                              }
                         }
                    }
               }
            },
            "VRF1": {
                "associations": {
                    "address": {
                         "10.64.4.4": {
                              "local_mode": {
                                   "client": {
                                        "isconfigured": {
                                             "True": {
                                                  "reach": 0,
                                                  "stratum": 16,
                                                  "poll": 256,
                                                  "address": "10.64.4.4",
                                                  "delay": 0.0,
                                                  "vrf": "VRF1",
                                                  "isconfigured": True,
                                                  "local_mode": "client"
                                             }
                                        }
                                   }
                              }
                         }
                    }
                },
                "unicast_configuration": {
                    "address": {
                         "10.64.4.4": {
                              "type": {
                                   "server": {
                                        "address": "10.64.4.4",
                                        "source": "0.0.0.0",
                                        "type": "server",
                                        "vrf": "VRF1"
                                   }
                              }
                         }
                    }
                }
            }
        }
    }


class NtpOutputNoConfig(object):

    ShowNtpPeers = '''
        --------------------------------------------------
        Peer IP Address               Serv/Peer          
      --------------------------------------------------
        127.127.1.0                   Server (configured)
    '''

    ShowNtpPeerStatus = '''
        Total peers : 1
        * - selected for sync, + -  peer mode(active), 
        - - peer mode(passive), = - polled in client mode 
            remote                                 local                                   st   poll   reach delay   vrf
        -----------------------------------------------------------------------------------------------------------------------
        *127.127.1.0                             0.0.0.0                                  3   16       1   0.00000

    '''

    Ntp_info = {
        "vrf": {
            "default": {
                 "unicast_configuration": {
                      "address": {
                           "127.127.1.0": {
                                "type": {
                                     "server": {
                                          "source": "0.0.0.0",
                                          "type": "server",
                                          "address": "127.127.1.0",
                                          "vrf": "default"
                                     }
                                }
                           }
                      }
                 }
            }
        },
        "clock_state": {
            "system_status": {
                 "clock_state": "synchronized",
                 "clock_stratum": 3,
                 "root_delay": 0.0,
                 "associations_address": "127.127.1.0"
            }
        }
    }
