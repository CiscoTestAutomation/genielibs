from unittest import TestCase
from genie.libs.sdk.apis.iosxe.crypto.execute import execute_show_monitor_event_trace_crypto_all
from unittest.mock import Mock


class TestExecuteShowMonitorEventTraceCryptoAll(TestCase):

    def test_execute_show_monitor_event_trace_crypto_all(self):
        self.device = Mock()
        results_map = {
            'show monitor event-trace crypto all': '''
pki_event:

Tracing currently disabled, from exec command


pki_internal_event:

Tracing currently disabled, from exec command


pki_error:

Tracing currently disabled, from exec command


ikev2_event:

Tracing currently disabled, from exec command


ikev2_internal_event:

Tracing currently disabled, from exec command


ikev2_error:

Tracing currently disabled, from exec command


ikev2_exception:

Tracing currently disabled, from exec command


ipsec_event:

Tracing currently disabled, from exec command


ipsec_error:

Tracing currently disabled, from exec command


ipsec_exception:

Tracing currently disabled, from exec command

interrupt context allocation count = 0''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_monitor_event_trace_crypto_all(self.device)
        self.assertIn(
            'show monitor event-trace crypto all',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show monitor event-trace crypto all']
        self.assertEqual(result, expected_output)
