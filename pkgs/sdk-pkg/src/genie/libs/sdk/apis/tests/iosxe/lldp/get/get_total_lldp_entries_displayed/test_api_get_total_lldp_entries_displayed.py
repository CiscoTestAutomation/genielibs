import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.lldp.get import get_total_lldp_entries_displayed


class TestGetTotalLldpEntriesDisplayed(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_total_lldp_entries_displayed(self):
        self.device.parse.return_value = {
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
        result = get_total_lldp_entries_displayed(self.device)
        self.device.parse.assert_called_once_with('show lldp neighbors')
        self.assertEqual(result, 2)

    def test_get_total_lldp_entries_displayed_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_total_lldp_entries_displayed(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
