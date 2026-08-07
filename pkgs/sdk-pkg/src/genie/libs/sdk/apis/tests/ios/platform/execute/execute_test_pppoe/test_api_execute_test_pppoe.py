from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.platform.execute import execute_test_pppoe


class TestExecuteTestPppoe(TestCase):

    def test_execute_test_pppoe(self):
        self.device = Mock()
        results_map = {
            'test pppoe 1 1 GigabitEthernet0/2': '',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_test_pppoe(self.device, '1', '1', 'GigabitEthernet0/2', 60)
        self.assertIn(
            'test pppoe 1 1 GigabitEthernet0/2',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)

    def test_execute_test_pppoe_raises(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure("failed")
        with self.assertRaises(SubCommandFailure):
            execute_test_pppoe(self.device, '1', '1', 'GigabitEthernet0/2')
