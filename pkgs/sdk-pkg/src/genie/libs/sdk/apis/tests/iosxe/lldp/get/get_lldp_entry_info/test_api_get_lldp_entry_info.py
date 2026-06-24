import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_entry_info


class TestGetLldpEntryInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_entry_info(self):
        expected_output = {
            'total_entries': 1,
            'interfaces': {
                'GigabitEthernet1/0/15': {
                    'if_name': 'GigabitEthernet1/0/15',
                    'port_id': {
                        'Gi1/0/1': {
                            'neighbors': {
                                'R5': {
                                    'chassis_id': '843d.c6ff.f1b8',
                                    'port_id': 'Gi1/0/1',
                                    'neighbor_id': 'R5',
                                    'port_description': 'GigabitEthernet1/0/1',
                                    'system_name': 'R5',
                                    'time_remaining': 108,
                                    'capabilities': {
                                        'mac_bridge': {
                                            'system': True,
                                            'enabled': True,
                                            'name': 'mac_bridge',
                                        },
                                        'router': {
                                            'system': True,
                                            'enabled': True,
                                            'name': 'router',
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_entry_info(self.device, '*')
        self.device.parse.assert_called_once_with('show lldp entry *')
        self.assertEqual(result, expected_output)
        self.assertEqual(result.get('total_entries'), 1)

    def test_get_lldp_entry_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_entry_info(self.device, '*')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
