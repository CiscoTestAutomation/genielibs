import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_neighbors_brief_info


class TestGetLldpNeighborsBriefInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_neighbors_brief_info(self):
        expected_output = {
            'total_entries': 2,
            'interfaces': {
                'GigabitEthernet1/0/15': {
                    'port_id': {
                        'Gi1/0/1': {
                            'neighbors': {'R5': {'hold_time': 120}}
                        }
                    }
                },
                'GigabitEthernet1/0/16': {
                    'port_id': {
                        'Gi1/0/2': {
                            'neighbors': {'R6': {'hold_time': 120}}
                        }
                    }
                },
            },
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_neighbors_brief_info(self.device)
        self.device.parse.assert_called_once_with('show lldp neighbors')
        self.assertEqual(result, expected_output)
        self.assertEqual(result.get('total_entries'), 2)
        self.assertIn('interfaces', result)
        self.assertIn('GigabitEthernet1/0/15', result['interfaces'])

    def test_get_lldp_neighbors_brief_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_neighbors_brief_info(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
