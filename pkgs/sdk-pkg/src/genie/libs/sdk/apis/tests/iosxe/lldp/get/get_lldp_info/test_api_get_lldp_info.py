import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_info


class TestGetLldpInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_info(self):
        expected_output = {
            "hello_timer": 30,
            "enabled": True,
            "hold_timer": 120,
            "status": "active",
            "reinit_timer": 2,
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_info(self.device)
        self.device.parse.assert_called_once_with('show lldp')
        self.assertEqual(result, expected_output)

    def test_get_lldp_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_info(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
