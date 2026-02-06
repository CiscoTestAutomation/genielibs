from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_test_pppoe
from unittest.mock import Mock


class TestExecuteTestPppoe(TestCase):

    def test_execute_test_pppoe(self):
        self.device = Mock()
        results_map = {
            'test pppoe 1 1 Te0/0/2': '',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_test_pppoe(self.device, '1', '1', 'Te0/0/2', 60)
        self.assertIn(
            'test pppoe 1 1 Te0/0/2',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
