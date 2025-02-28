from unittest import TestCase
from genie.libs.sdk.apis.iosxe.line.clear import clear_raw_socket_transport_statistics_all
from unittest.mock import Mock


class TestClearRawSocketTransportStatisticsAll(TestCase):

    def test_clear_raw_socket_transport_statistics_all(self):
        self.device = Mock()
        results_map = {
            'clear raw-socket transport statistics all': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_raw_socket_transport_statistics_all(self.device)
        self.assertIn(
            'clear raw-socket transport statistics all',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
