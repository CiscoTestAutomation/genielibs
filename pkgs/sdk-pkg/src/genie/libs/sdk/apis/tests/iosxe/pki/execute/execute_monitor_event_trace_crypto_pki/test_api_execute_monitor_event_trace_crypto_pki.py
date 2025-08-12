from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_monitor_event_trace_crypto_pki
from unittest.mock import Mock


class TestExecuteMonitorEventTraceCryptoPki(TestCase):

    def test_event_clear(self):
        self.device = Mock()
        results_map = {
            "['monitor event-trace crypto pki event clear']": '{}',
        }
        self.device.execute.side_effect = lambda arg, **kwargs: results_map.get(str(arg))
        result = execute_monitor_event_trace_crypto_pki(self.device, 'event', clear=True)
        self.assertIn(
            "['monitor event-trace crypto pki event clear']",
            str(self.device.execute.call_args_list[0][0])
        )
        self.assertEqual(result, None)

    def test_event_internal_continuous_cancel(self):
        self.device = Mock()
        results_map = {
            "['monitor event-trace crypto pki event internal continuous', "
            "'monitor event-trace crypto pki event internal continuous cancel']": '{}',
        }
        self.device.execute.side_effect = lambda arg, **kwargs: results_map.get(str(arg))
        result = execute_monitor_event_trace_crypto_pki(self.device, 'event', internal=True, continuous=True, cancel=True)
        self.assertIn(
            "['monitor event-trace crypto pki event internal continuous', 'monitor event-trace crypto pki event internal continuous cancel']",
            str(self.device.execute.call_args_list[0][0])
        )
        self.assertEqual(result, None)

    def test_event_dump_pretty_with_url(self):
        self.device = Mock()
        results_map = {
            "['monitor event-trace crypto pki event dump pretty flash:/trace.txt']": '{}',
        }
        self.device.execute.side_effect = lambda arg, **kwargs: results_map.get(str(arg))
        result = execute_monitor_event_trace_crypto_pki(self.device, 'event', dump=True, pretty=True, event_data_url='flash:/trace.txt')
        self.assertIn(
            "['monitor event-trace crypto pki event dump pretty flash:/trace.txt']",
            str(self.device.execute.call_args_list[0][0])
        )
        self.assertEqual(result, None)

    def test_error_enable(self):
        self.device = Mock()
        results_map = {
            "['monitor event-trace crypto pki error enable']": '{}',
        }
        self.device.execute.side_effect = lambda arg, **kwargs: results_map.get(str(arg))
        result = execute_monitor_event_trace_crypto_pki(self.device, 'error', enable=True)
        self.assertIn(
            "['monitor event-trace crypto pki error enable']",
            str(self.device.execute.call_args_list[0][0])
        )
        self.assertEqual(result, None)

    def test_error_dump_with_url(self):
        self.device = Mock()
        results_map = {
            "['monitor event-trace crypto pki error dump flash:/error_trace.txt']": '{}',
        }
        self.device.execute.side_effect = lambda arg, **kwargs: results_map.get(str(arg))
        result = execute_monitor_event_trace_crypto_pki(self.device, 'error', dump=True, event_data_url='flash:/error_trace.txt')
        self.assertIn(
            "['monitor event-trace crypto pki error dump flash:/error_trace.txt']",
            str(self.device.execute.call_args_list[0][0])
        )
        self.assertEqual(result, None)

    def test_event_internal_all_flags(self):
        self.device = Mock()
        results_map = {
            "['monitor event-trace crypto pki event internal clear', "
            "'monitor event-trace crypto pki event internal continuous', "
            "'monitor event-trace crypto pki event internal continuous cancel', "
            "'monitor event-trace crypto pki event internal disable', "
            "'monitor event-trace crypto pki event internal dump pretty flash:/full_trace.txt', "
            "'monitor event-trace crypto pki event internal enable', "
            "'monitor event-trace crypto pki event internal one-shot']": '{}',
        }
        self.device.execute.side_effect = lambda arg, **kwargs: results_map.get(str(arg))
        result = execute_monitor_event_trace_crypto_pki(
            self.device,
            'event',
            clear=True,
            continuous=True,
            cancel=True,
            disable=True,
            dump=True,
            enable=True,
            internal=True,
            one_shot=True,
            event_data_url='flash:/full_trace.txt',
            pretty=True
        )
        self.assertIn(
            "['monitor event-trace crypto pki event internal clear', 'monitor event-trace crypto pki event internal continuous', "
            "'monitor event-trace crypto pki event internal continuous cancel', 'monitor event-trace crypto pki event internal disable', "
            "'monitor event-trace crypto pki event internal dump pretty flash:/full_trace.txt', 'monitor event-trace crypto pki event internal enable', "
            "'monitor event-trace crypto pki event internal one-shot']",
            str(self.device.execute.call_args_list[0][0])
        )
        self.assertEqual(result, None)

    def test_event_internal_invalid_with_error(self):
        self.device = Mock()
        with self.assertRaises(ValueError):
            execute_monitor_event_trace_crypto_pki(self.device, 'error', internal=True)
