''' 
Ntp Genie Ops Object Outputs for IOSXR.
'''


class NtpOutput(object):

    ShowNtpAssociations = {
        'clock_state': {
            'system_status': {
                'associations_address': '172.19.69.1',
                'associations_local_mode': 'client',
                'clock_offset': 67.16,
                'clock_refid': '172.24.114.33',
                'clock_state': 'synchronized',
                'clock_stratum': 3,
                'root_delay': 2.0}
        },
        'peer': {
            '127.127.1.1': {
                'local_mode': {
                    'client': {
                        'configured': True,
                        'delay': 0.0,
                        'jitter': 438.3,
                        'local_mode': 'client',
                        'mode': 'candidate',
                        'offset': 0.0,
                        'poll': 1024,
                        'reach': 37,
                        'receive_time': 5,
                        'refid': '127.127.1.1',
                        'remote': '127.127.1.1',
                        'stratum': 5}
                }
            },
            '172.19.69.1': {
                'local_mode': {
                    'client': {
                        'configured': True,
                        'delay': 2.0,
                        'jitter': 0.0,
                        'local_mode': 'client',
                        'mode': 'synchronized',
                        'offset': 67.16,
                        'poll': 1024,
                        'reach': 1,
                        'receive_time': 13,
                        'refid': '172.24.114.33',
                        'remote': '172.19.69.1',
                        'stratum': 3}
                }
            }
        },
        'vrf': {
            'default': {
                'address': {
                    '127.127.1.1': {
                        'isconfigured': {
                            True: {
                                'address': '127.127.1.1',
                                'isconfigured': True}
                        },
                        'type': {
                            'peer': {
                                'address': '127.127.1.1',
                                'type': 'peer',
                                'vrf': 'default'}
                        }
                    },
                    '172.19.69.1': {
                        'isconfigured': {
                            True: {
                                'address': '172.19.69.1',
                                'isconfigured': True}
                        },
                        'type': {
                            'peer': {
                                'address': '172.19.69.1',
                                'type': 'peer',
                                'vrf': 'default'}
                        }
                    }
                }
            }
        }
    }

    ShowNtpStatus = {
        'clock_state': {
            'system_status': {
                'act_freq': 1000.2725,
                'drift': '-0.0002724105 s/s',
                'last_update': '66 sec ago',
                'leap_status': "'CTRL' (Normal "
                                'Controlled Loop)',
                'nom_freq': 1000.0,
                'offset': -1.738,
                'peerdispersion': 0.09,
                'poll': 64,
                'precision': '2**24',
                'refid': '192.168.128.5',
                'reftime': 'CC95463C.9B964367 '
                           '(11:21:48.607 EST Tue Oct  '
                           '7 2008)',
                'rootdelay': 186.05,
                'rootdispersion': 53.86,
                'status': 'synchronized',
                'stratum': 3}
        }
    }

    ShowRunningConfigNtp = {
        'vrf': {
            'default': {
                'source': 'Loopback0',
                'address': {
                    '127.127.1.1': {
                        'type': 'server'},
                    '172.19.69.1': {
                        'type': 'peer'},
                }
            }
        }
    }

    Ntp_info = {
        'clock_state': {
            'system_status': {
                'actual_freq': 1000.2725,
                'associations_address': '172.19.69.1',
                'associations_local_mode': 'client',
                'clock_offset': 67.16,
                'clock_precision': '2**24',
                'clock_refid': '172.24.114.33',
                'clock_state': 'synchronized',
                'clock_stratum': 3,
                'reference_time': 'CC95463C.9B964367 '
                                  '(11:21:48.607 EST '
                                  'Tue Oct  7 2008)',
                'root_delay': 2.0,
                'root_dispersion': 53.86}
            },
        'vrf': {
            'default': {
                'associations': {
                    'address': {
                        '127.127.1.1': {
                            'local_mode': {
                                'client': {
                                    'isconfigured': {
                                        True: {
                                            'address': '127.127.1.1',
                                            'delay': 0.0,
                                            'isconfigured': True,
                                            'local_mode': 'client',
                                            'offset': 0.0,
                                            'poll': 1024,
                                            'reach': 37,
                                            'receive_time': 5,
                                            'refid': '127.127.1.1',
                                            'stratum': 5,
                                            'vrf': 'default'}
                                    }
                                }
                            }
                        },
                        '172.19.69.1': {
                            'local_mode': {
                                'client': {
                                    'isconfigured': {
                                        True: {
                                            'address': '172.19.69.1',
                                            'delay': 2.0,
                                            'isconfigured': True,
                                            'local_mode': 'client',
                                            'offset': 67.16,
                                            'poll': 1024,
                                            'reach': 1,
                                            'receive_time': 13,
                                            'refid': '172.24.114.33',
                                            'stratum': 3,
                                            'vrf': 'default'}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'unicast_configuration': {
                        'address': {
                            '127.127.1.1': {
                                'type': {
                                    'server': {
                                        'address': '127.127.1.1',
                                        'type': 'server',
                                        'vrf': 'default'}
                                }
                            },
                            '172.19.69.1': {
                                'type': {
                                    'peer': {
                                        'address': '172.19.69.1',
                                        'type': 'peer',
                                        'vrf': 'default'}
                                }
                            }
                        }
                    }
                }
            }
        }