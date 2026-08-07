import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.span.verify import verify_span_session


def _build_session_info(session_id='1', session_type='Local Session',
                        src_direct='rx_only', src_port='Gi0/1/4',
                        dst_port='Gi0/1/5', source_ports=None):
    """Build a ShowMonitorSchema-shaped dict for one session."""
    if source_ports is None:
        source_ports = {src_direct: src_port}
    return {
        'session': {
            session_id: {
                'type': session_type,
                'source_ports': source_ports,
                'destination_ports': dst_port,
            }
        }
    }


class TestVerifySpanSession(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_match_all_fields(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info())
        self.assertTrue(verify_span_session(
            self.device, '1',
            session_type='Local Session', src_direct='rx_only',
            src_port='Gi0/1/4', dst_port='Gi0/1/5'))
        self.device.api.get_span_session_info.assert_called_once_with('1')

    def test_match_no_expectations(self):
        # When all expects are None, function only checks that session
        # exists.
        self.device.api.get_span_session_info.return_value = (
            _build_session_info())
        self.assertTrue(verify_span_session(self.device, '1'))

    def test_mismatch_type(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info(session_type='Local Session'))
        self.assertFalse(verify_span_session(
            self.device, '1', session_type='ERSPAN Source'))

    def test_mismatch_src_direct(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info(src_direct='rx_only'))
        self.assertFalse(verify_span_session(
            self.device, '1', src_direct='tx_only'))

    def test_match_src_direct_only_configured_direction_present(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info(
                source_ports={
                    'rx_only': 'Gi0/1/4',
                }))
        self.assertTrue(verify_span_session(
            self.device, '1', src_direct='rx_only', src_port='Gi0/1/4'))

    def test_mismatch_src_port(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info(src_port='Gi0/1/4'))
        self.assertFalse(verify_span_session(
            self.device, '1', src_port='Gi0/1/9'))

    def test_mismatch_dst_port(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info(dst_port='Gi0/1/5'))
        self.assertFalse(verify_span_session(
            self.device, '1', dst_port='Gi0/1/9'))

    def test_session_info_none(self):
        self.device.api.get_span_session_info.return_value = None
        self.assertFalse(verify_span_session(self.device, '1'))

    def test_expect_not_exist_when_missing(self):
        self.device.api.get_span_session_info.return_value = None
        self.assertTrue(verify_span_session(
            self.device, '1', expect_exist=False))

    def test_expect_not_exist_when_present_fails(self):
        self.device.api.get_span_session_info.return_value = (
            _build_session_info())
        self.assertFalse(verify_span_session(
            self.device, '1',
            session_type='Local Session', expect_exist=False))


if __name__ == '__main__':
    unittest.main()
