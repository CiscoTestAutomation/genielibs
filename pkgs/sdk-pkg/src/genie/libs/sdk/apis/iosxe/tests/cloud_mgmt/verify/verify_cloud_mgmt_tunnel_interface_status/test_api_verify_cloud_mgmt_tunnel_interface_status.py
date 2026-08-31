from unittest import TestCase
from unittest.mock import Mock
from genie.utils import Dq
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_mgmt_tunnel_interface_status
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtTunnelInterfaceStatus(TestCase):
    """Tests for verify_cloud_mgmt_tunnel_interface_status.

    Parser: ShowCloudMgmtConnect (show cloud-mgmt connect)
    Schema key path: output.q.contains('cloud-mgmt_tunnel_interface').get_values('status'/'rx_errors'/'tx_errors', 0)
    """

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def _make_parsed_output(self, status, rx_errors, tx_errors):
        """Return a Dq-compatible parsed dict matching the real ShowCloudMgmtConnect schema."""
        parsed = {
            'service_cloud-mgmt_connect': 'enable',
            'cloud-mgmt_tunnel_interface': {
                'status': status,
                'rx_packets': 100,
                'tx_packets': 100,
                'rx_errors': rx_errors,
                'tx_errors': tx_errors,
                'rx_drop_packets': 0,
                'tx_drop_packets': 0,
            }
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output

    def test_tunnel_interface_status_success(self):
        """Test successful verification when status, rx_errors and tx_errors all match"""
        self._make_parsed_output('Enable', 0, 0)
        result = verify_cloud_mgmt_tunnel_interface_status(
            self.device,
            expected_status='Enable',
            expected_rx_errors=0,
            expected_tx_errors=0,
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_tunnel_interface_status_mismatch(self):
        """Test failure when interface status does not match expected"""
        self._make_parsed_output('Disable', 0, 0)
        result = verify_cloud_mgmt_tunnel_interface_status(
            self.device,
            expected_status='Enable',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_rx_errors_mismatch(self):
        """Test failure when rx_errors does not match expected"""
        self._make_parsed_output('Enable', 5, 0)
        result = verify_cloud_mgmt_tunnel_interface_status(
            self.device,
            expected_rx_errors=0,
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_tx_errors_mismatch(self):
        """Test failure when tx_errors does not match expected"""
        self._make_parsed_output('Enable', 0, 10)
        result = verify_cloud_mgmt_tunnel_interface_status(
            self.device,
            expected_tx_errors=0,
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_status_lookup_is_scoped_to_tunnel_interface(self):
        """Test that device registration 'Registered' status does not satisfy expected tunnel interface status"""
        parsed = {
            'service_cloud-mgmt_connect': 'enable',
            'cloud-mgmt_tunnel_interface': {
                'status': 'Enable',
                'rx_packets': 100,
                'tx_packets': 100,
                'rx_errors': 0,
                'tx_errors': 0,
                'rx_drop_packets': 0,
                'tx_drop_packets': 0,
            },
            'cloud-mgmt_device_registration': {
                'url': 'https://catalyst.meraki.com/nodes/register',
                'devices': {
                    '1': {
                        'pid': 'IE-3500-8U3X',
                        'serial_number': 'FCW2805Y304',
                        'mac_address': 'A0:BC:6F:CC:A7:80',
                        'status': 'Registered',
                        'timestamp(utc)': '2025-03-21 09:12:19',
                    }
                }
            }
        }
        mock_output = Mock()
        mock_output.q = Dq(parsed)
        self.device.parse.return_value = mock_output
        # 'Registered' from device_registration must not satisfy expected_status='Enable'
        result = verify_cloud_mgmt_tunnel_interface_status(
            self.device,
            expected_status='Enable',
            max_time=1,
            check_interval=1
        )
        self.assertTrue(result)

    def test_parser_empty_output(self):
        """Test failure when parser raises SchemaEmptyParserError"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)
        result = verify_cloud_mgmt_tunnel_interface_status(
            self.device,
            expected_status='Enable',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_no_expected_values_returns_false(self):
        """Test that omitting all expected values returns False without calling parse"""
        result = verify_cloud_mgmt_tunnel_interface_status(self.device, max_time=1, check_interval=1)
        self.assertFalse(result)
        self.device.parse.assert_not_called()
