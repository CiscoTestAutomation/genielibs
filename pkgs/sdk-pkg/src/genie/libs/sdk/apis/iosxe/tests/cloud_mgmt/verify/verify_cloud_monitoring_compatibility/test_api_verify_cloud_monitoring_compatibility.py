from unittest import TestCase
from unittest.mock import Mock, MagicMock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import (
    verify_cloud_monitoring_compatibility,
)
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMonitoringCompatibility(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def test_cloud_monitoring_compatibility_success(self):
        """Test successful cloud monitoring compatibility verification"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'Compatible'

        self.device.parse.return_value = mock_output

        result = verify_cloud_monitoring_compatibility(
            self.device,
            expected_cloud_monitoring_compatibility='Compatible',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_cloud_monitoring_compatibility_mismatch(self):
        """Test cloud monitoring compatibility mismatch"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = 'Incompatible'

        self.device.parse.return_value = mock_output

        result = verify_cloud_monitoring_compatibility(
            self.device,
            expected_cloud_monitoring_compatibility='Compatible',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_cloud_monitoring_compatibility_not_found(self):
        """Test cloud monitoring compatibility not found in output"""
        mock_output = MagicMock()
        mock_q = MagicMock()
        mock_output.q = mock_q
        mock_q.get_values.return_value = None

        self.device.parse.return_value = mock_output

        result = verify_cloud_monitoring_compatibility(
            self.device,
            expected_cloud_monitoring_compatibility='Compatible',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test handling of empty parser output"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)

        result = verify_cloud_monitoring_compatibility(
            self.device,
            expected_cloud_monitoring_compatibility='Compatible',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_no_expected_value_returns_false(self):
        """Test that omitting the expected value returns False."""
        result = verify_cloud_monitoring_compatibility(
            self.device, max_time=1, check_interval=1
        )

        self.assertFalse(result)
        self.device.parse.assert_not_called()
