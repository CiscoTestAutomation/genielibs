from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipsec.get import get_monitor_event_trace_crypto_ipsec_event_from_boot_detail
from unittest.mock import Mock


class TestGetMonitorEventTraceCryptoIpsecEventFromBootDetail(TestCase):

    def test_get_monitor_event_trace_crypto_ipsec_event_from_boot_detail(self):
        self.device = Mock()
        results_map = {
            'show monitor event-trace crypto ipsec event from-boot detail': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_monitor_event_trace_crypto_ipsec_event_from_boot_detail(self.device)
        self.assertIn(
            'show monitor event-trace crypto ipsec event from-boot detail',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
