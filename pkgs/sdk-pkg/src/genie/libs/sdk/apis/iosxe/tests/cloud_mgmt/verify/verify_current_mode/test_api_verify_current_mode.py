from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_current_mode
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCurrentMode(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_output(self, current_mode):
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_output.get.return_value = {}
        mock_q.get_values.return_value = current_mode
        self.device.parse.return_value = mock_output

    def test_current_mode_success(self):
        self._make_output('IE35xx-M')
        result = verify_current_mode(self.device, expected_current_mode='IE35xx-M', max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_current_mode_mismatch(self):
        self._make_output('WRONG-MODE')
        result = verify_current_mode(self.device, expected_current_mode='IE35xx-M', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_current_mode_not_found(self):
        self._make_output(None)
        result = verify_current_mode(self.device, expected_current_mode='IE35xx-M', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_parser_empty_output(self):
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_current_mode(self.device, expected_current_mode='IE35xx-M', max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_current_mode_switch_number_success(self):
        """Test current mode verification with explicit switch_number using real parser schema"""
        mock_output = MagicMock()
        mock_output.get.side_effect = lambda k, d=None: {
            'meraki': {'switch': {'1': {'current_mode': 'IE35xx-M'}}}
        }.get(k, d if d is not None else {})
        mock_output.q = MagicMock()
        self.device.parse.return_value = mock_output
        result = verify_current_mode(self.device, expected_current_mode='IE35xx-M', switch_number=1, max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_current_mode_switch_number_not_found(self):
        """Test current mode with switch_number that does not exist in real parser schema"""
        mock_output = MagicMock()
        mock_output.get.side_effect = lambda k, d=None: {
            'meraki': {'switch': {'1': {'current_mode': 'IE35xx-M'}}}
        }.get(k, d if d is not None else {})
        mock_output.q = MagicMock()
        self.device.parse.return_value = mock_output
        result = verify_current_mode(self.device, expected_current_mode='IE35xx-M', switch_number=99, max_time=1, check_interval=1)
        self.assertFalse(result)
