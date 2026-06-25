from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_test_platform_software_command
from unittest.mock import Mock


class TestExecuteTestPlatformSoftwareCommand(TestCase):

    def test_execute_test_platform_software_command(self):
        self.device = Mock()
        results_map = {
            'test platform software bp crimson node 1 power redundancy-mode combined provision': (
                '$e bp crimson node 1 power redundancy-mode combined provision\n'
                'Setting node 1 red_type combined oper 0'
            ),
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_platform_software_command(self.device, 'bp', 'redundancy-mode', 'combined', 'provision', '1')
        self.assertIn(
            'test platform software bp crimson node 1 power redundancy-mode combined provision',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = (
            '$e bp crimson node 1 power redundancy-mode combined provision\n'
            'Setting node 1 red_type combined oper 0'
        )
        self.assertEqual(result, expected_output)
