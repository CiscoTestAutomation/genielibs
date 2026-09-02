from unittest import TestCase
from unittest.mock import Mock
from genie.utils import Dq
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_mgmt_connect_status
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtConnectStatus(TestCase):
    """Tests for verify_cloud_mgmt_connect_status.

    Parser: ShowCloudMgmtConnect (show cloud-mgmt connect)
    Schema key path: output.q.get_values('service_cloud-mgmt_connect', 0)
    """

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_parsed_output(self, connect_status):
        """Return a Dq-compatible parsed dict matching the real ShowCloudMgmtConnect schema."""
        parsed = {'service_cloud-mgmt_connect': connect_status}
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output

    def test_connect_status_success(self):
        """Test successful verification when connect status matches expected"""
        self._make_parsed_output('enable')
        result = verify_cloud_mgmt_connect_status(
            self.device,
            expected_connect_status='enable',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_connect_status_mismatch(self):
        """Test failure when connect status does not match expected"""
        self._make_parsed_output('disable')
        result = verify_cloud_mgmt_connect_status(
            self.device,
            expected_connect_status='enable',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test failure when parser raises SchemaEmptyParserError"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_cloud_mgmt_connect_status(
            self.device,
            expected_connect_status='enable',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_connect_status_key_absent(self):
        """Test failure when service_cloud-mgmt_connect key is absent from parsed output"""
        parsed = {}
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output
        result = verify_cloud_mgmt_connect_status(
            self.device,
            expected_connect_status='enable',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)
