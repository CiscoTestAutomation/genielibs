from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import (
    verify_cloud_mgmt_migration_details,
)
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtMigrationDetails(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def test_migration_details_success(self):
        """Test successful migration details verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q

        def get_values_side_effect(key, index):
            values = {
                'current_booted_mode': 'cloud',
                'migration_in_progress': 'No'
            }
            return values.get(key)

        mock_q.get_values.side_effect = get_values_side_effect
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_current_booted_mode='cloud',
            expected_migration_in_progress='No',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_migration_details_booted_mode_mismatch(self):
        """Test booted mode mismatch"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q

        def get_values_side_effect(key, index):
            values = {
                'current_booted_mode': 'standalone',
                'migration_in_progress': 'No'
            }
            return values.get(key)

        mock_q.get_values.side_effect = get_values_side_effect
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_current_booted_mode='cloud',
            expected_migration_in_progress='No',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_migration_in_progress_mismatch(self):
        """Test migration in progress mismatch"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q

        def get_values_side_effect(key, index):
            values = {
                'current_booted_mode': 'cloud',
                'migration_in_progress': 'Yes'
            }
            return values.get(key)

        mock_q.get_values.side_effect = get_values_side_effect
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_current_booted_mode='cloud',
            expected_migration_in_progress='No',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_booted_mode_not_found(self):
        """Test booted mode not found in output"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q

        def get_values_side_effect(key, index):
            return None

        mock_q.get_values.side_effect = get_values_side_effect
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_current_booted_mode='cloud',
            expected_migration_in_progress='No',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test handling of empty parser output"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_current_booted_mode='cloud',
            expected_migration_in_progress='No',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_only_booted_mode_supplied(self):
        """Test verification with only expected_current_booted_mode."""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q

        def get_values_side_effect(key, index):
            values = {
                'current_booted_mode': 'cloud'
            }
            return values.get(key)

        mock_q.get_values.side_effect = get_values_side_effect
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_current_booted_mode='cloud',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_only_migration_in_progress_supplied(self):
        """Test verification with only expected_migration_in_progress."""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q

        def get_values_side_effect(key, index):
            values = {
                'migration_in_progress': 'No'
            }
            return values.get(key)

        mock_q.get_values.side_effect = get_values_side_effect
        self.device.parse.return_value = mock_output

        result = verify_cloud_mgmt_migration_details(
            self.device,
            expected_migration_in_progress='No',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_no_expected_values_returns_false(self):
        """Test that omitting all expected values returns False."""
        result = verify_cloud_mgmt_migration_details(
            self.device, max_time=1, check_interval=1
        )
        self.assertFalse(result)
        self.device.parse.assert_not_called()
