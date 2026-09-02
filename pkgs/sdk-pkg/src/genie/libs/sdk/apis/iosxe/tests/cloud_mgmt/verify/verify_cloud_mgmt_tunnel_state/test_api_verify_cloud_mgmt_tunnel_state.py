from unittest import TestCase
from unittest.mock import Mock
from genie.utils import Dq
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_mgmt_tunnel_state
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtTunnelState(TestCase):
    """Tests for verify_cloud_mgmt_tunnel_state.

    Parser: ShowCloudMgmtConnect (show cloud-mgmt connect)
    Schema key path: output.q.contains('cloud-mgmt_tunnel_state').get_values('primary'/'secondary')
    """

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_parsed_output(self, primary, secondary):
        """Return a Dq-compatible parsed dict matching the real ShowCloudMgmtConnect schema."""
        parsed = {
            'service_cloud-mgmt_connect': 'Enabled',
            'cloud-mgmt_tunnel_state': {
                'primary': primary,
                'secondary': secondary,
            }
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.execute.return_value = ''
        self.device.parse.return_value = mock_output

    def test_tunnel_state_success(self):
        """Test successful verification when both primary and secondary are Up"""
        self._make_parsed_output('Up', 'Up')
        result = verify_cloud_mgmt_tunnel_state(
            self.device,
            expected_primary_status='Up',
            expected_secondary_status='Up',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_tunnel_primary_mismatch(self):
        """Test failure when primary status does not match expected"""
        self._make_parsed_output('Down', 'Up')
        result = verify_cloud_mgmt_tunnel_state(
            self.device,
            expected_primary_status='Up',
            expected_secondary_status='Up',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_tunnel_secondary_mismatch(self):
        """Test failure when secondary status does not match expected"""
        self._make_parsed_output('Up', 'Down')
        result = verify_cloud_mgmt_tunnel_state(
            self.device,
            expected_primary_status='Up',
            expected_secondary_status='Up',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_tunnel_state_key_absent(self):
        """Test failure when cloud-mgmt_tunnel_state key is absent from parsed output"""
        parsed = {'service_cloud-mgmt_connect': 'Enabled'}
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.execute.return_value = ''
        self.device.parse.return_value = mock_output
        result = verify_cloud_mgmt_tunnel_state(
            self.device,
            expected_primary_status='Up',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test failure when parser raises SchemaEmptyParserError"""
        self.device.execute.return_value = ''
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_cloud_mgmt_tunnel_state(
            self.device,
            expected_primary_status='Up',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_no_expected_values_returns_false(self):
        """Test that omitting all expected values returns False without calling parse"""
        result = verify_cloud_mgmt_tunnel_state(self.device, max_time=1, check_interval=1)
        self.assertFalse(result)
        self.device.parse.assert_not_called()
