class PlatformOutput(object):

    # 'show version output
    showVersionOutput =  {
        'chassis_detail': 'ASR 9006 4 Line Card Slot Chassis with V2 AC PEM',
        'config_register': '0x1922',
        'image': 'disk0:asr9k-os-mbi-6.1.4.10I/0x100305/mbiasr9k-rsp3.vm',
        'main_mem': 'cisco ASR9K Series (Intel 686 F6M14S4) processor with 6291456K '
                    'bytes of memory.',
        'operating_system': 'IOSXR',
        'processor': 'Intel 686 F6M14S4',
        'processor_memory_bytes': '6291456K',
        'device_family': 'ASR9K',
        'rp_config_register': '0x1922',
        'software_version': '6.1.4.10I',
        'uptime': '5 hours, 14 minutes'}

    # 'show sdr detail' output
    showSdrDetailOutput = {
        'sdr_id': {
            0: {
                'dsdrsc_node': '0/RSP0/CPU0',
                'dsdrsc_partner_node': '0/RSP1/CPU0',
                'mac_address': 'a80c.0d5f.ab17',
                'membership': {
                    '0/0/CPU0': {
                        'node_status': 'IOS XR RUN',
                        'partner_name': 'NONE',
                        'red_state': 'Not-known',
                        'type': 'LC'},
                    '0/RSP0/CPU0': {
                        'node_status': 'IOS XR RUN',
                        'partner_name': '0/RSP1/CPU0',
                        'red_state': 'Primary',
                        'type': 'RP'},
                    '0/RSP1/CPU0': {
                        'node_status': 'IOS XR RUN',
                        'partner_name': '0/RSP0/CPU0',
                        'red_state': 'Backup',
                        'type': 'RP'}},
                'primary_node1': '0/RSP0/CPU0',
                'primary_node2': '0/RSP1/CPU0',
                'sdr_name': 'Owner'}}}

    # 'show plaform' output
    showPlatformOutput = {
        'slot': {
            'lc': {
                '0/0': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-MOD80-SE',
                    'state': 'IOS XR RUN',
                    'subslot': {
                        '0': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MPA-20X1GE',
                            'redundancy_state': 'None',
                            'state': 'OK'},
                        '1': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MQA-20X2GE',
                            'redundancy_state': 'None',
                            'state': 'OK'},
                        '2': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MRA-20X3GE',
                            'redundancy_state': 'None',
                            'state': 'OK'}}}},
            'rp': {
                '0/RSP0': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-RSP440-TR',
                    'redundancy_state': 'Active',
                    'state': 'IOS XR RUN'},
                '0/RSP1': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-RSP440-TR',
                    'redundancy_state': 'Standby',
                    'state': 'IOS XR RUN'}}}}

    # 'show platform vm' output
    showPlatformVmOutput = {
        'node': {
            '0/0/CPU0': {
                'ip_address': '192.0.0.6',
                'partner_name': 'NONE',
                'sw_status': 'FINAL Band',
                'type': 'LC (ACTIVE)'},
            '0/RP0/CPU0': {
                'ip_address': '192.0.0.4',
                'partner_name': 'NONE',
                'sw_status': 'FINAL Band',
                'type': 'RP (ACTIVE)'}}}

    # 'show install active summary'
    showInstallActiveSummaryOutput = {
        'active_packages': ['disk0:asr9k-mini-px-6.1.21.15I',
                            'disk0:asr9k-mpls-px-6.1.21.15I',
                            'disk0:asr9k-mcast-px-6.1.21.15I',
                            'disk0:asr9k-mgbl-px-6.1.21.15I'],
        'sdr': 'Owner'}

    # 'show inventory' output
    showInventoryOutput = {
        'module_name': {
            'module 0/RSP0/CPU0': {
                'descr': 'ASR9K Route Switch '
                         'Processor with 440G/slot '
                         'Fabric and 6GB',
                'pid': 'A9K-RSP440-TR',
                'sn': 'FOC1808NEND',
                'vid': 'V05'},
            'module 0/RSP1/CPU0': {
                'descr': 'ASR9K Route Switch '
                         'Processor with 440G/slot '
                         'Fabric and 6GB',
                'pid': 'A9K-MPA-20X1GE',
                'sn': 'FOC1811N49J',
                'vid': 'V02'},
            'module mau 0/0/0/0': {
                'descr': 'Unknown or Unsupported '
                         'CPAK Module',
                'pid': 'GLC-T',
                'sn': '00000MTC160107LP',
                'vid': 'N/A'},
            'module mau 0/0/0/1': {
                'descr': 'Unknown or Unsupported '
                         'CPAK Module',
                'pid': 'GLC-T',
                'sn': '00000MTC17150731',
                'vid': 'N/A'}}}

    # 'admin show diag chassis' ouptput
    adminShowDiagChassisOutput = {
        'chassis_feature': 'V2 AC PEM',
        'clei': 'IPMUP00BRB',
        'desc': 'ASR 9006 4 Line Card Slot Chassis with V2 AC PEM',
        'device_family': 'ASR',
        'device_series': 9006,
        'num_line_cards': 4,
        'pid': 'ASR-9006-AC-V2',
        'rack_num': 0,
        'sn': 'FOX1810G8LR',
        'top_assy_num': '68-4235-02',
        'vid': 'V02'}

    # 'show redundancy summary' output
    showRedundancySummaryOutput = {
        "redundancy_communication": True,
        'node': {
            '0/RSP0/CPU0(A)': {
                'node_detail': 'Node Not Ready, NSR: Not '
                               'Configured',
                'standby_node': '0/RSP1/CPU0(S)',
                'type': 'active'},
            '0/RSP0/CPU0(P)': {
                'backup_node': '0/RSP1/CPU0(B)',
                'node_detail': 'Proc Group Not Ready, NSR: '
                               'Ready',
                'standby_node': '0/RSP1/CPU0(B)',
                'type': 'primary'}}}

    # 'show redundancy' output
    showRedundancyOutput = {
        'node': {
            '0/RSP0/CPU0': {
                'group': {
                    'central-services': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not '
                                  'Ready'},
                    'dlrsc': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not Ready'},
                    'dsc': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not Ready'},
                    'mcast-routing': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not '
                                  'Ready'},
                    'netmgmt': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not Ready'},
                    'v4-routing': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not Ready'},
                    'v6-routing': {
                        'backup': 'N/A',
                        'primary': '0/RSP0/CPU0',
                        'status': 'Not Ready'}},
                'last_reload_timestamp': 'Thu Apr 27 02:14:12 '
                                         '2017',
                'last_switchover_timepstamp': 'Thu Apr 27 '
                                              '03:29:57 2017',
                'node_uptime': '8 minutes',
                'node_uptime_in_seconds': 480,
                'node_uptime_timestamp': 'Thu Apr 27 03:22:37 '
                                         '2017',
                'primary_rmf_state': 'not ready',
                'primary_rmf_state_reason': 'Backup is not '
                                            'Present',
                'reload_cause': 'Initiating switch-over',
                'role': 'ACTIVE',
                'time_since_last_reload': '1 hour, 16 minutes ago',
                'time_since_last_switchover': '1 minute ago',
                'valid_partner': ''}}}

    # 'dir:' output
    dirOutput = {
        'dir': {
            'dir_name': 'disk0a:/usr',
            'total_bytes': '2562719744 bytes',
            'total_free_bytes': '1918621184 bytes'}}

    # Platform Ops Object final output
    platformOpsOutput = {
        'attributes': None,
        "redundancy_communication": True,
        #'callables': {},
        'chassis': 'ASR 9006 4 Line Card Slot Chassis with V2 AC PEM',
        'chassis_sn': 'FOX1810G8LR',
        'config_register': '0x1922',
        'connections': None,
        #'context_manager': {},
        #'device': <Device aDevice at 0xf6fcf8ac>,
        #'diff_ignore': deque(['maker', 'callables', 'device']),
        'image': 'disk0:asr9k-os-mbi-6.1.4.10I/0x100305/mbiasr9k-rsp3.vm',
        'installed_packages': ['disk0:asr9k-mini-px-6.1.21.15I',
                               'disk0:asr9k-mpls-px-6.1.21.15I',
                               'disk0:asr9k-mcast-px-6.1.21.15I',
                               'disk0:asr9k-mgbl-px-6.1.21.15I'],
        'main_mem': '6291456K',
        #'maker': <genie.ops.base.maker.Maker object at 0xf6fcfacc>,
        'os': 'IOSXR',
        'rtr_type': 'ASR9K',
        'sdr_owner': 'Owner',
        'rp_uptime': 480,
        'slot': {
            'lc': {
                '0/0': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-MOD80-SE',
                    'state': 'IOS XR RUN',
                    'subslot': {
                        '0': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MPA-20X1GE',
                            'redundancy_state': 'None',
                            'state': 'OK'},
                        '1': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MQA-20X2GE',
                            'redundancy_state': 'None',
                            'state': 'OK'},
                        '2': {
                            'config_state': 'PWR,NSHUT,MON',
                            'name': 'A9K-MRA-20X3GE',
                            'redundancy_state': 'None',
                            'state': 'OK'}}}},
            'rp': {
                '0/RSP0': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-RSP440-TR',
                    'redundancy_state': 'Active',
                    'state': 'IOS XR RUN'},
                '0/RSP1': {
                    'config_state': 'PWR,NSHUT,MON',
                    'name': 'A9K-RSP440-TR',
                    'redundancy_state': 'Standby',
                    'state': 'IOS XR RUN'},
                'rp_config_register': '0x1922'}},
        'version': '6.1.4.10I',
        'virtual_device': {
            0: {
                'membership': {
                    '0/0/CPU0': {
                        'vd_ms_partner_name': 'NONE',
                        'vd_ms_red_state': 'Not-known',
                        'vd_ms_status': 'IOS '
                                        'XR '
                                        'RUN',
                        'vd_ms_type': 'LC'},
                    '0/RSP0/CPU0': {
                        'vd_ms_partner_name': '0/RSP1/CPU0',
                        'vd_ms_red_state': 'Primary',
                        'vd_ms_status': 'IOS '
                                        'XR '
                                        'RUN',
                        'vd_ms_type': 'RP'},
                    '0/RSP1/CPU0': {
                        'vd_ms_partner_name': '0/RSP0/CPU0',
                        'vd_ms_red_state': 'Backup',
                        'vd_ms_status': 'IOS '
                                       'XR '
                                       'RUN',
                        'vd_ms_type': 'RP'}},
                'vd_dSDRsc_nod': '0/RSP0/CPU0',
                'vd_dSDRsc_partner_node': '0/RSP1/CPU0',
                'vd_mac_addr': 'a80c.0d5f.ab17',
                'vd_name': 'Owner',
                'vd_primary_node1': '0/RSP0/CPU0',
                'vd_primary_node2': '0/RSP1/CPU0'}}}


# vim: ft=python et sw=4
