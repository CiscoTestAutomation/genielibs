from unittest import TestCase
from genie.libs.sdk.apis.iosxe.test_platform.execute import execute_test_platform
from unittest.mock import Mock


class TestExecuteTestPlatform(TestCase):

    def test_execute_test_platform(self):
        self.device = Mock()
        results_map = {
            'test platform software trace slot fp active cpp-service rotate': '  Rotated file from: ---, Bytes: 776, Messages: 1',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_platform(self.device, 'software trace slot fp active cpp-service rotate', 60)
        self.assertIn(
            'test platform software trace slot fp active cpp-service rotate',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['test platform software trace slot fp active cpp-service rotate']
        self.assertEqual(result, expected_output)
