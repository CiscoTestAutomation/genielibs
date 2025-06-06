from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_diagnostic_start_module_port
from unittest.mock import Mock


class TestExecuteDiagnosticStartModulePort(TestCase):

    def test_execute_diagnostic_start_module_port(self):
        self.device = Mock()
        results_map = {
            'diagnostic start module 1 test 1 port 5': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_diagnostic_start_module_port(self.device, 1, '1', '5')
        self.assertIn(
            'diagnostic start module 1 test 1 port 5',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
