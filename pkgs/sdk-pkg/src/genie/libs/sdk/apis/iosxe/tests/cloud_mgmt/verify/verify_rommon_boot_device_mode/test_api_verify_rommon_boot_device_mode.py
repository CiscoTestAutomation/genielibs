from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import (
    verify_rommon_boot_device_mode,
)
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyRommonBootDeviceMode(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def test_boot_device_mode_success(self):
        """Test successful boot device mode verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'cloud'

        self.device.parse.return_value = mock_output

        result = verify_rommon_boot_device_mode(
            self.device,
            expected_boot_device_mode='cloud',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_boot_device_mode_mismatch(self):
        """Test boot device mode mismatch"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'standalone'

        self.device.parse.return_value = mock_output

        result = verify_rommon_boot_device_mode(
            self.device,
            expected_boot_device_mode='cloud',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_boot_device_mode_not_found(self):
        """Test boot device mode not found in output"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = None

        self.device.parse.return_value = mock_output

        result = verify_rommon_boot_device_mode(
            self.device,
            expected_boot_device_mode='cloud',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test handling of empty parser output"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)

        result = verify_rommon_boot_device_mode(
            self.device,
            expected_boot_device_mode='cloud',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_no_expected_value_returns_false(self):
        """Test that omitting the expected value returns False."""
        result = verify_rommon_boot_device_mode(
            self.device, max_time=1, check_interval=1
        )

        self.assertFalse(result)
        self.device.parse.assert_not_called()
