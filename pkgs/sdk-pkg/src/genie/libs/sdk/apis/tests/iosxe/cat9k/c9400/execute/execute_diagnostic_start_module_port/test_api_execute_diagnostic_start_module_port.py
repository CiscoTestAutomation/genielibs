from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9400.execute import execute_diagnostic_start_module_port
from unittest.mock import Mock


class TestExecuteDiagnosticStartModulePort(TestCase):

    def test_execute_diagnostic_start_module_port(self):
        self.device = Mock()
        results_map = {
            'diagnostic start module 2 test 2 port 2': """Diagnostic[module 2]: Running test(s) 2 may disrupt normal system operation and requires reload
Do you want to continue? [no]: yes""",
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_diagnostic_start_module_port(self.device, 2, '2', '2')
        self.assertIn(
            'diagnostic start module 2 test 2 port 2',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
