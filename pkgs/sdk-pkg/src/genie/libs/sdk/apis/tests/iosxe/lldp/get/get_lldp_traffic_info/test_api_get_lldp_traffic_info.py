import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_traffic_info


class TestGetLldpTrafficInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_traffic_info(self):
        expected_output = {
            "frame_in": 13315,
            "frame_out": 20372,
            "frame_error_in": 0,
            "frame_discard": 14,
            "tlv_discard": 0,
            "tlv_unknown": 0,
            "entries_aged_out": 34,
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_traffic_info(self.device)
        self.device.parse.assert_called_once_with('show lldp traffic')
        self.assertEqual(result, expected_output)

    def test_get_lldp_traffic_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_traffic_info(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
