from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_conversion_status
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyConversionStatus(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_output(self, conversion_status):
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_output.get.return_value = {}
        mock_q.get_values.return_value = conversion_status
        self.device.parse.return_value = mock_output

    def test_conversion_status_success(self):
        self._make_output('Registered')
        result = verify_conversion_status(self.device, expected_conversion_status='Registered', max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_conversion_status_mismatch(self):
        self._make_output('Unregistered')
        result = verify_conversion_status(self.device, expected_conversion_status='Registered', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_conversion_status_not_found(self):
        self._make_output(None)
        result = verify_conversion_status(self.device, expected_conversion_status='Registered', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_conversion_status_empty_string(self):
        """Test that empty string is treated as a valid value, not missing"""
        self._make_output('')
        result = verify_conversion_status(self.device, expected_conversion_status='', max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_parser_empty_output(self):
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_conversion_status(self.device, expected_conversion_status='Registered', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_conversion_status_switch_number_success(self):
        """Test conversion status verification with explicit switch_number using real parser schema"""
        mock_output = MagicMock()
        mock_output.get.side_effect = lambda k, d=None: {
            'meraki': {'switch': {'1': {'conversion_status': 'Registered'}}}
        }.get(k, d if d is not None else {})
        mock_output.q = MagicMock()
        self.device.parse.return_value = mock_output
        result = verify_conversion_status(self.device, expected_conversion_status='Registered', switch_number=1, max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_conversion_status_switch_number_not_found(self):
        """Test conversion status with switch_number that does not exist in real parser schema"""
        mock_output = MagicMock()
        mock_output.get.side_effect = lambda k, d=None: {
            'meraki': {'switch': {'1': {'conversion_status': 'Registered'}}}
        }.get(k, d if d is not None else {})
        mock_output.q = MagicMock()
        self.device.parse.return_value = mock_output
        result = verify_conversion_status(self.device, expected_conversion_status='Registered', switch_number=99, max_time=1, check_interval=1)
        self.assertFalse(result)
