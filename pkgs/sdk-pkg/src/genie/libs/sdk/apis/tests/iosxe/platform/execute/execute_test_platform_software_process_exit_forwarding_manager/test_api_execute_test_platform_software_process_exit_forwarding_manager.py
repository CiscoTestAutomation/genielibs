from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_test_platform_software_process_exit_forwarding_manager
from unittest.mock import Mock


class TestExecuteTestPlatformSoftwareProcessExitForwardingManager(TestCase):

    def test_execute_test_platform_software_process_exit_forwarding_manager(self):
        self.device = Mock()
        results_map = {
            'test platform software process exit forwarding-manager RP active': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_platform_software_process_exit_forwarding_manager(self.device, 'RP', 'active')
        self.assertIn(
            'test platform software process exit forwarding-manager RP active',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
