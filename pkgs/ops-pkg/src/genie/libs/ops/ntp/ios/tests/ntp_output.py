''' 
Ntp Genie Ops Object Outputs for IOS.
'''


class NtpOutput(object):

	ShowNtpAssociations = {
	'clock_state':
		{'system_status':
			{'associations_address': '10.16.2.2',
			 'associations_local_mode': 'client',
			 'clock_offset': 27.027,
			 'clock_refid': '127.127.1.1',
			 'clock_state': 'synchronized',
			 'clock_stratum': 3,
			 'root_delay': 5.61}
		},
	'peer':
		{'10.16.2.2':
			{'local_mode':
				{'client':
					{'delay': 5.61,
					'jitter': 3.342,
					'mode': 'synchronized',
					'offset': 27.027,
					'poll': 64,
					'reach': 7,
					'receive_time': 25,
					'refid': '127.127.1.1',
					'remote': '10.16.2.2',
					'stratum': 3,
					'local_mode': 'client'}
				}
			},
		'10.36.3.3':
			{'local_mode':
				{'client':
					{'delay': 0.0,
					'jitter': 15937.0,
					'mode': 'configured',
					'offset': 0.0,
					'poll': 512,
					'reach': 0,
					'receive_time': '-',
					'refid': '.STEP.',
					'remote': '10.36.3.3',
					'stratum': 16,
					'local_mode': 'client'}
				}
			}
		}
	}

	ShowNtpStatus = {
		'clock_state': {
			'system_status': {
				'act_freq': 1000.4589,
				'last_update': '182 sec ago',
				'nom_freq': 1000.0003,
				'offset': 27.0279,
				'peerdispersion': 3.34,
				'poll': 64,
				'precision': '2**14',
				'refid': '10.16.2.2',
				'reftime': 'DFA02517.D2F7B9F6 '
						   '(13:40:23.824 EST Wed Nov '
						   '21 2018)',
				'resolution': 1000,
				'rootdelay': 5.61,
				'rootdispersion': 273.61,
				'status': 'synchronized',
				'stratum': 4,
				'uptime': '239700 (1/100 of seconds)'}
		}
	}

	ShowNtpConfig = {
        'vrf': {
            'default': {
                'address': {
                    '10.16.2.2': {
                        'isconfigured': {
                            'True': {
                                'address': '10.16.2.2',
                                'isconfigured': True}
                        },
                        'type': {
                            'server': {
                                'address': '10.16.2.2',
                                'source': 'Loopback0',
                                'type': 'server',
                                'vrf': 'default'}
                        }
                    },
                    '10.36.3.3': {
                        'isconfigured': {
                            'True': {
                                'address': '10.36.3.3',
                                'isconfigured': True}
                        },
                        'type': {
                            'server': {
                                'address': '10.36.3.3',
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
				'associations_address': '10.16.2.2',
                'associations_local_mode': 'client',
                'clock_offset': 27.027,
                'clock_precision': '2**14',
                'clock_refid': '127.127.1.1',
                'clock_state': 'synchronized',
                'clock_stratum': 3,
                'reference_time': 'DFA02517.D2F7B9F6 '
                                  '(13:40:23.824 EST '
                                  'Wed Nov 21 2018)',
                'root_delay': 5.61,
                'root_dispersion': 273.61}
        },
 		'vrf': {
 			'default': {
 				'associations': {
 					'address': {
 						'10.16.2.2': {
 							'local_mode': {
 								'client': {
 									'isconfigured': {
 										True: {
 											'address': '10.16.2.2',
                                            'delay': 5.61,
                                            'isconfigured': True,
                                            'local_mode': 'client',
                                            'offset': 27.027,
                                            'poll': 64,
                                            'reach': 7,
                                            'receive_time': 25,
                                            'refid': '127.127.1.1',
                                            'stratum': 3,
                                            'vrf': 'default'}
                                    }
                                }
                            }
                        },
                        '10.36.3.3': {
                        	'local_mode': {
                        		'client': {
                        			'isconfigured': {
                        				True: {
                        					'address': '10.36.3.3',
                                            'delay': 0.0,
                                            'isconfigured': True,
                                            'local_mode': 'client',
                                            'offset': 0.0,
                                            'poll': 512,
                                            'reach': 0,
                                            'receive_time': '-',
                                            'refid': '.STEP.',
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
                		'10.16.2.2': {
                			'type': {
                				'server': {
                					'address': '10.16.2.2',
                                    'source': 'Loopback0',
                                    'type': 'server',
                                    'vrf': 'default'}
                            }
                        },
                        '10.36.3.3': {
                        	'type': {
                        		'server': {
                        			'address': '10.36.3.3',
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