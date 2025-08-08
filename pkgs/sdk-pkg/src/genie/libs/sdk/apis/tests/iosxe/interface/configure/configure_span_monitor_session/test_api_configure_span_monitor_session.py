from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_span_monitor_session
from unittest.mock import Mock


class TestConfigureSpanMonitorSession(TestCase):

    def test_configure_span_monitor_session(self):
        self.device = Mock()
        result = configure_span_monitor_session(self.device, '1', 'FiftyGigE1/0/3', 'both', 'FiftyGigE1/0/9')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['monitor session 1  source interface FiftyGigE1/0/3 both', 'monitor session 1  destination interface FiftyGigE1/0/9'],)
        )
        
    def test_configure_span_monitor_session_2(self):
        self.device = Mock()
        result = configure_span_monitor_session(self.device, '10', None, None, None, '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['monitor session 10  source vlan 100'],)
        )
