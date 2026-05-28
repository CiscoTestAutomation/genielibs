from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_monitor_event_trace_crypto
from unittest.mock import Mock


class TestExecuteMonitorEventTraceCrypto(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.execute.return_value = ''

    def test_event_clear(self):
        execute_monitor_event_trace_crypto(
            self.device, action='event', clear=True, protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec event clear'
        )

    def test_error_dump_pretty_merged(self):
        execute_monitor_event_trace_crypto(
            self.device, action='error', dump=True, pretty=True, merged=True, protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec error dump merged pretty'
        )

    def test_error_dump_pretty_url(self):
        execute_monitor_event_trace_crypto(
            self.device, action='error', dump=True, pretty=True,
            event_data_url='tftp://host/file', protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec error dump pretty tftp://host/file'
        )

    def test_error_dump_pretty(self):
        execute_monitor_event_trace_crypto(
            self.device, action='error', dump=True, pretty=True, protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec error dump pretty'
        )

    def test_exception_dump_pretty_merged(self):
        execute_monitor_event_trace_crypto(
            self.device, action='exception', dump=True, pretty=True, merged=True, protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec exception dump merged pretty'
        )

    def test_exception_dump_pretty_url(self):
        execute_monitor_event_trace_crypto(
            self.device, action='exception', dump=True, pretty=True,
            event_data_url='tftp://host/file', protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec exception dump pretty tftp://host/file'
        )

    def test_exception_dump_pretty(self):
        execute_monitor_event_trace_crypto(
            self.device, action='exception', dump=True, pretty=True, protocol='ipsec'
        )
        self.device.execute.assert_called_once_with(
            'monitor event-trace crypto ipsec exception dump pretty'
        )
