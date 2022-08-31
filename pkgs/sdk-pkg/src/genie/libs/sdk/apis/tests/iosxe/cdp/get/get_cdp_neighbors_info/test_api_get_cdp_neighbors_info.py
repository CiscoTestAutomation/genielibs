import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cdp.get import get_cdp_neighbors_info


class TestGetCdpNeighborsInfo(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          1783-CMS20DN:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-CMS20DN']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_cdp_neighbors_info(self):
        result = get_cdp_neighbors_info(self.device)
        expected_output = {'index': {1: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 147,
               'local_interface': 'GigabitEthernet1/1',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'TenGigabitEthernet1/1',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           2: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 135,
               'local_interface': 'GigabitEthernet1/17',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet2/5',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           3: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 154,
               'local_interface': 'GigabitEthernet1/15',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet1/9',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           4: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 139,
               'local_interface': 'GigabitEthernet1/12',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet1/8',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           5: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 174,
               'local_interface': 'GigabitEthernet1/14',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet1/7',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           6: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 125,
               'local_interface': 'GigabitEthernet1/8',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet1/4',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           7: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 158,
               'local_interface': 'GigabitEthernet1/13',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet1/6',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           8: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 175,
               'local_interface': 'GigabitEthernet1/6',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'GigabitEthernet1/3',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           9: {'advertisement_ver': 2,
               'capabilities': 'Router Switch IGMP',
               'device_id': 'device',
               'duplex_mode': 'full',
               'entry_addresses': {},
               'hold_time': 169,
               'local_interface': 'GigabitEthernet1/4',
               'management_addresses': {},
               'native_vlan': '1',
               'platform': 'cisco IE-3300-8U2X',
               'port_id': 'TenGigabitEthernet1/2',
               'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                   'Switch Software (IE3x00-UNIVERSALK9-M), '
                                   'Experimental Version 17.9.20220411:075757 '
                                   '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                   '101]\n'
                                   'Copyright (c) 1986-2022 by Cisco Systems, '
                                   'Inc.\n'
                                   'Compiled Mon 11-Apr-22 00:57 by mcpre',
               'vtp_management_domain': ' '},
           10: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': 'device',
                'duplex_mode': 'full',
                'entry_addresses': {},
                'hold_time': 178,
                'local_interface': 'GigabitEthernet1/5',
                'management_addresses': {},
                'native_vlan': '1',
                'platform': 'cisco IE-3300-8U2X',
                'port_id': 'GigabitEthernet2/1',
                'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                    'Switch Software (IE3x00-UNIVERSALK9-M), '
                                    'Experimental Version 17.9.20220411:075757 '
                                    '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Mon 11-Apr-22 00:57 by mcpre',
                'vtp_management_domain': ' '},
           11: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': 'device',
                'duplex_mode': 'full',
                'entry_addresses': {},
                'hold_time': 145,
                'local_interface': 'GigabitEthernet1/19',
                'management_addresses': {},
                'native_vlan': '1',
                'platform': 'cisco IE-3300-8U2X',
                'port_id': 'GigabitEthernet2/8',
                'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                    'Switch Software (IE3x00-UNIVERSALK9-M), '
                                    'Experimental Version 17.9.20220411:075757 '
                                    '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Mon 11-Apr-22 00:57 by mcpre',
                'vtp_management_domain': ' '},
           12: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': 'device',
                'duplex_mode': 'full',
                'entry_addresses': {},
                'hold_time': 169,
                'local_interface': 'GigabitEthernet1/7',
                'management_addresses': {},
                'native_vlan': '1',
                'platform': 'cisco IE-3300-8U2X',
                'port_id': 'GigabitEthernet1/5',
                'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                    'Switch Software (IE3x00-UNIVERSALK9-M), '
                                    'Experimental Version 17.9.20220411:075757 '
                                    '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Mon 11-Apr-22 00:57 by mcpre',
                'vtp_management_domain': ' '},
           13: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': 'device',
                'duplex_mode': 'full',
                'entry_addresses': {},
                'hold_time': 167,
                'local_interface': 'GigabitEthernet1/18',
                'management_addresses': {},
                'native_vlan': '1',
                'platform': 'cisco IE-3300-8U2X',
                'port_id': 'GigabitEthernet2/7',
                'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                    'Switch Software (IE3x00-UNIVERSALK9-M), '
                                    'Experimental Version 17.9.20220411:075757 '
                                    '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Mon 11-Apr-22 00:57 by mcpre',
                'vtp_management_domain': ' '},
           14: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': 'device',
                'duplex_mode': 'full',
                'entry_addresses': {},
                'hold_time': 163,
                'local_interface': 'GigabitEthernet1/16',
                'management_addresses': {},
                'native_vlan': '1',
                'platform': 'cisco IE-3300-8U2X',
                'port_id': 'GigabitEthernet2/6',
                'software_version': 'Cisco IOS Software [Cupertino], IE3x00 '
                                    'Switch Software (IE3x00-UNIVERSALK9-M), '
                                    'Experimental Version 17.9.20220411:075757 '
                                    '[BLD_POLARIS_DEV_LATEST_20220411_072129:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Mon 11-Apr-22 00:57 by mcpre',
                'vtp_management_domain': ' '},
           15: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': '1783-CMS10B',
                'duplex_mode': 'full',
                'entry_addresses': {'11.1.18.205': {}},
                'hold_time': 146,
                'local_interface': 'GigabitEthernet1/3',
                'management_addresses': {'11.1.18.205': {}},
                'native_vlan': '1',
                'platform': 'Allen-Bradley 1783-CMS10B',
                'port_id': 'GigabitEthernet1/1',
                'software_version': 'Cisco IOS Software [Dublin], S5200 Switch '
                                    'Software (S5200-UNIVERSALK9-M), '
                                    'Experimental Version '
                                    '17.10.20220708:150333 '
                                    '[BLD_POLARIS_DEV_LATEST_20220708_143608:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Fri 08-Jul-22 08:03 by mcpre',
                'vtp_management_domain': ' '},
           16: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': '1783-CMS20DN',
                'duplex_mode': 'full',
                'entry_addresses': {'11.1.18.201': {}},
                'hold_time': 163,
                'local_interface': 'GigabitEthernet1/2',
                'management_addresses': {'11.1.18.201': {}},
                'native_vlan': '1',
                'platform': 'Allen-Bradley 1783-CMS20DN',
                'port_id': 'GigabitEthernet1/11',
                'software_version': 'Cisco IOS Software [Dublin], S5200 Switch '
                                    'Software (S5200-UNIVERSALK9-M), '
                                    'Experimental Version '
                                    '17.10.20220708:150333 '
                                    '[BLD_POLARIS_DEV_LATEST_20220708_143608:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Fri 08-Jul-22 08:03 by mcpre',
                'vtp_management_domain': ' '},
           17: {'advertisement_ver': 2,
                'capabilities': 'Router Switch IGMP',
                'device_id': '1783-CMS20DN',
                'duplex_mode': 'full',
                'entry_addresses': {'11.1.18.201': {}},
                'hold_time': 177,
                'local_interface': 'GigabitEthernet1/11',
                'management_addresses': {'11.1.18.201': {}},
                'native_vlan': '1',
                'platform': 'Allen-Bradley 1783-CMS20DN',
                'port_id': 'GigabitEthernet1/2',
                'software_version': 'Cisco IOS Software [Dublin], S5200 Switch '
                                    'Software (S5200-UNIVERSALK9-M), '
                                    'Experimental Version '
                                    '17.10.20220708:150333 '
                                    '[BLD_POLARIS_DEV_LATEST_20220708_143608:/nobackup/mcpre/s2c-build-ws '
                                    '101]\n'
                                    'Copyright (c) 1986-2022 by Cisco Systems, '
                                    'Inc.\n'
                                    'Compiled Fri 08-Jul-22 08:03 by mcpre',
                'vtp_management_domain': ' '}},
 'total_entries_displayed': 17}
        self.assertEqual(result, expected_output)
