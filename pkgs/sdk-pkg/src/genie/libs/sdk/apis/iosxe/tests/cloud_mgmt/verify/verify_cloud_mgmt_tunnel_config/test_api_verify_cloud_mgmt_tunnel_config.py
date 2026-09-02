from unittest import TestCase
from unittest.mock import Mock
from genie.utils import Dq
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_mgmt_tunnel_config
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtTunnelConfig(TestCase):
    """Tests for verify_cloud_mgmt_tunnel_config.

    Parser: ShowCloudMgmtConnect (show cloud-mgmt connect)
    Schema key path: output.q.get_values('fetch_fail'/'fetch_state'/'network_name', 0)
    """

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_parsed_output(self, fetch_state, fetch_fail, network_name):
        """Return a Dq-compatible parsed dict matching the real ShowCloudMgmtConnect schema."""
        parsed = {
            'service_cloud-mgmt_connect': 'enable',
            'cloud-mgmt_tunnel_config': {
                'fetch_state': fetch_state,
                'fetch_fail': fetch_fail,
                'network_name': network_name,
            }
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output

    def test_tunnel_config_success(self):
        """Test successful verification when fetch_state, fetch_fail and network_name all match"""
        self._make_parsed_output('Config fetch succeeded', '', 'Meraki_bgl - switch')
        result = verify_cloud_mgmt_tunnel_config(
            self.device,
            expected_fetch_fail='',
            expected_fetch_state='Config fetch succeeded',
            expected_network_name='Meraki_bgl - switch',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_fetch_fail_mismatch(self):
        """Test failure when fetch_fail does not match expected"""
        self._make_parsed_output('Config fetch failed', 'Connection timeout', 'Meraki_bgl - switch')
        result = verify_cloud_mgmt_tunnel_config(
            self.device,
            expected_fetch_fail='',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_fetch_state_mismatch(self):
        """Test failure when fetch_state does not match expected"""
        self._make_parsed_output('Config fetch failed', '', 'Meraki_bgl - switch')
        result = verify_cloud_mgmt_tunnel_config(
            self.device,
            expected_fetch_state='Config fetch succeeded',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_network_name_mismatch(self):
        """Test failure when network_name does not match expected"""
        self._make_parsed_output('Config fetch succeeded', '', 'Different Network')
        result = verify_cloud_mgmt_tunnel_config(
            self.device,
            expected_network_name='Meraki_bgl - switch',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test failure when parser raises SchemaEmptyParserError"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_cloud_mgmt_tunnel_config(
            self.device,
            expected_fetch_state='Config fetch succeeded',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_no_expected_values_returns_false(self):
        """Test that omitting all expected values returns False without calling parse"""
        result = verify_cloud_mgmt_tunnel_config(self.device, max_time=1, check_interval=1)
        self.assertFalse(result)
        self.device.parse.assert_not_called()
