''' 
Ntp Genie Ops Object Outputs for IOSXE.
'''


class NtpOutput(object):

    ShowNtpAssociations = {
    'clock_state':
        {'system_status':
            {'associations_address': '127.127.1.1',
             'associations_local_mode': 'client',
             'clock_offset': 0.0,
             'clock_refid': '.LOCL.',
             'clock_state': 'synchronized',
             'clock_stratum': 0,
             'root_delay': 0.0}
            },
    'peer':
        {'10.4.1.1':
            {'local_mode':
                {'client':
                    {'delay': 0.0,
                    'jitter': 15937.0,
                    'mode': 'configured',
                    'offset': 0.0,
                    'poll': 1024,
                    'reach': 0,
                    'receive_time': '-',
                    'refid': '.INIT.',
                    'remote': '10.4.1.1',
                    'stratum': 16,
                    'local_mode': 'client'}
                }
            },
        '127.127.1.1':
            {'local_mode':
                {'client':
                    {'delay': 0.0,
                    'jitter': 1.204,
                    'mode': 'synchronized',
                    'offset': 0.0,
                    'poll': 16,
                    'reach': 377,
                    'receive_time': 6,
                    'refid': '.LOCL.',
                    'remote': '127.127.1.1',
                    'stratum': 0,
                    'local_mode': 'client'}
                }
            },
        '10.16.2.2':
            {'local_mode':
                {'client':
                    {'delay': 0.0,
                    'jitter': 15937.0,
                    'mode': 'configured',
                    'offset': 0.0,
                    'poll': 1024,
                    'reach': 0,
                    'receive_time': '-',
                    'refid': '.INIT.',
                    'remote': '10.16.2.2',
                    'stratum': 16,
                    'local_mode': 'client'}
                }
            }
        }
    }

    ShowNtpStatus = {
        'clock_state': {'system_status': {'act_freq': 250.0,
                                   'drift': '0.000000000 s/s',
                                   'last_update': '9 sec ago',
                                   'leap_status': "'CTRL' (Normal "
                                                  'Controlled Loop)',
                                   'nom_freq': 250.0,
                                   'offset': 0.0,
                                   'peerdispersion': 1.2,
                                   'poll': 16,
                                   'precision': '2**10',
                                   'refid': '.LOCL.',
                                   'reftime': 'DF9FFBA0.8B020DC8 '
                                              '(15:43:28.543 UTC Wed Nov '
                                              '21 2018)',
                                   'resolution': 4000,
                                   'rootdelay': 0.0,
                                   'rootdispersion': 2.31,
                                   'status': 'synchronized',
                                   'stratum': 1,
                                   'uptime': '1921500 (1/100 of seconds)'}}
    }

    ShowNtpConfig = {
        'vrf': {
            'VRF1': {
                'address': {
                    '10.64.4.4': {
                        'isconfigured': {
                            'True': {
                                'address': '10.64.4.4',
                                'isconfigured': True}
                        },
                        'type': {
                            'server': {
                                'address': '10.64.4.4',
                                'type': 'server',
                                'vrf': 'VRF1'}
                        }
                    }
                }
            },
            'default': {
                'address': {
                    '10.4.1.1': {
                        'isconfigured': {
                            'True': {
                                'address': '10.4.1.1',
                                'isconfigured': True}
                            },
                        'type': {
                            'server': {
                                'address': '10.4.1.1',
                                'type': 'server',
                                'vrf': 'default'}
                        }
                    },
                    '10.16.2.2': {
                        'isconfigured': {
                            'True': {
                                'address': '10.16.2.2',
                                'isconfigured': True}
                        },
                        'type': {
                            'server': {
                                'address': '10.16.2.2',
                                'type': 'server',
                                'vrf': 'default'}
                        }
                    }
                }
            }
        }
    }

    Ntp_info = {
    'clock_state': {
        'system_status': {
            'associations_address': '127.127.1.1',
            'associations_local_mode': 'client',
            'clock_offset': 0.0,
            'clock_precision': '2**10',
            'clock_refid': '.LOCL.',
            'clock_state': 'synchronized',
            'clock_stratum': 0,
            'reference_time': 'DF9FFBA0.8B020DC8 '
                              '(15:43:28.543 UTC '
                              'Wed Nov 21 2018)',
            'root_delay': 0.0,
            'root_dispersion': 2.31}
        },
    'vrf': {
        'VRF1': {
            'associations': {
                'address': {
                    '10.64.4.4': {
                        'isconfigured': {
                            'True': {
                                'address': '10.64.4.4',
                                'isconfigured': True}
                        }
                    }
                }
            },
            'unicast_configuration': {
                'address': {
                    '10.64.4.4': {
                        'type': {
                            'server': {
                                'address': '10.64.4.4',
                                'type': 'server',
                                'vrf': 'VRF1'}
                        }
                    }
                }
            }
        },
        'default': {
            'associations': {
                'address': {
                    '10.4.1.1': {
                        'local_mode': {
                            'client': {
                                'isconfigured': {
                                    True: {
                                        'address': '10.4.1.1',
                                        'delay': 0.0,
                                        'isconfigured': True,
                                        'local_mode': 'client',
                                        'offset': 0.0,
                                        'poll': 1024,
                                        'reach': 0,
                                        'receive_time': '-',
                                        'refid': '.INIT.',
                                        'stratum': 16,
                                        'vrf': 'default'}
                                }
                            }
                        }
                    },
                    '127.127.1.1': {
                        'local_mode': {
                            'client': {
                                'isconfigured': {
                                    False: {
                                        'address': '127.127.1.1',
                                        'delay': 0.0,
                                        'isconfigured': False,
                                        'local_mode': 'client',
                                        'offset': 0.0,
                                        'poll': 16,
                                        'reach': 377,
                                        'receive_time': 6,
                                        'refid': '.LOCL.',
                                        'stratum': 0,
                                        'vrf': 'default'}
                                }
                            }
                        }
                    },
                    '10.16.2.2': {
                        'local_mode': {
                            'client': {
                                'isconfigured': {
                                    True: {
                                        'address': '10.16.2.2',
                                        'delay': 0.0,
                                        'isconfigured': True,
                                        'local_mode': 'client',
                                        'offset': 0.0,
                                        'poll': 1024,
                                        'reach': 0,
                                        'receive_time': '-',
                                        'refid': '.INIT.',
                                        'stratum': 16,
                                        'vrf': 'default'}
                                }
                            }
                        }
                    }
                }
            },
            'unicast_configuration': {
                'address': {
                    '10.4.1.1': {
                        'type': {
                            'server': {
                                'address': '10.4.1.1',
                                'type': 'server',
                                'vrf': 'default'}
                        }
                    },
                    '10.16.2.2': {
                        'type': {
                            'server': {
                                'address': '10.16.2.2',
                                'type': 'server',
                                'vrf': 'default'}
                        }
                    }
                }
            }
        }
    }
}


class NtpOutputNoConfig(object):

    ShowNtpStatus = '''
        show ntp status
        Clock is synchronized, stratum 3, reference is 127.127.1.1
        nominal freq is 1000.0003 Hz, actual freq is 1000.0003 Hz, precision is 2**14
        ntp uptime is 110800 (1/100 of seconds), resolution is 1000
        reference time is DFA7FD64.3BFF4486 (12:29:08.234 EST Tue Nov 27 2018)
        clock offset is 0.0000 msec, root delay is 0.00 msec
        root dispersion is 0.51 msec, peer dispersion is 0.29 msec
        loopfilter state is 'CTRL' (Normal Controlled Loop), drift is 0.000000000 s/s
        system poll interval is 16, last update was 11 sec ago.
    '''

    ShowNtpAssociations = '''
        show ntp associations

          address         ref clock       st   when   poll reach  delay  offset   disp
        *~127.127.1.1     .LOCL.           2     10     16   377  0.000   0.000  0.292
         * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
    '''

    ShowNtpConfig = '''
        show ntp config
    '''

    Ntp_info = {
        'clock_state': {
            'system_status': {
                'associations_address': '127.127.1.1',
                'associations_local_mode': 'client',
                'clock_offset': 0.0,
                'clock_precision': '2**14',
                'clock_refid': '.LOCL.',
                'clock_state': 'synchronized',
                'clock_stratum': 2,
                'reference_time': 'DFA7FD64.3BFF4486 '
                                  '(12:29:08.234 EST '
                                  'Tue Nov 27 2018)',
                'root_delay': 0.0,
                'root_dispersion': 0.51}
        },
        'vrf': {
            'default': {
                'associations': {
                    'address': {
                        '127.127.1.1': {
                            'local_mode': {
                                'client': {
                                    'isconfigured': {
                                        False: {
                                            'address': '127.127.1.1',
                                            'delay': 0.0,
                                            'isconfigured': False,
                                            'local_mode': 'client',
                                            'offset': 0.0,
                                            'poll': 16,
                                            'reach': 377,
                                            'receive_time': 10,
                                            'refid': '.LOCL.',
                                            'stratum': 2,
                                            'vrf': 'default'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }