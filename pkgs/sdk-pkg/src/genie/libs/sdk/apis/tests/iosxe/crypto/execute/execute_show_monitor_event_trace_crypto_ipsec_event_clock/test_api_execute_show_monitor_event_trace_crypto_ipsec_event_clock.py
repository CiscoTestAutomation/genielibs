from unittest import TestCase
from genie.libs.sdk.apis.iosxe.crypto.execute import execute_show_monitor_event_trace_crypto_ipsec_event_clock
from unittest.mock import Mock


class TestExecuteShowMonitorEventTraceCryptoIpsecEventClock(TestCase):

    def test_execute_show_monitor_event_trace_crypto_ipsec_event_clock(self):
        self.device = Mock()
        results_map = {
            'show monitor event-trace crypto ipsec event clock 21:40': 'Tracing currently disabled, from exec command',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_monitor_event_trace_crypto_ipsec_event_clock(self.device, '21', '40', 30)
        self.assertIn(
            'show monitor event-trace crypto ipsec event clock 21:40',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show monitor event-trace crypto ipsec event clock 21:40']
        self.assertEqual(result, expected_output)
