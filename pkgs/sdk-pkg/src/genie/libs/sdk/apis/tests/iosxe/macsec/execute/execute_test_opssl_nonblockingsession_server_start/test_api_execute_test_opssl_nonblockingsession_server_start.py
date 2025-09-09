from unittest import TestCase
from genie.libs.sdk.apis.iosxe.macsec.execute import execute_test_opssl_nonblockingsession_server_start
from unittest.mock import Mock


class TestExecuteTestOpsslNonblockingsessionServerStart(TestCase):

    def test_execute_test_opssl_nonblockingsession_server_start(self):
        self.device = Mock()
        results_map = {
            'test opssl nonblockingsession server tls1.2 start 192.168.1.1 9001 134217727 0 server': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_opssl_nonblockingsession_server_start(self.device, 'tls1.2', 'start', '192.168.1.1', '9001', '134217727', '0', 'server', 'server')
        self.assertIn(
            'test opssl nonblockingsession server tls1.2 start 192.168.1.1 9001 134217727 0 server',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
