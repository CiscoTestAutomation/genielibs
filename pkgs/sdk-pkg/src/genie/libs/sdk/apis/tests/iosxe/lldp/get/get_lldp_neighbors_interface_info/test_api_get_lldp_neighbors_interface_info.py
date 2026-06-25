import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError, InvalidCommandError)
from genie.libs.sdk.apis.iosxe.lldp.get import (
    get_lldp_neighbors_interface_info)


class TestGetLldpNeighborsInterfaceInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_neighbors_interface_info(self):
        expected_output = {
            'interface': {
                'GigabitEthernet1/0/15': {
                    'port_id': {
                        'Gi1/0/1': {
                            'local_intf_service_instance': {
                                'chassis_id': '843d.c6ff.f1b8',
                                'port_id': 'Gi1/0/1',
                                'port_description': 'GigabitEthernet1/0/1',
                                'system_name': 'R5',
                            },
                            'system_description': {
                                'cisco_ios_software': 'C3750E Software',
                                'catalyst_l3_switch_software': (
                                    'C3750E-UNIVERSALK9-M'),
                                'copyright': (
                                    'Copyright (c) 1986-2016 by Cisco '
                                    'Systems, Inc.'),
                                'compiled': 'Wed 23-Mar-16 16:33',
                                'time_remaining_sec': 108,
                                'system_capabilities': 'B,R',
                                'enabled_capabilities': 'B,R',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': {
                                    0: '1000baseT(FD)',
                                },
                                'vlan_id': 1,
                                'peer_source_mac': '843d.c6ff.f1b8',
                            },
                        }
                    }
                }
            },
            'total_entries_displayed': 1,
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_neighbors_interface_info(
            self.device, 'GigabitEthernet1/0/15')
        self.device.parse.assert_called_once_with(
            'show lldp neighbors GigabitEthernet1/0/15 detail')
        self.assertEqual(result, expected_output)

    def test_get_lldp_neighbors_interface_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_neighbors_interface_info(
            self.device, 'GigabitEthernet1/0/15')
        self.assertIsNone(result)

    def test_get_lldp_neighbors_interface_info_invalid_command(self):
        self.device.parse.side_effect = InvalidCommandError("Invalid")
        result = get_lldp_neighbors_interface_info(
            self.device, 'GigabitEthernet1/0/15')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
