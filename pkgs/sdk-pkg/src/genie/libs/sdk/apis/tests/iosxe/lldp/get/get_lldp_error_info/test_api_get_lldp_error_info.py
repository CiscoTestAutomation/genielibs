import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_error_info


class TestGetLldpErrorInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_error_info(self):
        expected_output = {
            'memory': 0,
            'encapsulation': 0,
            'input_queue': 0,
            'table': 0,
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_error_info(self.device)
        self.device.parse.assert_called_once_with('show lldp errors')
        self.assertEqual(result, expected_output)

    def test_get_lldp_error_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_error_info(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
