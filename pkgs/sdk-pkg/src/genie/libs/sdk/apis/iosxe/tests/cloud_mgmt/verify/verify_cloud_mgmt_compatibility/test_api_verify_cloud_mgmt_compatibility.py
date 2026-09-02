from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.utils import Dq
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import (
    verify_cloud_mgmt_compatibility,
)
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtCompatibility(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def test_cloud_monitoring_success(self):
        """Test successful cloud monitoring verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'Compatible'
        mock_q.contains.return_value = mock_q

        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_cloud_monitoring='Compatible',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_boot_status_success(self):
        """Test successful boot status verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'Compatible'
        mock_q.contains.return_value = mock_q

        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_boot_status='Compatible',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_boot_status_mismatch(self):
        """Test boot status mismatch"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'Incompatible'
        mock_q.contains.return_value = mock_q

        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_boot_status='Compatible',
            max_time=3,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test handling of empty parser output"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_cloud_monitoring='Compatible',
            max_time=3,
            check_interval=1
        )
        self.assertFalse(result)
    def test_switch_specific_without_switch_number_fails(self):
        """Test switch-specific fields require a switch number."""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'Compatible'
        mock_q.contains.return_value = mock_q

        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_sku_model='IE-3500-8U3X',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)
    def test_boot_mode_success(self):
        """Test successful boot mode verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'INSTALL'
        mock_q.contains.return_value = mock_q

        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_boot_mode='INSTALL',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_boot_message_contains_success(self):
        """Test successful boot message contains verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = (
            'Image is in INSTALL mode and compatible'
        )
        mock_q.contains.return_value = mock_q

        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_boot_message='INSTALL mode',
            boot_message_match='contains',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_no_expected_values_returns_false(self):
        """Test that omitting all expected values returns False."""
        result = verify_cloud_mgmt_compatibility(
            self.device, max_time=1, check_interval=1
        )
        self.assertFalse(result)
        self.device.parse.assert_not_called()

    def test_second_expansion_module_matches(self):
        """Test a match on the second expansion module succeeds."""
        parsed = {
            'cloud_mgmt_cloud_monitoring': 'Compatible',
            'cloud_mgmt_cloud_management': {
                'boot_mode': {'mode': 'INSTALL', 'status': 'Compatible'},
                'switch_details': [
                    {
                        'switch_number': 1,
                        'sku': {
                            'model': 'IE-3500-8U3X',
                            'status': 'Compatible',
                        },
                        'bootloader_version': {
                            'version': '26.1.1r',
                            'status': 'Compatible',
                        },
                        'expansion_modules': [
                            {'model': 'IEM-3500-4MU', 'status': 'Compatible'},
                            {'model': 'IEM-3500-8T', 'status': 'Incompatible'},
                        ],
                    }
                ],
            },
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_switch_number=1,
            expected_expansion_module_model='IEM-3500-8T',
            expected_expansion_module_status='Incompatible',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_expansion_module_no_match(self):
        """Test failure when no expansion module record matches."""
        parsed = {
            'cloud_mgmt_cloud_monitoring': 'Compatible',
            'cloud_mgmt_cloud_management': {
                'boot_mode': {'mode': 'INSTALL', 'status': 'Compatible'},
                'switch_details': [
                    {
                        'switch_number': 1,
                        'sku': {
                            'model': 'IE-3500-8U3X',
                            'status': 'Compatible',
                        },
                        'bootloader_version': {
                            'version': '26.1.1r',
                            'status': 'Compatible',
                        },
                        'expansion_modules': [
                            {'model': 'IEM-3500-4MU', 'status': 'Compatible'},
                            {'model': 'IEM-3500-8T', 'status': 'Compatible'},
                        ],
                    }
                ],
            },
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_compatibility(
            self.device,
            expected_switch_number=1,
            expected_expansion_module_model='IEM-3500-8T',
            expected_expansion_module_status='Incompatible',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)
